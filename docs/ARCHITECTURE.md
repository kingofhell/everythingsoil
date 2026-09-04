# Everything Soil — Technical Architecture

## 1. Architecture Style

Use a modular Django monolith.

Do not introduce microservices unless a demonstrated technical requirement exists.

Use PostgreSQL as the production database.

Use Django Templates + Bootstrap 5 as the primary frontend.

Use HTMX for lightweight interactive functionality where it improves UX without requiring a SPA.

## 2. Django Apps

Recommended applications:

- `core` — site-wide functionality and homepage
- `accounts` — custom user, profile, authentication and interests
- `elements` — Panja Bootham
- `content` — articles, stories, categories, tags and resources
- `experiences` — meditation, yoga, nature, farm and other experiences
- `events` — scheduled events and registrations
- `community` — Circles and memberships
- `volunteers` — volunteer profiles, opportunities and applications
- `projects` — ecological/development projects and updates
- `contributions` — financial contributions and payment records
- `visits` — physical-center visit requests
- `notifications` — notifications and communication preferences
- `analytics` — meaningful product and impact metrics

## 3. Core Engineering Principles

1. Use a custom Django User model from the beginning.
2. Keep business logic out of templates.
3. Keep views thin where practical.
4. Use reusable services for complex business operations.
5. Use model constraints for important invariants.
6. Use database indexes for common lookup paths.
7. Use `select_related` and `prefetch_related` where appropriate.
8. Use slugs for public content URLs.
9. Never modify an already-applied migration; create a new migration.
10. Never commit secrets.
11. Store secrets in environment variables.
12. Never disable CSRF/security checks merely to make development easier.
13. Validate all user-submitted content.
14. Moderate user-generated stories before publication.
15. Keep public content SEO-friendly.
16. Build mobile-first.
17. Prefer server-rendered HTML.
18. Use progressive enhancement rather than unnecessary frontend complexity.

## 4. Authentication

Google Sign-In should be the primary convenient authentication method.

Anonymous users should be able to browse most public content.

Authentication should be required for actions such as:

- Event registration
- Joining a Circle
- Saving content
- Completing a Journey practice
- Volunteer application
- Story submission
- Contributions where identity is needed
- Profile management

Do not force authentication for ordinary reading.

## 5. Authorization

Use three layers:

### Authentication
- Anonymous
- Authenticated

### Django permissions
Examples:
- `can_manage_events`
- `can_manage_content`
- `can_manage_projects`
- `can_manage_volunteers`
- `can_moderate_stories`

### Application roles
Examples:
- Member
- Volunteer
- Circle Coordinator
- Event Coordinator
- Content Contributor
- Facilitator
- Project Coordinator
- Administrator

A user may have multiple roles.

Do not use Django Groups as a replacement for domain objects such as Circles.

## 6. Template Structure

Recommended:

```text
templates/
├── base.html
├── components/
│   ├── navbar.html
│   ├── footer.html
│   ├── hero.html
│   ├── element-card.html
│   ├── article-card.html
│   ├── event-card.html
│   ├── experience-card.html
│   ├── project-card.html
│   ├── circle-card.html
│   ├── story-card.html
│   ├── progress-bar.html
│   └── user-avatar.html
└── pages/
```

## 7. Static Assets

Use:

```text
static/
├── css/
├── js/
├── images/
└── icons/
```

Media uploaded by users/admins should be kept separate from static assets.

## 8. URL Principles

Public URLs should be:
- Human readable
- Stable
- Slug-based
- SEO-friendly
- Language-aware where multilingual routing is implemented

Recommended patterns are documented in `WEBSITE.md`.

## 9. Multilingual Content

Prefer a translation model for substantial content instead of adding `*_en` and `*_ta` fields to every model.

Conceptually:

```text
Article
  ├── ArticleTranslation(en)
  └── ArticleTranslation(ta)
```

The same principle can be used for other editorial content where appropriate.

## 10. HTMX

Good use cases:
- Join Circle
- Leave Circle
- Register for event
- Save article
- Complete practice
- Filter content
- Load additional content
- Lightweight moderation actions

Avoid using HTMX for functionality that would be simpler as a normal Django request.

## 11. Testing

Every feature should have appropriate tests.

Minimum expectations:
- Model tests for important constraints
- View tests for critical workflows
- Permission tests
- Registration tests
- Contribution/payment tests before production use
- Form validation tests

Before completing a task:
- Run Django system checks
- Run relevant tests
- Check migrations
- Check affected URLs
- Check mobile layout where practical
