# Subjects Database - Implementation Tasks

## Overview

This document outlines the implementation tasks for creating and integrating the subjects database feature. Tasks are organized by phases and priority.

## Phase 1: Database Schema & Core Infrastructure

### Task 1.1: Create Subject Table
**Priority**: P0 - Critical
**Estimated Time**: 1-2 hours
**Dependencies**: None

**Description**:
- Create `subject` table in Xano database
- Define all fields as per spec (id, name, description, code, owner_id, account_id, etc.)
- Set up indexes for performance (owner_id, account_id, code)
- Define foreign key constraints
- Enable created_at / updated_at auto-timestamps

**Acceptance Criteria**:
- [x] Table exists in Xano with all fields
- [x] Primary key and indexes configured
- [x] Foreign key constraints working
- [x] Auto-timestamps functional

**Resources**:
- See: `specs/01-table-schema.md`
- Reference: Existing table patterns in `tables/753421_user.xs`

---

### Task 1.2: Create Event Logging Infrastructure
**Priority**: P0 - Critical
**Estimated Time**: 1-2 hours
**Dependencies**: Task 1.1

**Description**:
- Create triggers on subject table for INSERT, UPDATE, DELETE
- Integrate with existing `create_event_log` function
- Map subject events (created, updated, deleted) to event_logs
- Add details payload with field changes

**Acceptance Criteria**:
- [x] INSERT trigger created and tested
- [x] UPDATE trigger captures changes
- [x] DELETE trigger logs deletion
- [x] Events properly captured in event_logs
- [x] Event payloads include required details

**Resources**:
- See: `specs/03-event-logging.md`
- Reference: Existing function `269536_create_event_log.xs`

---

### Task 1.3: Create Core API Endpoints (CRUD)
**Priority**: P0 - Critical
**Estimated Time**: 4-6 hours
**Dependencies**: Task 1.1, Task 1.2

**Description**:
Create the following REST API endpoints:
1. `POST /subjects` - Create subject
2. `GET /subjects/my` - List user's subjects
3. `GET /subjects/:id` - Get subject details
4. `PATCH /subjects/:id` - Update subject
5. `DELETE /subjects/:id` - Delete subject

**Acceptance Criteria**:
- [x] All 5 endpoints implemented
- [x] Input validation working
- [x] Error responses properly formatted
- [x] Pagination implemented for list endpoint
- [x] Timestamps returned correctly
- [x] Endpoints accept and return correct JSON

**Resources**:
- See: `specs/02-api-endpoints.md`
- Reference: Existing API patterns in `apis/`

---

## Phase 2: Authorization & Security

### Task 2.1: Implement RBAC for Subjects
**Priority**: P1 - High
**Estimated Time**: 3-4 hours
**Dependencies**: Task 1.3

**Description**:
- Implement role-based access control middleware
- Enforce owner-based permissions
- Enforce account authority
- Implement admin overrides
- Add permission validation to all subject endpoints

**Acceptance Criteria**:
- [x] Owner can read/modify their subjects
- [x] Members can only access their subjects
- [x] Admins can access all account subjects
- [x] Unauthorized access returns 403
- [x] All endpoints validate permissions
- [x] 404 returned instead of 403 to prevent leaks

**Resources**:
- See: `specs/04-security-rbac.md`
- Reference: Existing RBAC in `functions/269537_role_based_access_control.xs`

---

### Task 2.2: Add Input Validation & Sanitization
**Priority**: P1 - High
**Estimated Time**: 2-3 hours
**Dependencies**: Task 1.3

**Description**:
- Add input validation to all endpoints
- Validate field types and lengths
- Sanitize descriptions to prevent XSS
- Validate foreign keys
- Validate enums (status, semester, etc)

**Acceptance Criteria**:
- [ ] Invalid inputs rejected with 400 errors
- [ ] Error messages descriptive
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] Field length constraints enforced

**Resources**:
- See: `specs/02-api-endpoints.md` - Validation section

---

