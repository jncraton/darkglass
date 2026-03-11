# Darkglass

[![Lint](https://github.com/jncraton/college-agent/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/college-agent/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/test.yml)
[![Release](https://github.com/jncraton/college-agent/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/college-agent/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/darkglass.svg)](https://pypi.org/project/darkglass/)

Darkglass is a lightweight, embeddable chatbot designed for small colleges, providing prospective students with automated responses while logging interactions for administrative review through a minimal, Python-based stack.

## Design

The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases. To guarantee long-term stability and eliminate dependency churn, the application avoids high-level LLM frameworks in favor of direct REST calls via Python's standard urllib library. The default integration targets Google's Gemini API using a simple API key (GEMINI_API_KEY) and an optional GEMINI_API_URL override. Institutional knowledge is managed through embedded system prompts and native model inference capabilities, removing the complexity of vector databases and custom search tools. This approach culminates in a cohesive application that serves a lightweight JavaScript widget to prospective students and a secure Google Auth-protected interface for administrators, maintaining a strict, minimal dependency footprint.
