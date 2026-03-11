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

```toml
[gemini]
api_key = "mysecretkey"
model = "gemini-3.1-flash-lite-preview"

[context]
prompt = "You are a helpful agent for Acme College."
```

## Add to arbitrary site via dev tools:

```js
let darkglass = document.createElement('script')
darkglass.src = 'http://localhost:8000/static/widget.js'
darkglass.defer = true
document.body.appendChild(darkglass)
```
