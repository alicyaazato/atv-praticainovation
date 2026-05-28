## Why

Students need to manage their academic subjects (disciplinas) within EduTrack AI, but there is no formal, spec-driven contract for the CRUD endpoints that govern subject creation, retrieval, update, and deletion. Formalizing these endpoints ensures consistent access control — every user must only read and modify their own subjects — and establishes a clear behavioral contract for the Streamlit frontend to integrate against.

## What Changes

- **POST `/subjects`** — Create a new subject, auto-assigning `owner_id` from the authenticated user's JWT token.
- **GET `/subjects/my`** — List all subjects owned by the authenticated user, with pagination and filtering.
- **GET `/subjects/{id}`** — Retrieve a single subject; returns 403 if the authenticated user is not the owner.
- **PATCH `/subjects/{id}`** — Partially update a subject; enforces owner-only write access and auto-updates `updated_at`.
- **DELETE `/subjects/{id}`** — Soft-delete a subject (sets `is_active = false`); enforces owner-only access.

All endpoints require a valid Bearer JWT token (`auth = "user"`). No endpoint exposes subjects belonging to other users.

## Capabilities

### New Capabilities

- `subjects-crud`: Full lifecycle management of subject records for the authenticated user — create, list, read, update, and soft-delete — with ownership-scoped access control enforced on every operation.

### Modified Capabilities

<!-- No existing spec-level capabilities are changing. -->

## Impact

- **Xano backend** (`atv2Lab/apis/subjects/`): Five endpoint functions implementing the CRUD operations with RBAC and audit logging via triggers on the `subject` table.
- **Streamlit frontend** (`app.py`, `pages/`): The "Disciplinas" page will consume these endpoints once the Xano integration is wired up.
- **Authentication**: All endpoints depend on Xano's JWT auth system (`$auth.user_id` context variable).
- **Database**: The `subject` table with `owner_id` and `is_active` fields is the persistence layer; no schema changes required.
