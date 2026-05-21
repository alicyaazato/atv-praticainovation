# Academic Tasks Database Specification

## Purpose

This specification defines the database schema and infrastructure for managing academic tasks in the EduTrack AI system. Academic tasks represent student assignments, lessons, tests, and other learning obligations linked to specific academic subjects.

## Requirements

### Requirement: Create academic_task Table
The system SHALL store academic task information with clear ownership and relationship to subjects.

#### Scenario: Student creates an academic task
- **WHEN** a student creates a new academic task
- **THEN** the system stores it with proper user_id and subject_id associations
- **AND** the task status is set to "pending" by default
- **AND** created_at and updated_at timestamps are automatically set

### Requirement: Support task status tracking
The system SHALL track task completion status through defined enum values.

#### Scenario: Teacher views student task progress
- **WHEN** a teacher accesses tasks for a subject
- **THEN** each task shows current status (pending, in_progress, completed, overdue)
- **AND** tasks can be filtered by status

### Requirement: Implement automatic audit logging
The system SHALL log all academic_task table changes to the event_logs table.

#### Scenario: Student completes a task
- **WHEN** a student updates task status to "completed"
- **THEN** an event is logged with event type "academic_task.updated"
- **AND** the metadata includes the status change details

### Requirement: Support data validation
The system SHALL validate all required fields and constraints before storage.

#### Scenario: Invalid task data submission
- **WHEN** a user submits invalid task data (empty title, invalid date)
- **THEN** the system rejects the submission with clear validation error
- **AND** no database record is created

## Data Model

### Table: academic_task

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| id | int | Yes | auto | primary key | Unique identifier for task |
| title | text | Yes | - | max:255 | Task title/name |
| description | text | No | - | max:2000 | Detailed task description |
| user_id | int | Yes | - | FK to user | Student who owns task |
| subject_id | int | Yes | - | FK to subject | Subject task belongs to |
| due_date | date | Yes | - | required, valid date | Task due date |
| status | enum | Yes | "pending" | pending, in_progress, completed, overdue | Task completion status |
| metadata | json | No | - | private | Additional task metadata |
| created_at | timestamp | Yes | now | auto, private | Record creation timestamp |
| updated_at | timestamp | Yes | now | auto, private | Record update timestamp |

### Relationships

```
academic_task.user_id → user.id (Task owner)
academic_task.subject_id → subject.id (Associated subject)
```

## Indexes

| Name | Type | Columns | Purpose |
|------|------|---------|---------|
| pk_academic_task | Primary | id | Primary key |
| idx_user_id | BTree | user_id | Find tasks by student |
| idx_subject_id | BTree | subject_id | Find tasks by subject |
| idx_status | BTree | status | Filter tasks by status |
| idx_user_status | Composite | (user_id, status) | Find student's pending tasks |
| idx_due_date | BTree | due_date | Sort by due date |
| idx_created_at | BTree | created_at DESC | Recent tasks |
| idx_updated_at | BTree | updated_at DESC | Recently modified |

## Constraints

### Field-Level Constraints
- **title**: NOT NULL, max 255 characters, required validation
- **user_id**: NOT NULL, must reference valid user.id
- **subject_id**: NOT NULL, must reference valid subject.id
- **due_date**: NOT NULL, must be valid date format (YYYY-MM-DD)
- **status**: NOT NULL, must be one of: pending, in_progress, completed, overdue
- **created_at**: NOT NULL, auto-generated on INSERT
- **updated_at**: NOT NULL, auto-generated/updated on INSERT or UPDATE

### Referential Integrity
- Deleting a user should handle cascading (document separately)
- Deleting a subject should handle cascading (document separately)
- Foreign key constraints enforced by database

## Access Control

| Role | Can Create | Can Read Own | Can Update | Can Delete | Can Read Others |
|------|-----------|--------------|-----------|-----------|-----------------|
| Student (Owner) | Yes | Yes | Yes | Yes | No |
| Teacher (Subject Owner) | No | - | No | No | Yes (their subjects) |
| Account Admin | No | - | No | No | Yes (all) |
| Other Users | No | - | No | No | No |

## Event Logging

All operations on `academic_task` generate events in `event_logs` table:

### Events Generated

| Event Type | Trigger | Payload |
|-----------|---------|---------|
| academic_task.created | After INSERT | task_id, title, user_id, subject_id, due_date, status |
| academic_task.updated | After UPDATE | task_id, title, changes (diff) |
| academic_task.deleted | After DELETE | task_id, title, user_id, subject_id, reason |
| academic_task.status_changed | After UPDATE (status field) | task_id, from_status, to_status |

### Event Payload Example

```json
{
  "event": "academic_task.updated",
  "task_id": 12345,
  "task_title": "Chapter 5 Exercises",
  "changes": {
    "status": {
      "from": "pending",
      "to": "in_progress"
    }
  }
}
```

## Status Lifecycle

```
pending
  ├→ in_progress (optional)
  │   ├→ completed (success)
  │   └→ overdue (deadline passed)
  └→ completed (direct)
```

**Rules**:
- Tasks marked as "overdue" when due_date < today AND status != completed
- Status transitions are user-initiated except for "overdue" (automated)

## Integration Points

1. **User Management**: Tasks linked to authenticated users
2. **Subject Management**: Tasks linked to academic subjects
3. **Event Logging**: Automatic audit trail via event_logs table
4. **APIs**: Future CRUD endpoints for task management
5. **Notifications**: Future notifications for approaching deadlines
6. **Reporting**: Future analytics on task completion rates

## Implementation Notes

- Xano Table ID: 753428_academic_task.xs
- Triggers File: 754428_academic_task_triggers.xs
- Test File: academic_tasks_integration_tests.xs
- No soft-delete implemented (tasks are hard-deleted)
- Timestamps use UTC timezone
- Enum values use lowercase (pending, in_progress, etc.)

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-21 | AI Assistant | Initial specification |
