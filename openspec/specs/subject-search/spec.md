### Requirement: Search subjects by name
The system SHALL allow an authenticated user to search their own subjects by partial name match (case-insensitive). Only subjects where `is_active = true` and `owner_id = $auth.user_id` SHALL be returned.

#### Scenario: Successful name search
- **WHEN** an authenticated user calls GET `/subjects/search?q=calc`
- **THEN** the system returns HTTP 200 with an `items` array containing only subjects owned by that user whose `name` contains "calc" (case-insensitive) and are active

#### Scenario: No matches found
- **WHEN** an authenticated user calls GET `/subjects/search?q=xyznotfound`
- **THEN** the system returns HTTP 200 with an empty `items` array and `count = 0`

#### Scenario: Unauthenticated request
- **WHEN** a request is made to GET `/subjects/search` without a valid Bearer token
- **THEN** the system returns HTTP 401

---

### Requirement: Search subjects with overdue tasks
The system SHALL allow an authenticated user to retrieve their own subjects that have at least one academic task with `due_date < now` and `status != "completed"`. Only subjects where `is_active = true` and `owner_id = $auth.user_id` SHALL be considered.

#### Scenario: Filter subjects with overdue tasks
- **WHEN** an authenticated user calls GET `/subjects/search?has_overdue_tasks=true`
- **THEN** the system returns HTTP 200 with an `items` array containing only the user's active subjects that have at least one overdue task

#### Scenario: No overdue tasks exist
- **WHEN** an authenticated user calls GET `/subjects/search?has_overdue_tasks=true` and none of their subjects have overdue tasks
- **THEN** the system returns HTTP 200 with an empty `items` array and `count = 0`

#### Scenario: Tasks without due date are not considered overdue
- **WHEN** a subject has tasks where `due_date` is null
- **THEN** those tasks SHALL NOT cause the subject to appear in the `has_overdue_tasks=true` results

---

### Requirement: Combined search (name OR overdue tasks)
The system SHALL apply OR logic when both `q` and `has_overdue_tasks=true` are provided: the response SHALL include subjects that match by name **or** have overdue tasks (or both). The result SHALL NOT contain duplicate subjects.

#### Scenario: Combined filter returns union of results
- **WHEN** an authenticated user calls GET `/subjects/search?q=math&has_overdue_tasks=true`
- **THEN** the system returns HTTP 200 with subjects that match "math" by name **or** have overdue tasks, deduplicated by subject `id`

#### Scenario: No filters provided returns empty result
- **WHEN** an authenticated user calls GET `/subjects/search` with neither `q` nor `has_overdue_tasks`
- **THEN** the system returns HTTP 400 with a validation error requiring at least one filter parameter

---

### Requirement: Paginated search results
The system SHALL support `limit` (1–100, default 20) and `offset` (default 0) pagination parameters on GET `/subjects/search`.

#### Scenario: Paginated results
- **WHEN** an authenticated user calls GET `/subjects/search?q=calc&limit=5&offset=0`
- **THEN** the system returns at most 5 matching subjects and a `count` field with the total number of matches

---

### Requirement: Overdue detection implemented as Python function
The system SHALL implement overdue-task detection as a reusable Xano Python function `filter_overdue_subjects(subject_ids, user_id)` that accepts a list of subject IDs and the authenticated user ID, queries the `academic_task` table, and returns only the IDs that have at least one task where `due_date IS NOT NULL AND due_date < now AND status != "completed"`.

#### Scenario: Function returns correct overdue IDs
- **WHEN** the function is called with a list of subject IDs that includes some with overdue tasks
- **THEN** the function returns only the IDs whose tasks qualify as overdue

#### Scenario: Function handles empty input
- **WHEN** the function is called with an empty list of subject IDs
- **THEN** the function returns an empty list without error
