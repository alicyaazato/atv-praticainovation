## Context

EduTrack AI is a Xano + Streamlit application for academic tracking. The backend runs on Xano (instance `x8ki-letl-twmt`, workspace `edutrack-ai`), which provides a PostgreSQL database, a built-in JWT auth system, and a XanoScript runtime for defining API endpoints.

The `subject` table already exists with 14 fields including `owner_id` (FK → users), `is_active` (soft-delete flag), and `account_id` (multi-tenant context). Five CRUD endpoint stubs exist in `atv2Lab/apis/subjects/`. This design formalizes the behavioral contract so the Streamlit "Disciplinas" frontend and any future consumers have a clear, testable specification to integrate against.

## Goals / Non-Goals

**Goals:**
- Define the exact request/response contract for all 5 subject endpoints.
- Enforce user-scoped data access: authenticated users can only read and write their own subjects.
- Support partial updates (PATCH semantics) and non-destructive deletion (soft-delete via `is_active = false`).
- Expose pagination and basic filtering on the list endpoint.

**Non-Goals:**
- Admin or cross-user subject access (out of scope for this change).
- Hard-delete of subject records.
- Bulk operations (create/update/delete multiple subjects in one call).
- Subject sharing or collaboration between users.

## Decisions

### D1 — Owner enforcement via `$auth.user_id`, not query parameter

Every endpoint resolves the owner from the JWT token (`$auth.user_id`) rather than accepting `user_id` as an input parameter.

**Why**: Prevents horizontal privilege escalation. A caller cannot supply another user's ID to access their records. This is the standard pattern already used in `members_accounts` and `event_logs` endpoints.

**Alternative considered**: Accept `user_id` in the request body and validate it server-side against `$auth.user_id`. Rejected — adds complexity with no benefit; the token already carries the identity.

---

### D2 — Soft-delete instead of hard-delete

DELETE sets `is_active = false` and `updated_at = now()` rather than removing the row.

**Why**: Preserves referential integrity with `academic_tasks` and `event_logs` tables that reference `subject.id`. Enables auditing and potential restore flows. Consistent with the existing `is_active` field already on the table.

**Alternative considered**: Hard-delete with cascading FK deletes. Rejected — would destroy audit trail and break historical task records.

---

### D3 — PATCH for partial updates, no PUT

Only `PATCH /subjects/{id}` is exposed; there is no `PUT` endpoint.

**Why**: Subjects have many optional fields. Requiring clients to send a complete representation on every update is fragile and leads to accidental overwrites of fields the client didn't intend to change.

---

### D4 — Separate list route (`/subjects/my`) instead of query-param filter on `/subjects`

The list endpoint is `/subjects/my` rather than `GET /subjects?owner=me`.

**Why**: Xano routes are matched by path prefix. A generic `/subjects` GET would conflict with `/subjects/{id}`. The `/my` suffix makes the ownership scope explicit and removes the need for a query-parameter filter for the most common case.

---

### D5 — Audit trail via database triggers, not endpoint logic

Writes to `event_logs` are handled by PostgreSQL triggers on the `subject` table, not by explicit endpoint code.

**Why**: Ensures the audit trail is always written regardless of which path modifies the row, avoids duplicating logging logic across endpoints, and keeps endpoint code focused on validation and response shaping.

## Risks / Trade-offs

- **Stale soft-deleted records in list results** → The `GET /subjects/my` endpoint MUST filter `is_active = true` by default. If a client caches the list, it may show subjects the user has deleted. Mitigation: list endpoint always applies `is_active = true` filter server-side; no client-side caching guarantee is made.

- **`account_id` isolation not enforced at spec level** → The `account_id` field exists for multi-tenant isolation, but this change only specifies owner-scoped (`owner_id`) access. A future multi-tenant change could break assumptions if `account_id` checks are added without updating these specs. Mitigation: document the gap as an open question.

- **Xano schema drift** → If a future table migration renames or removes `owner_id` or `is_active`, these endpoints will silently misbehave. Mitigation: OpenSpec specs serve as the regression baseline; workflow tests in `atv2Lab/workflow_tests/` should cover the 403 and 404 ownership scenarios.

## Open Questions

1. **Multi-tenant enforcement**: Should `account_id` isolation be enforced in addition to `owner_id`? Currently out of scope, but the table has the field. Needs a decision before adding admin or team-sharing features.
2. **Archived vs deleted subjects**: The table has both `status = archived` and `is_active = false`. Should archived subjects still appear in `GET /subjects/my`? Current decision: yes (filter only on `is_active`), but this may need revisiting.
