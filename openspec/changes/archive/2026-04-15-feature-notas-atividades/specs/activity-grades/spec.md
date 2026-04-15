# activity-grades Specification

## Purpose

Define the database structure and API contract for managing activity grades (notas) in EduTrack AI. Allows professors to record numerical evaluations of student work on specific academic tasks.

## ADDED Requirements

### Requirement: Create activity_grades table

The system SHALL store activity grades with associations to students, activities, and evaluating professors.

#### Scenario: Store professor feedback on student activity
- **WHEN** a professor submits a grade for a student's activity
- **THEN** the system records the grade with timestamp, student reference, activity reference, and professor reference

### Requirement: Validate grade permissions

The system SHALL ensure only the professor who owns the activity's subject can record grades for that activity.

#### Scenario: Unauthorized professor attempt
- **WHEN** a professor from a different subject tries to record a grade
- **THEN** the system returns HTTP 403 Forbidden

#### Scenario: Authorized professor submission
- **WHEN** the activity's subject is owned by the authenticating professor
- **THEN** the system accepts the grade submission

### Requirement: Accept numeric grade values

The system SHALL store grades as numeric values without enforcing a specific scale (0-10, 0-100, etc.).

#### Scenario: Valid numeric grade submission
- **WHEN** a professor submits a numeric grade
- **THEN** the system stores the grade with decimal precision

#### Scenario: Invalid non-numeric submission
- **WHEN** a professor attempts to submit non-numeric data in the grade field
- **THEN** the system returns HTTP 400 Bad Request with validation error

### Requirement: Create POST API endpoint

The system SHALL expose a REST API endpoint for recording activity grades.

#### Scenario: POST /activity_grades creates record
- **WHEN** an authenticated professor sends POST to `/activity_grades` with valid data
- **THEN** the system creates the record and returns HTTP 201 Created with the new grade resource

#### Scenario: Missing required fields
- **WHEN** POST request lacks required fields (activity_id, user_id, grade)
- **THEN** the system returns HTTP 400 Bad Request

### Requirement: Track timestamp and auditor

The system SHALL record when a grade was submitted and by whom.

#### Scenario: Automatic audit trail
- **WHEN** a grade is created
- **THEN** the system automatically populates created_at timestamp and professor_id from authenticated user
