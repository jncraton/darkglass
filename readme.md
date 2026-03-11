# College Agent

This application serves as a lightweight, embeddable chatbot for small Christian institutions, providing prospective students with automated responses while logging interactions for administrative review through a minimal, Python-based stack.

## Design

The system is built on a minimalist "bare-metal" architecture, utilizing FastAPI and SQLite to ensure zero-configuration deployment on lightweight Linux VMs without the overhead of external databases. To guarantee long-term stability and eliminate dependency churn, the application avoids high-level LLM frameworks in favor of direct REST calls via Python's standard urllib library. Institutional knowledge is managed through embedded system prompts and native model inference capabilities, removing the complexity of vector databases and custom search tools. This approach culminates in a cohesive application that serves a lightweight JavaScript widget to prospective students and a secure Google Auth-protected interface for administrators, maintaining a strict, minimal dependency footprint. 
      
