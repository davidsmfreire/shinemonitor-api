// Package shinemonitor is a client for the ShineMonitor REST API
// (https://api.shinemonitor.com/), used by WatchPower, SolarPower, and
// other vendor apps for Voltronic-derived inverters.
//
// Most action methods live in the generated actions.go; this file
// holds the handwritten core: signing, login, and the request
// dispatcher that the generated methods call.
package shinemonitor

import (
	"context"
	"crypto/sha1" //nolint:gosec // vendor-mandated
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
)

const (
	// DefaultBaseURL is the vendor mobile host used by WatchPower-class apps.
	// Vendor also exposes api.shinemonitor.com for documented REST traffic;
	// the suffix-context/_app_id_ pinning below targets the mobile host.
	DefaultBaseURL = "http://android.shinemonitor.com/public/"

	// WatchPowerSuffixContext is the app-context query string emitted by
	// the WatchPower Android app. Pins the request fingerprint to that app.
	WatchPowerSuffixContext = "&i18n=pt_BR&lang=pt_BR&source=1&_app_client_=android" +
		"&_app_id_=wifiapp.volfw.watchpower&_app_version_=1.0.6.3"

	// WatchPowerCompanyKey is the vendor identifier issued to the WatchPower
	// app. Reverse-engineered from the Android client; required by authSource.
	WatchPowerCompanyKey = "bnrl_frRFjEz8Mkn"
)

// Auth is the result of a successful login — what subsequent requests sign with.
type Auth struct {
	Token    string
	Secret   string
	Expire   int64
	Acquired time.Time
}

// Client is the entry point. Construct with New(...) — the zero value
// is unusable.
type Client struct {
	BaseURL       string
	SuffixContext string
	CompanyKey    string
	HTTP          *http.Client
	auth          *Auth
}

// Option mutates a freshly-constructed Client. Use the With* functions.
type Option func(*Client)

// WithBaseURL overrides the default vendor URL (useful for tests against
// the mock server).
func WithBaseURL(s string) Option { return func(c *Client) { c.BaseURL = s } }

// WithSuffixContext overrides the default app-context query string.
func WithSuffixContext(s string) Option { return func(c *Client) { c.SuffixContext = s } }

// WithCompanyKey overrides the default vendor identifier.
func WithCompanyKey(s string) Option { return func(c *Client) { c.CompanyKey = s } }

// WithHTTP injects a caller-managed *http.Client (custom timeouts/transport).
func WithHTTP(h *http.Client) Option { return func(c *Client) { c.HTTP = h } }

// New constructs a Client. Defaults match the WatchPower Android app context.
func New(opts ...Option) *Client {
	c := &Client{
		BaseURL:       DefaultBaseURL,
		SuffixContext: WatchPowerSuffixContext,
		CompanyKey:    WatchPowerCompanyKey,
		HTTP:          &http.Client{Timeout: 10 * time.Second},
	}
	for _, opt := range opts {
		opt(c)
	}
	return c
}

// Auth returns the current login token+secret, or nil if not logged in.
func (c *Client) AuthState() *Auth { return c.auth }

// APIError wraps a non-zero `err` field returned by the API. Callers
// can check IsAuth() to decide whether to re-prompt for credentials.
type APIError struct {
	Err  int
	Desc string
	Raw  json.RawMessage
}

func (e *APIError) Error() string {
	return fmt.Sprintf("shinemonitor: err=0x%04X desc=%q", e.Err, e.Desc)
}

func (e *APIError) IsAuth() bool {
	_, ok := authErrCodes[e.Err]
	return ok
}

var authErrCodes = map[int]struct{}{
	0x0007: {}, 0x000F: {}, 0x0010: {}, 0x0019: {}, 0x0105: {}, 0x010E: {},
}

// Login signs in and stores the token+secret on the client.
func (c *Client) Login(ctx context.Context, username, password string) error {
	baseAction := fmt.Sprintf(
		"&action=authSource&usr=%s&company-key=%s%s",
		username, c.CompanyKey, c.SuffixContext,
	)
	salt := saltMs()
	pwdHash := sha1Hex(password)
	sign := sha1Hex(salt + pwdHash + baseAction)
	url := fmt.Sprintf("%s?sign=%s&salt=%s%s", c.BaseURL, sign, salt, baseAction)

	payload, err := c.fetch(ctx, url)
	if err != nil {
		return err
	}
	var resp struct {
		Err  int    `json:"err"`
		Desc string `json:"desc"`
		Dat  struct {
			Secret string `json:"secret"`
			Token  string `json:"token"`
			Expire int64  `json:"expire"`
		} `json:"dat"`
	}
	if err := json.Unmarshal(payload, &resp); err != nil {
		return fmt.Errorf("decode login response: %w", err)
	}
	if resp.Err != 0 {
		return &APIError{Err: resp.Err, Desc: resp.Desc, Raw: payload}
	}
	c.auth = &Auth{
		Token:    resp.Dat.Token,
		Secret:   resp.Dat.Secret,
		Expire:   resp.Dat.Expire,
		Acquired: time.Now(),
	}
	return nil
}

// requestWith signs and dispatches an authed request whose action-specific
// query segment was assembled by the caller (typically a generated method
// in actions.go).
func (c *Client) requestWith(ctx context.Context, action, extra string) (json.RawMessage, error) {
	if c.auth == nil {
		return nil, &APIError{Err: -1, Desc: "not logged in"}
	}
	baseAction := fmt.Sprintf("&action=%s%s%s", action, extra, c.SuffixContext)
	salt := saltMs()
	sign := sha1Hex(salt + c.auth.Secret + c.auth.Token + baseAction)
	url := fmt.Sprintf(
		"%s?sign=%s&salt=%s&token=%s%s",
		c.BaseURL, sign, salt, c.auth.Token, baseAction,
	)
	return c.fetchAndCheck(ctx, url)
}

func (c *Client) fetch(ctx context.Context, url string) (json.RawMessage, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}
	resp, err := c.HTTP.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("http %d", resp.StatusCode)
	}
	return io.ReadAll(resp.Body)
}

func (c *Client) fetchAndCheck(ctx context.Context, url string) (json.RawMessage, error) {
	body, err := c.fetch(ctx, url)
	if err != nil {
		return nil, err
	}
	var head struct {
		Err  int    `json:"err"`
		Desc string `json:"desc"`
	}
	if err := json.Unmarshal(body, &head); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}
	if head.Err != 0 {
		return nil, &APIError{Err: head.Err, Desc: head.Desc, Raw: body}
	}
	return body, nil
}

func sha1Hex(s string) string {
	h := sha1.Sum([]byte(s)) //nolint:gosec
	return hex.EncodeToString(h[:])
}

func saltMs() string {
	return strconv.FormatInt(time.Now().UnixMilli(), 10)
}
