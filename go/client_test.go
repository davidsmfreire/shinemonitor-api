package shinemonitor

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// mockServer spawns the Python mock as a subprocess on a free port and
// returns its base URL. Cleanup terminates the process.
type mockServer struct {
	cmd *exec.Cmd
	URL string
}

func startMock(t *testing.T) *mockServer {
	t.Helper()
	python := os.Getenv("SHINEMONITOR_MOCK_PYTHON")
	if python == "" {
		// Repo layout: ../python/.venv/bin/python (created by `uv sync`).
		wd, err := os.Getwd()
		if err != nil {
			t.Fatal(err)
		}
		candidate := filepath.Join(wd, "..", "python", ".venv", "bin", "python")
		if _, err := os.Stat(candidate); err == nil {
			python = candidate
		} else {
			t.Skip("set SHINEMONITOR_MOCK_PYTHON or run `uv sync` in python/")
		}
	}

	cmd := exec.Command(python, "-m", "shinemonitor_mock", "--port", "0")
	cmd.Env = append(os.Environ(), "PYTHONUNBUFFERED=1")
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		t.Fatal(err)
	}
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		t.Fatal(err)
	}

	reader := bufio.NewReader(stdout)
	line, err := reader.ReadString('\n')
	if err != nil {
		_ = cmd.Process.Kill()
		t.Fatalf("read mock greeting: %v", err)
	}
	line = strings.TrimSpace(line)
	if !strings.HasPrefix(line, "LISTENING ") {
		_ = cmd.Process.Kill()
		t.Fatalf("unexpected mock greeting: %q", line)
	}
	url := strings.TrimSuffix(strings.TrimPrefix(line, "LISTENING "), "/")

	// Wait for socket to accept.
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		resp, err := http.Get(url + "/public/?action=__ping__") //nolint:gosec
		if err == nil {
			resp.Body.Close()
			break
		}
		time.Sleep(50 * time.Millisecond)
	}

	t.Cleanup(func() {
		_ = cmd.Process.Kill()
		_, _ = cmd.Process.Wait()
	})
	return &mockServer{cmd: cmd, URL: url}
}

func newTestClient(baseURL string) *Client {
	return New(
		WithBaseURL(baseURL+"/public/"),
		WithCompanyKey("test-company"),
		WithSuffixContext("&source=1&_app_client_=android&_app_id_=test.app&_app_version_=0.0.1"),
	)
}

const (
	fixtureUser = "demo-user"
	fixturePass = "demo-pass"
)

func TestLoginSuccess(t *testing.T) {
	srv := startMock(t)
	c := newTestClient(srv.URL)
	if err := c.Login(context.Background(), fixtureUser, fixturePass); err != nil {
		t.Fatalf("login: %v", err)
	}
	if c.AuthState() == nil || c.AuthState().Token != "tok-12345" {
		t.Fatalf("unexpected auth state: %+v", c.AuthState())
	}
}

func TestLoginBadPassword(t *testing.T) {
	srv := startMock(t)
	c := newTestClient(srv.URL)
	err := c.Login(context.Background(), fixtureUser, "wrong")
	if err == nil {
		t.Fatal("expected error")
	}
	var apiErr *APIError
	if !errors.As(err, &apiErr) {
		t.Fatalf("expected APIError, got %T: %v", err, err)
	}
	if apiErr.Err != 0x0010 {
		t.Fatalf("expected err=0x0010, got 0x%X", apiErr.Err)
	}
	if !apiErr.IsAuth() {
		t.Fatal("expected IsAuth() == true")
	}
}

func TestQueryAccountInfo(t *testing.T) {
	srv := startMock(t)
	c := newTestClient(srv.URL)
	if err := c.Login(context.Background(), fixtureUser, fixturePass); err != nil {
		t.Fatalf("login: %v", err)
	}
	raw, err := c.QueryAccountInfo(context.Background())
	if err != nil {
		t.Fatalf("QueryAccountInfo: %v", err)
	}
	var resp struct {
		Err int `json:"err"`
	}
	if err := json.Unmarshal(raw, &resp); err != nil {
		t.Fatal(err)
	}
	if resp.Err != 0 {
		t.Fatalf("expected err=0, got %d", resp.Err)
	}
}

func TestQueryDeviceLastData(t *testing.T) {
	srv := startMock(t)
	c := newTestClient(srv.URL)
	if err := c.Login(context.Background(), fixtureUser, fixturePass); err != nil {
		t.Fatalf("login: %v", err)
	}
	// QueryDeviceLastData is a generated method — exercises a multi-arg path.
	raw, err := c.QueryDeviceLastData(context.Background(), "W0001234", 2451, 1, "9620230101001")
	if err != nil {
		t.Fatalf("QueryDeviceLastData: %v", err)
	}
	if !strings.Contains(string(raw), `"err": 0`) && !strings.Contains(string(raw), `"err":0`) {
		t.Fatalf("unexpected response: %s", raw)
	}
}

func TestUnauthedCallReturnsError(t *testing.T) {
	c := newTestClient("http://unused")
	_, err := c.QueryAccountInfo(context.Background())
	if err == nil {
		t.Fatal("expected error")
	}
	var apiErr *APIError
	if !errors.As(err, &apiErr) {
		t.Fatalf("expected APIError, got %T", err)
	}
	if apiErr.Err != -1 {
		t.Fatalf("unexpected err code: %d", apiErr.Err)
	}
}
