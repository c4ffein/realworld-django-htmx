# realworld-django-htmx
**Django + HTMX fullstack implementation of the RealWorld spec — no API, no SPA**

## Rules

- **NEVER raise timeouts** without asking first. We build fast software. If a test times out, the code is broken — fix the code, don't raise the timeout. Raising timeouts destroys the feedback loop.

## Before finishing

Run `make verify` (lint + type-check + unit tests) and fix any issues.

## Commands

- `make sync` - install dependencies
- `make verify` - lint, type-check, unit tests
- `make e2e` - run Playwright e2e tests
