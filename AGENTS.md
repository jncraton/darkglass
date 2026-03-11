## Overview

Darkglass is a tiny FastAPI application that provides an embeddable chat widget
for prospective students and an admin dashboard for reviewing logged
interactions. The service calls a language model (defaulting to Google's
Gemini API) via plain REST, stores exchanges in a local SQLite database,
and uses a minimal session system with optional Google OAuth for admin login.
The Python package lives under `darkglass/` with the main logic in
`darkglass/main.py`. Static assets (`widget.js` and `admin.html`) are served
from the `static/` directory and the simple landing page is `index.html`.

Configuration

The package now supports an optional `darkglass.toml` file in the
working directory. When present the two supported keys are

- `gemini_api_key` – API key used by the model
- `prompt` – system prompt describing institutional knowledge (defaults to
  an embedded string if not provided)

All other values are hard‑coded sensible defaults; there is no
longer any support for configuration via environment variables. Administrative
email restrictions, cookie secrets, OAuth client IDs and URLs may be
adjusted by editing the source, but typical deployments simply run with
no admin or OAuth features enabled and the built‑in defaults. Database
storage is always `data.db` in the working directory.

## Testing

Run tests using `make test` which installs dependencies in a virtual
environment, runs pytest, and exercises both API and browser tests.

## Formatting

Format code using `make format` which runs Prettier on JS/HTML and
black on Python.

## Style

Never comment code. Use docstrings, but only for examples run via doctest.
