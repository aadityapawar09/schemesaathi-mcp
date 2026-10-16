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


## Example requests to try

- Find schemes related to farming.
- Explain PM-KISAN in simple words and link to the official portal.
- Prepare a document checklist for Kisan Credit Card.
- I am a traditional artisan. What details should I check for PM Vishwakarma?
- Help me identify what information is missing before I check eligibility.

## Limitations and responsible use

- This project searches only the bundled catalog; it does not query a live government database.
- Eligibility checks are preliminary and keyword-based, not official decisions.
- It does not submit applications, verify identity, or guarantee benefits.
- Never share passwords or OTPs with agents or through this tool.
- Check the official scheme portal or an authorized office for current rules.

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

## License

This project is provided for educational use. Add a license file if you decide how you want others to reuse your code.
