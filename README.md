# SchemeSaathi MCP

SchemeSaathi is a small Python MCP server that helps people explore a starter catalog of Indian government schemes. It is designed as a learning and portfolio project using FastMCP and `uv`.

## What it can do

### Tools
- `search_schemes` — search the local catalog by keyword or category.
- `get_scheme_details` — view a scheme summary, possible beneficiaries, documents to check, and its official source.
- `check_eligibility` — create a preliminary checklist based on a short description. It does not make an official decision.
- `prepare_application_checklist` — prepare a general list of documents and steps to verify.

### Resources
- `schemesaathi://guide` — how to use the server and its limitations.
- `schemesaathi://schemes` — the local catalog as JSON.
- `schemesaathi://categories` — categories in the catalog.

### Prompts
- `find_schemes_for_me`
- `explain_scheme`
- `check_my_eligibility`
- `prepare_my_application`

## Included catalog

The starter catalog contains examples for PM-KISAN, PMFBY, Kisan Credit Card, AB PM-JAY, and PM Vishwakarma. The catalog is intentionally small and local; it is not a complete list of Indian government schemes.

Official links are included in `schemes.json`. Rules, application windows, required documents, and state-level availability can change, so check the official source before acting.


## Project structure

```text
schemesaathi-mcp/
├── server.py
├── schemes.json
├── pyproject.toml
├── README.md
└── tests/
    └── test_server.py
```

