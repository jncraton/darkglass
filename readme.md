# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review.

## Design

The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases.

## Config

A `[gemini]` section supplies the `api_key` used for the model along with an optional `model` entry; the latter defaults to `gemini-3.1-flash-lite-preview`. Example:

````toml
[gemini]
api_key = "mysecretkey"
model = "gemini-3.1-flash-lite-preview"

[context]
prompt = "You are a helpful agent for Acme College."

## Demo

1. Install the package
2. Set configuration
3. Run `make serve` and view http://localhost:8000/static/index.html

## Optional Google authentication

An `[google]` section may be added when you wish to enable an administrative
interface protected by Google accounts.  Only the `client_id` value is
required.  A `[roles]` section may be added to list trusted addresses.  When the
`admins` list is non‑empty only the addresses contained therein will be
allowed to access the dashboard; the previous `ADMIN_EMAILS` mechanism is
overridden by the list.

```toml
[roles]
admins = ["alice@example.com", "bob@example.com"]
```


```toml
[google]
client_id = "your-google-client-id.apps.googleusercontent.com"
# client_secret may be present but is no longer required
client_secret = "your-secret"
````

````

## Add to arbitrary site via dev tools:

```js
let darkglass = document.createElement('script')
darkglass.src = 'http://localhost:8000/static/webchat.js'
darkglass.defer = true
document.body.appendChild(darkglass)
````
