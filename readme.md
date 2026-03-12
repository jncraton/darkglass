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

# Optional Google authentication

An `[google]` section may be added when you wish to enable an administrative
interface protected by Google accounts.  Only the `client_id` value is
required.  The login flow takes place entirely in the browser: the static
admin page renders a Google sign‑in button, obtains an ID token, and then
sends that token as a bearer credential with any request to `/logs` or other
protected APIs.  The server verifies the token against Google's
``/tokeninfo`` endpoint and checks the email address against the
optional `ADMIN_EMAILS` whitelist.  The `client_secret` value is unused by the
server but may be provided for completeness or testing purposes.

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
