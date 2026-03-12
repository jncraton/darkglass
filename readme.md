# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review.

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

## Demo

1. Install the package
2. Set configuration
3. Run `make serve` and view http://localhost:8000/static/index.html

## Add to arbitrary site via dev tools

```js
let darkglass = document.createElement('script')
darkglass.src = 'http://localhost:8000/static/webchat.js'
darkglass.defer = true
document.body.appendChild(darkglass)
```
