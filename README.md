# Swim Results Database

Private LAN-only application for collecting, storing and presenting swimming
competition results, primarily from Swimify.

## Governance and ownership

This repository owns application behavior and domain logic for Swim Results DB:

- Swimify data acquisition and import logic;
- PostgreSQL data model and migrations;
- athlete/profile selection;
- result comparison and statistics;
- web application and UI;
- application-level validation and tests.

Hosting and operation are owned by
`SicOmen-HS/hosting-lab-infrastructure`, including Compose/runtime placement,
Caddy/LAN routing, host secrets, backup/restore and deployment procedures.

At the start of substantive work, follow `.ai-governance/project.json` and the
current canonical Minimal Governance v2 process. This repository is governance
adopted but is intentionally not Queue-onboarded at this stage.

## Product direction

The application should remain small and easy to operate. Prefer the existing
PostgreSQL database and Python code, a small Python web application, and a
lightweight server-rendered/mobile-friendly frontend unless a stronger need is
proven.

The intended user experience is a personal sports-results page rather than an
administration dashboard.

## Privacy and security

- LAN-only; no public exposure without a separate approved plan.
- Do not commit or expose database credentials, Swimify secrets or `.env`
  contents.
- Secrets must remain server-side and must never be sent to the frontend.
- Store and display only the personal data needed for competition results.
- Comparisons with other swimmers should prefer result statistics and ranking
  rather than building unnecessary profiles of other children or participants.
- UI-triggered imports must use bounded application logic; the web application
  must never expose arbitrary shell or Docker execution.

## Current code

The existing Python importer uses:

- Swimify GraphQL;
- PostgreSQL via `psycopg2`;
- `HASURA_PUBLIC_SECRET_KEY`;
- a manually supplied Swimify competition UUID.

Primary source files currently include:

- `main.py` — manual import entry point;
- `scraper.py` — Swimify competition/result queries;
- `graphql_client.py` — GraphQL transport;
- `database.py` — PostgreSQL persistence;
- `config.py` — environment-backed configuration.

## Task routing

| Task | Start with |
| --- | --- |
| Governance/bootstrap | `.ai-governance/project.json`, then this README |
| Scraper/import logic | `scraper.py`, `graphql_client.py`, `main.py` |
| Database/schema | `database.py`, then versioned migrations once introduced |
| Web/UI | application web entry point/templates/static files once introduced |
| Runtime, Compose, Caddy, backup or deployment | `SicOmen-HS/hosting-lab-infrastructure` |

## Development rules

- Preserve stable Swimify identifiers where available; do not key domain logic
  on display names when a durable competitor or competition identifier exists.
- Import operations must be idempotent or explicitly detect duplicates.
- Network requests require bounded timeouts and useful error handling.
- Database schema changes must become reproducible through version-controlled
  schema/migrations before relying on new fields in the UI.
- Do not make destructive database changes without fresh runtime evidence and a
  rollback/backup disposition.
- Prefer focused tests and queries that do not print secrets or unnecessary
  participant data.

## Local setup

Install packages:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to a local `.env` and provide environment-specific
credentials outside Git. Do not commit the resulting `.env`.
