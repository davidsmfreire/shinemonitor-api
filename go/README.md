# ShineMonitor API in Go

Go client for the ShineMonitor REST API (`api.shinemonitor.com`),
sibling of the Python and Rust clients in this repo. Method surface is
generated from `spec/endpoints.yaml`; signing and login are
handwritten in `client.go`.

```sh
go get github.com/davidsmfreire/shinemonitor-api/go@latest
```

## Usage

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    shinemonitor "github.com/davidsmfreire/shinemonitor-api/go"
)

func main() {
    c := shinemonitor.New()

    ctx := context.Background()
    if err := c.Login(ctx, "user", "pass"); err != nil {
        log.Fatal(err)
    }

    raw, err := c.QueryAccountInfo(ctx)
    if err != nil {
        log.Fatal(err)
    }
    var resp struct {
        Dat json.RawMessage `json:"dat"`
    }
    if err := json.Unmarshal(raw, &resp); err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(resp.Dat))
}
```

Every generated method takes `ctx` as its first argument. Returns
`(json.RawMessage, error)` — caller decides the response shape.

## Constructor options

```go
c := shinemonitor.New(
    shinemonitor.WithBaseURL("http://your-host/public/"),
    shinemonitor.WithSuffixContext("&_app_id_=..."),
    shinemonitor.WithCompanyKey("..."),
    shinemonitor.WithHTTP(&http.Client{Timeout: 30 * time.Second}),
)
```

Defaults pin the request fingerprint to the WatchPower Android app
(`WatchPowerSuffixContext`, `WatchPowerCompanyKey`). Override only if
talking to a different vendor app.

## Errors

Non-zero `err` field from the vendor surfaces as `*APIError`:

```go
var apiErr *shinemonitor.APIError
if errors.As(err, &apiErr) {
    if apiErr.IsAuth() {
        // re-login
    }
    fmt.Printf("err=0x%04X desc=%s\n", apiErr.Err, apiErr.Desc)
}
```

`IsAuth()` returns true for the chapter-2 auth-band codes — the same
set the Python and Rust clients flag for re-login.

## Testing

`go test ./...` from this directory. Tests spawn the Python mock
server (`shinemonitor-mock`) — set `SHINEMONITOR_MOCK_PYTHON` to a
Python interpreter that has it installed, or run `uv sync` in
`../python/` first.
