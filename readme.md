# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review through a minimal, Python-based stack.

## Design

The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases. A `[gemini]` section supplies the `api_key` used for the model along with an optional `model` entry; the latter defaults to `gemini-3.1-flash-lite-preview`. Example:

```toml
[gemini]
api_key = "mysecretkey"
model = "gemini-3.1-flash-lite-preview"

[context]
prompt = "You are a helpful agent for Acme College."
```

The TOML parser uses Python’s built‑in `tomllib`, so Python 3.11 or newer is
required. To guarantee long-term stability and eliminate dependency churn,
the application avoids high-level LLM frameworks in favor of direct REST calls
via Python's standard urllib library. The default integration targets
Google's Gemini API using the configured API key. Institutional knowledge is managed through a system
prompt, either embedded or supplied via TOML, removing the complexity of vector databases and custom search tools. This
approach culminates in a cohesive application that serves a lightweight
JavaScript widget to prospective students and a secure Google
Auth-protected interface for administrators, maintaining a strict, minimal
dependency footprint.
