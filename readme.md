# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review.

## Demo

![Demo Video](demo.gif)

## Design

The system is built on a minimalist architecture, utilizing FastAPI and SQLite to provide zero-configuration deployment on lightweight Linux VMs without the overhead of external databases.

## Configuration

Add a `[gemini]` section with your API key and optional model (defaults to `gemini-3.1-flash-lite-preview`):

```toml
[gemini]
api_key = "mysecretkey"
model = "gemini-3.1-flash-lite-preview"
```

You can also include a `[context]` section to provide a default prompt for the agent:

```toml
[context]
prompt = "You are a helpful agent for Acme College."
```

To enable a secure administrative dashboard, add a `[google]` section with a `client_id` to use for authentication.

```toml
[google]
client_id = "your-google-client-id.apps.googleusercontent.com"
```

To restrict dashboard access to specific addresses, add a `[roles]` section with an `admins` list. When `admins` is non-empty, only addresses listed will be allowed access.

```toml
[roles]
admins = ["alice@example.com", "bob@example.com"]
```

## Usage

1. Set API keys, system prompt, and authorized users in `darkglass.toml`
2. Run `uvx darkglass` or `pipx darkglass` to launch production server
3. Use the demo page to test the config: <http://localhost:8000/static/demo.html>
4. Update reverse proxy configs as required to route requests to darkglass.
5. Add the following snippet to your site, replacing the URL based on your chosen production endpoint:

```html
<script src="https://darkglass.example.com/static/webchat.js"></script>
```

## Add to arbitrary site via dev tools

```js
let darkglass = document.createElement('script')
darkglass.src = 'http://localhost:8000/static/webchat.js'
darkglass.defer = true
document.body.appendChild(darkglass)
```
