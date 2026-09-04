# Everything Soil — Database Specification

This document describes the initial domain model. Exact field types and implementation details may evolve after inspecting the existing Django project.

## 1. Account Domain

### User
Custom Django user.

Core fields:
- email
- username if required by implementation
- first/last name if needed
- active status
- staff status
- timestamps

Authentication provider details should be compatible with the selected Google OAuth package.

### Profile

Relationship:
`User 1 — 1 Profile`

Suggested fields:
- user
- display_name
- bio
- profile_image
- city
- country
- preferred_language
- created_at
- updated_at

### Interest

Suggested fields:
- name
- slug
- description
- icon
- is_active

Relationship:
`Profile M — M Interest`

Initial interests:
- Soil
- Natural Farming
- Meditation
- Yoga
- Nature
- Water
- Traditional Knowledge
- Panja Bootham
- Photography
- Volunteering
- Research

---

## 2. Panja Bootham Domain

### Element

Five initial records:
- Earth
- Water
- Fire
- Air
- Space

Suggested fields:
- key
- name
- slug
- description
- image
- order
- active status

### ElementTranslation

If multilingual content is implemented through translations:
- element
- language
- name
- description
- content

Constraint:
`unique(element, language)`

---

## 3. Content Domain

### Category
- name
- slug
- description
- active

### Tag
- name
- slug

### Article
- title
- slug
- excerpt
- content
- cover_image
- author
- category
- tags
- elements
- interests
- status
- published_at
- created_at
- updated_at

### Story

User-generated content.

- author
- title
- content
- image
- status
- created_at
- moderated_by
- moderated_at

Status:
- pending
- approved
- rejected

Never automatically publish unmoderated user stories.

### Resource

Optional future model for:
- PDFs
- books
- external resources
- research material

---

## 4. Practice Domain

### Practice
- element
- title
- slug
- description
- duration_minutes
- instructions
- image
- active

### PracticeCompletion
- user
- practice
- completed_at
- notes

Recommended constraint:
Do not enforce uniqueness unless product requirements explicitly require one completion per practice. Repeated practices are expected.

---

## 5. Experience Domain

### Experience

Represents a type of experience, not a specific date.

Types:
- meditation
- yoga
- soil
- nature
- farm
- panja_bootham
- retreat

Fields:
- type
- title
- slug
- description
- duration
- image
- active

Example:
`Earth & Soil Experience`

can have many scheduled Events.

---

## 6. Event Domain

### Event
- experience
- title
- slug
- description
- start_at
- end_at
- location
- capacity
- registration_required
- registration_fee
- image
- published

### EventRegistration
- event
- user
- status
- registered_at

Statuses:
- registered
- cancelled
- attended
- no_show

Constraint:
`unique(event, user)`

### EventFeedback
Future optional model:
- event
- user
- rating
- feedback
- created_at

---

## 7. Community Domain

### Circle
Examples:
- Soil Circle
- Meditation Circle
- Farming Circle
- Nature Circle
- Water Circle
- Knowledge Circle
- Volunteer Circle

Fields:
- name
- slug
- description
- interests
- image
- public/private
- active
- created_at

### CircleMembership
- circle
- user
- role
- joined_at

Roles:
- member
- coordinator
- moderator

Recommended constraint:
`unique(circle, user)`

### DiscussionPost

Future MVP+ model:
- circle
- author
- content
- created_at
- updated_at
- status

Moderation may be required.

---

## 8. Volunteer Domain

### VolunteerProfile
- user
- skills
- availability
- motivation
- approved
- created_at

### VolunteerOpportunity
- title
- slug
- description
- skills_required
- start_date
- end_date
- active

### VolunteerApplication
- user
- opportunity
- status
- created_at

Statuses:
- pending
- approved
- rejected
- withdrawn

### VolunteerParticipation
- user
- opportunity
- date
- hours
- notes

Volunteer hours can be aggregated for Impact metrics.

---

## 9. Project Domain

### Project
- title
- slug
- description
- image
- goal_amount
- start_date
- target_date
- status
- active

Examples:
- Soil Restoration
- Native Tree Garden
- Water Restoration
- Meditation Space
- Panja Bootha Pathway

### ProjectUpdate
- project
- title
- content
- image
- created_at
- author

---

## 10. Contribution Domain

### Contribution
- user, nullable
- project, nullable
- amount
- currency
- status
- payment_provider
- payment_reference
- receipt_reference
- created_at

Statuses:
- pending
- success
- failed
- refunded

Payment integration must be implemented only after selecting and configuring the appropriate provider.

Never trust client-submitted payment success status. Verify server-side with the provider.

---

## 11. Visit Domain

### VisitRequest
- user
- visit_date
- number_of_people
- purpose
- notes
- status
- created_at

Statuses:
- pending
- confirmed
- cancelled
- completed

Future extensions:
- overnight stay
- retreat booking
- accommodation
- meal preference
- school/group visit

---

## 12. Notification Domain

### Notification
- user
- type
- title
- message
- URL
- read_at
- created_at

Potential types:
- event reminder
- event update
- circle announcement
- volunteer update
- project update
- story moderation result
- contribution receipt

---

## 13. Analytics / Impact

Do not initially store derived counts redundantly.

Examples:

Volunteer hours:
`SUM(VolunteerParticipation.hours)`

Events attended:
`COUNT(EventRegistration where status='attended')`

Circles:
`COUNT(CircleMembership)`

Practices:
`COUNT(PracticeCompletion)`

Project contribution totals:
`SUM(Contribution.amount where status='success')`

Later, materialized summaries or cached counters may be introduced if performance requires them.

---

## 14. Key Relationship Summary

```text
User
 ├── Profile
 │     └── Interests
 │
 ├── EventRegistration
 ├── PracticeCompletion
 ├── CircleMembership
 ├── VolunteerProfile
 ├── VolunteerApplication
 ├── VolunteerParticipation
 ├── Story
 ├── VisitRequest
 └── Contribution

Element
 ├── Article
 ├── Practice
 └── Experience

Experience
 └── Event
       └── EventRegistration

Circle
 └── CircleMembership

VolunteerOpportunity
 ├── VolunteerApplication
 └── VolunteerParticipation

Project
 ├── ProjectUpdate
 └── Contribution
```

---

## 15. Important Database Rules

- Use foreign keys with intentional `on_delete` behavior.
- Use unique constraints where duplicate relationships are invalid.
- Use indexes on public slugs and common filtering fields.
- Use timezone-aware datetimes.
- Use `DecimalField` for money.
- Never use floating point for monetary amounts.
- Avoid hard deletion of financial records.
- Preserve contribution/payment audit information.
- Use soft-delete/status patterns for content that should remain historically traceable.
