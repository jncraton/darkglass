# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review through a minimal, Python-based stack.

## Design

The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases. Configuration happens via environment variables or an optional `darkglass.toml` file placed in the working directory; supported TOML keys are `gemini_api_key` and `prompt`. For example:
The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases. Configuration happens via environment variables or an optional `darkglass.toml` file placed in the working directory; supported TOML keys are `gemini_api_key` and `prompt`.  For example:

```toml
gemini_api_key = "mysecretkey"
prompt = "You are a helpful agent for Acme College."
```

The TOML parser uses Python’s built‑in `tomllib`, so Python 3.11 or newer is
required. To guarantee long-term stability and eliminate dependency churn,
the application avoids high-level LLM frameworks in favor of direct REST calls
via Python's standard urllib library. The default integration targets
Google's Gemini API using the configured API key and an optional
GEMINI_API_URL override. Institutional knowledge is managed through a system
prompt, either embedded, supplied via TOML, or set in the environment,
removing the complexity of vector databases and custom search tools. This
approach culminates in a cohesive application that serves a lightweight
JavaScript widget to prospective students and a secure Google
Auth-protected interface for administrators, maintaining a strict, minimal
dependency footprint.
