// ReadyStack PostHog (CE): the Caddy build entrypoint (xcaddy pattern, as product-kits/caddy). This main module depends
// on github.com/caddyserver/caddy/v2 at the pinned release; `caddy version` reports it from the build info.
package main

import (
	caddycmd "github.com/caddyserver/caddy/v2/cmd"

	_ "github.com/caddyserver/caddy/v2/modules/standard"
)

func main() {
	caddycmd.Main()
}
