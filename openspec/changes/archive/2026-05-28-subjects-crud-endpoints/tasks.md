## 1. Endpoint — POST /subjects (Create)

- [x] 1.1 Verify the `POST /subjects` function exists in `atv2Lab/apis/subjects/` and has `auth = "user"` set
- [x] 1.2 Confirm `owner_id` is auto-assigned from `$auth.user_id` (not accepted as input)
- [x] 1.3 Confirm `name` is required and returns HTTP 400 when missing
- [x] 1.4 Confirm optional fields (`code`, `description`, `semester`, `year`, `credits`, `status`) are accepted and stored correctly
- [x] 1.5 Confirm `is_active = true`, `created_at`, and `updated_at` are set automatically on creation
- [x] 1.6 Confirm response returns the full subject record including `id`, `owner_id`, `created_at`, `updated_at`

## 2. Endpoint — GET /subjects/my (List own subjects)

- [x] 2.1 Verify the `GET /subjects/my` function exists and has `auth = "user"` set
- [x] 2.2 Confirm the query filters `owner_id = $auth.user_id` and `is_active = true`
- [x] 2.3 Confirm `limit` parameter is accepted (1–100, default 20) and `offset` (default 0)
- [x] 2.4 Confirm soft-deleted subjects (`is_active = false`) are excluded from results
- [x] 2.5 Confirm response returns `items` array and `count` (total matching records)

## 3. Endpoint — GET /subjects/{id} (Retrieve single subject)

- [x] 3.1 Verify the `GET /subjects/{id}` function exists and has `auth = "user"` set
- [x] 3.2 Confirm that requesting a subject owned by another user returns HTTP 403
- [x] 3.3 Confirm that requesting a non-existent `id` returns HTTP 404
- [x] 3.4 Confirm successful retrieval returns the full subject record for the owner

## 4. Endpoint — PATCH /subjects/{id} (Partial update)

- [x] 4.1 Verify the `PATCH /subjects/{id}` function exists and has `auth = "user"` set
- [x] 4.2 Confirm PATCH semantics: only provided fields are updated; omitted fields remain unchanged
- [x] 4.3 Confirm `updated_at` is automatically refreshed on every successful update
- [x] 4.4 Confirm that patching a subject owned by another user returns HTTP 403
- [x] 4.5 Confirm field-level validation (e.g., `semester` must match `^[0-9]º$`) returns HTTP 400

## 5. Endpoint — DELETE /subjects/{id} (Soft-delete)

- [x] 5.1 Verify the `DELETE /subjects/{id}` function exists and has `auth = "user"` set
- [x] 5.2 Confirm deletion sets `is_active = false` and updates `updated_at` (no hard-delete)
- [x] 5.3 Confirm the subject no longer appears in `GET /subjects/my` after deletion
- [x] 5.4 Confirm that deleting a subject owned by another user returns HTTP 403
- [x] 5.5 Confirm idempotent behavior: deleting an already-deleted subject returns HTTP 200

## 6. Authentication guard (all endpoints)

- [x] 6.1 Confirm all 5 endpoints reject requests without a Bearer token with HTTP 401
- [x] 6.2 Confirm all 5 endpoints reject requests with an expired or invalid token with HTTP 401

## 7. Integration tests

- [x] 7.1 Add workflow test for the happy-path create → list → read → update → delete cycle
- [x] 7.2 Add workflow test asserting ownership boundary: User A cannot read, update, or delete User B's subjects
- [x] 7.3 Add workflow test asserting soft-deleted subjects are excluded from list results

## 8. Streamlit frontend integration

- [x] 8.1 Wire up `pages/` Disciplinas page to call `GET /subjects/my` with the stored auth token
- [x] 8.2 Implement create-subject form calling `POST /subjects`
- [x] 8.3 Implement edit-subject form calling `PATCH /subjects/{id}`
- [x] 8.4 Implement delete-subject action calling `DELETE /subjects/{id}` and refreshing the list
