## ADDED Requirements

### Requirement: Create subject
The system SHALL allow an authenticated user to create a new subject by providing a name. Optional fields are `code`, `description`, `semester`, `year`, `credits`, and `status`. The system SHALL automatically assign `owner_id` from the authenticated JWT token and set `is_active = true` and `created_at` / `updated_at` to the current timestamp.

#### Scenario: Successful creation
- **WHEN** an authenticated user sends POST `/subjects` with a valid `name`
- **THEN** the system returns HTTP 200 with the created subject record including its generated `id`, `owner_id`, `created_at`, and `updated_at`

#### Scenario: Missing required field
- **WHEN** an authenticated user sends POST `/subjects` without `name`
- **THEN** the system returns HTTP 400 with a validation error

#### Scenario: Unauthenticated request
- **WHEN** a request is made without a valid Bearer token
- **THEN** the system returns HTTP 401

---

### Requirement: List own subjects
The system SHALL return a paginated list of subjects owned by the authenticated user. Only subjects where `is_active = true` SHALL be included. The endpoint SHALL support `limit` (1–100, default 20) and `offset` (default 0) parameters for pagination.

#### Scenario: List with no subjects
- **WHEN** an authenticated user calls GET `/subjects/my` and owns no active subjects
- **THEN** the system returns HTTP 200 with an empty `items` array and `count = 0`

#### Scenario: Paginated list
- **WHEN** an authenticated user calls GET `/subjects/my` with `limit=5&offset=10`
- **THEN** the system returns up to 5 subjects starting from the 11th record owned by that user

#### Scenario: Soft-deleted subjects excluded
- **WHEN** an authenticated user has a subject with `is_active = false`
- **THEN** that subject SHALL NOT appear in the GET `/subjects/my` response

---

### Requirement: Retrieve a single subject
The system SHALL return the full subject record for a given `id`. The authenticated user SHALL only be able to retrieve subjects they own (`owner_id = $auth.user_id`).

#### Scenario: Successful retrieval
- **WHEN** an authenticated user calls GET `/subjects/{id}` for a subject they own
- **THEN** the system returns HTTP 200 with the full subject record

#### Scenario: Subject not owned by user
- **WHEN** an authenticated user calls GET `/subjects/{id}` for a subject owned by another user
- **THEN** the system returns HTTP 403

#### Scenario: Subject does not exist
- **WHEN** an authenticated user calls GET `/subjects/{id}` with a non-existent `id`
- **THEN** the system returns HTTP 404

---

### Requirement: Partially update a subject
The system SHALL allow an authenticated user to update one or more fields of a subject they own using PATCH semantics. Fields not included in the request SHALL remain unchanged. The system SHALL automatically update `updated_at` to the current timestamp on every successful update.

#### Scenario: Successful partial update
- **WHEN** an authenticated user sends PATCH `/subjects/{id}` with one or more valid fields
- **THEN** the system returns HTTP 200 with the updated subject record and a refreshed `updated_at`

#### Scenario: Update subject not owned by user
- **WHEN** an authenticated user sends PATCH `/subjects/{id}` for a subject owned by another user
- **THEN** the system returns HTTP 403

#### Scenario: Invalid field value
- **WHEN** an authenticated user sends PATCH `/subjects/{id}` with a value that violates a field constraint (e.g., `semester` not matching `^[0-9]º$`)
- **THEN** the system returns HTTP 400 with a validation error

---

### Requirement: Soft-delete a subject
The system SHALL allow an authenticated user to delete a subject they own by setting `is_active = false` and updating `updated_at`. The record SHALL remain in the database and SHALL NOT be returned in list results after deletion.

#### Scenario: Successful soft-delete
- **WHEN** an authenticated user sends DELETE `/subjects/{id}` for a subject they own
- **THEN** the system returns HTTP 200, the subject's `is_active` is set to `false`, and the subject no longer appears in GET `/subjects/my`

#### Scenario: Delete subject not owned by user
- **WHEN** an authenticated user sends DELETE `/subjects/{id}` for a subject owned by another user
- **THEN** the system returns HTTP 403

#### Scenario: Delete already-deleted subject
- **WHEN** an authenticated user sends DELETE `/subjects/{id}` for a subject they own that is already `is_active = false`
- **THEN** the system returns HTTP 200 (idempotent behavior)

---

### Requirement: Authentication required on all subject endpoints
Every subject endpoint (POST, GET /my, GET /{id}, PATCH /{id}, DELETE /{id}) SHALL require a valid Bearer JWT token. Requests without a token or with an expired/invalid token SHALL be rejected before any business logic is executed.

#### Scenario: Request without token to any endpoint
- **WHEN** any subject endpoint is called without a Bearer token
- **THEN** the system returns HTTP 401 before processing the request body or path parameters