## Phase 3: Testing & Documentation

### Task 3.1: Write Integration Tests
**Priority**: P1 - High
**Estimated Time**: 3-4 hours
**Dependencies**: Task 2.1, Task 2.2

**Description**:
- Write integration tests for all endpoints
- Test happy paths and error cases
- Test RBAC scenarios
- Test event logging
- Test data isolation between accounts

**Test Scenarios**:
- User can create subject
- User cannot create subject in other account
- Owner can update subject
- Non-owner cannot update subject
- Admin can update any subject
- Events logged properly
- Pagination works

**Acceptance Criteria**:
- [ ] All CRUD endpoints tested
- [ ] RBAC scenarios tested
- [ ] Event logging verified
- [ ] Error cases covered
- [ ] Tests pass 100%

---

### Task 3.2: Create API Documentation
**Priority**: P2 - Medium
**Estimated Time**: 2-3 hours
**Dependencies**: Task 1.3

**Description**:
- Create OpenAPI/Swagger documentation
- Document all endpoints with examples
- Document authentication requirements
- Document error codes
- Document rate limits

**Acceptance Criteria**:
- [ ] All endpoints documented
- [ ] Examples provided
- [ ] Error codes explained
- [ ] Accessible via /docs or similar
- [ ] Team can understand usage

---

### Task 3.3: Update Database Documentation
**Priority**: P2 - Medium
**Estimated Time**: 1-2 hours
**Dependencies**: Task 1.1

**Description**:
- Add subject table to system documentation
- Create ER diagram with relationships
- Document indexes and constraints
- Add to data dictionary

**Acceptance Criteria**:
- [ ] Table documented
- [ ] ER diagram updated
- [ ] Relationships clear
- [ ] Available in docs/

---

## Phase 4: Enhancements & Future Work

### Task 4.1: Add Pagination & Filtering
**Priority**: P2 - Medium
**Estimated Time**: 2-3 hours
**Dependencies**: Task 1.3

**Description**:
- Add filter support to list endpoints (by status, semester, year)
- Paginate results properly
- Add sorting support
- Optimize queries with proper indexes

**Acceptance Criteria**:
- [ ] Filter by status, semester, year working
- [ ] Sorting by name, created_at implemented
- [ ] Pagination limit/offset working
- [ ] Query performance verified

---

### Task 4.2: Add Search Functionality
**Priority**: P3 - Low
**Estimated Time**: 2-3 hours
**Dependencies**: Task 1.3

**Description**:
- Implement search on subject name and code
- Add full-text search if possible
- Optimize search performance

**Acceptance Criteria**:
- [ ] Can search by name
- [ ] Can search by code
- [ ] Results relevant
- [ ] Performance acceptable

---

### Task 4.3: Prepare for Sharing & Collaboration
**Priority**: P3 - Low
**Estimated Time**: 3-4 hours
**Dependencies**: Task 2.1

**Description**:
- Design sharing mechanism (share with users/roles)
- Create database schema for subject_share_permissions
- Implement share/unshare endpoints
- Prepare for future collaboration features

**Acceptance Criteria**:
- [ ] Sharing mechanism designed
- [ ] Schema prepared
- [ ] Endpoints stubbed
- [ ] Documentation ready for Phase 2

---

## Summary

| Phase | Est. Time | Priority |
|-------|-----------|----------|
| Phase 1 (Core) | 7-10 hrs | P0 |
| Phase 2 (Security) | 5-7 hrs | P1 |
| Phase 3 (Testing) | 6-9 hrs | P1 |
| Phase 4 (Enhancements) | 7-10 hrs | P2/P3 |
| **TOTAL** | **25-36 hrs** | - |

## Success Criteria

- ✅ All Phase 1 & 2 tasks completed
- ✅ 100% test coverage for critical paths
- ✅ Zero security vulnerabilities
- ✅ All RBAC rules enforced
- ✅ Event logging working
- ✅ Documentation complete
- ✅ Team can use and maintain feature
