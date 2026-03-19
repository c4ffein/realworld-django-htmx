# realworld-django-htmx
**WIP: Porting from Django Ninja API to Django + HTMX fullstack, assisted by AI and the RealWorld e2e spec suite**

Django + HTMX implementation of the RealWorld spec.

## Rules

- **NEVER raise timeouts** without asking first. We build fast software. If a test times out, the code is broken — fix the code, don't raise the timeout. Raising timeouts destroys the feedback loop.

## Before finishing

Run `make verify` (lint + type-check + fast tests) and fix any issues.

## Commands

- `make sync` - install dependencies
- `make verify` - lint, type-check, test
- `make test-django-fast` - fast tests only
