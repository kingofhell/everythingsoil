---
trigger: always_on
---

# Everything Soil — Antigravity Workspace Rules

You are implementing the Everything Soil project.

Before changing code, read:

- `docs/PROJECT.md`
- `docs/ARCHITECTURE.md`
- `docs/DATABASE.md`
- `docs/USER_FLOWS.md`
- `docs/WEBSITE.md`
- `docs/ROADMAP.md`

## General Rules

1. Inspect the existing code before making assumptions.
2. Do not rewrite working code unnecessarily.
3. Do not implement features outside the current requested task.
4. Do not skip documentation because a feature appears simple.
5. Preserve backward compatibility unless a migration is intentionally planned.
6. Explain important architectural decisions in the final response.

## Django Rules

1. Use the project's custom User model.
2. Keep business logic out of templates.
3. Prefer reusable services for complex workflows.
4. Use model constraints for data integrity.
5. Use indexes for common query paths.
6. Use `select_related` and `prefetch_related` appropriately.
7. Never edit an already-applied migration. Create a new migration.
8. Do not use floating-point fields for money.
9. Use timezone-aware datetimes.
10. Use slugs for public content URLs.

## Security

1. Never expose secrets.
2. Never commit `.env` files containing secrets.
3. Use environment variables for credentials.
4. Preserve CSRF protection.
5. Validate all user input.
6. Check authorization on every protected mutation.
7. Never trust client-side payment success.
8. Verify payment status server-side.
9. Do not expose private user information.
10. Moderate user-generated content.

## Frontend

1. Use Bootstrap 5.
2. Mobile-first.
3. Prefer server-rendered Django templates.
4. Use HTMX for small interactive operations where useful.
5. Avoid introducing React unless explicitly requested.
6. Build reusable template components.
7. Avoid unnecessary animations.
8. Optimize images.
9. Support readable Tamil typography.

## Product Principles

Everything Soil is not a conventional temple website.

The platform should communicate:

- Soil
- Nature
- Five Elements
- Meditation
- Yoga
- Ecology
- Community
- Service
- Inner observation

Do not make unsupported medical, scientific, religious or supernatural claims.

The philosophy should invite people to observe and experience rather than force belief.

## UX

Preferred journey:

Discover
→ Learn
→ Practice
→ Experience
→ Visit
→ Join
→ Participate
→ Contribute
→ Share

Do not make donation the dominant experience.

## AI Agent Workflow

Before implementing a task:

1. Read relevant documentation.
2. Inspect affected files.
3. Identify dependencies.
4. Explain the planned changes briefly.
5. Implement the smallest coherent change.
6. Run migrations if required.
7. Run relevant tests.
8. Run Django system checks.
9. Inspect affected URLs/templates.
10. Summarize files changed and tests performed.

Do not silently change architecture.

If a requested feature conflicts with the project specification, stop and explain the conflict before making a large architectural change.

## Current Development Principle

Implement one roadmap phase at a time.

Do not build future functionality merely because the database could support it.
