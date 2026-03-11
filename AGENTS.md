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

- `gemini_api_key` – API key used by the model (overrides the
  `GEMINI_API_KEY` environment variable)
- `prompt` – system prompt describing institutional knowledge (falls
  back to the `SYSTEM_PROMPT` environment variable or a built-in default)

Values can still be supplied via environment variables as before. The
file is parsed once at import time, so tests and the application itself
load the configuration on start-up.

Key environment variables

- `GEMINI_API_KEY` – required to make model requests (returns a placeholder
  string if unset).
- `GEMINI_API_URL` – override the default Gemini endpoint for testing.
- `DB_PATH` – path to the SQLite database file (defaults to `data.db`).
- `ADMIN_EMAILS` – comma‑separated list of permitted admin addresses.
- `COOKIE_SECRET` – secret used to sign session cookies.
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `OAUTH_REDIRECT` – for Google
  OAuth to access `/admin` and `/logs`.

## Running the service

Use `make serve` to start a development server (FastAPI uvicorn) on
port 8000. The chat widget can be embedded by including
`<script src="/static/widget.js"></script>` on any page; samples are
in `index.html` and `static/admin.html`.

## Testing

Run tests using `make test` which installs dependencies in a virtual
environment, runs pytest, and exercises both API and browser tests.

## Formatting

Format code using `make format` which runs Prettier on JS/HTML and
black on Python.
