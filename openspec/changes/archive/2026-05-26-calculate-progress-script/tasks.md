# Calculate Progress Script - Implementation Tasks

## Phase 1: Setup & Validation (2h)

### Task 1.1: Create Project Structure
- [x] Create `scripts/` directory (if not exists)
- [x] Create `scripts/calculate_progress.py` with base skeleton
- [x] Create `scripts/__init__.py`
- [x] Create `scripts/utils/` subdirectory
- [x] Create `scripts/tests/` subdirectory

**Acceptance Criteria:**
- Directory structure is in place
- Files are creatable without errors

### Task 1.2: Create Input Validators
- [x] Create `scripts/utils/validators.py`
- [x] Implement `validate_user_id(user_id: int) -> bool`
- [x] Implement `validate_subject_id(subject_id: int) -> bool`
- [x] Implement `validate_date_format(date_str: str) -> bool`
- [x] Implement `validate_date_range(start: str, end: str) -> bool`
- [x] Add proper error messages for each validation

**Acceptance Criteria:**
- All validators return boolean
- Error messages are clear and actionable
- Handles None values gracefully

---

## Phase 2: Database Integration (2h)

### Task 2.1: Create Database Connection Module
- [x] Create `scripts/utils/database.py`
- [x] Implement `get_xano_connection()` or `fetch_xano_data()`
- [x] Add error handling for connection failures
- [x] Add retry logic (optional but recommended)

**Acceptance Criteria:**
- Can successfully query Xano API
- Handles auth/credentials securely
- Clear error messages on failure

### Task 2.2: Create Query Function
- [x] Implement `fetch_tasks_by_user_subject(user_id, subject_id, start_date, end_date)`
- [x] Query `academic_task` table with filters
- [x] Return list of tasks with status
- [x] Add proper SQL/query parameter handling

**Acceptance Criteria:**
- Returns correct task data
- Filters work correctly
- Handles no results gracefully

---

## Phase 3: Core Logic (2h)

### Task 3.1: Implement Progress Calculation
- [x] Create main function `calculate_progress(user_id, subject_id, start_date, end_date)`
- [x] Count tasks by status (completed, pending, in_progress, overdue)
- [x] Calculate percentage: `(completed / total) * 100`
- [x] Handle division by zero (no tasks case)

**Acceptance Criteria:**
- Formula is mathematically correct
- Edge case (0 tasks) returns progress_percentage: 0
- All statuses are counted

### Task 3.2: Fetch Subject Info
- [x] Query subject name/details from Xano
- [x] Include `subject_name` in response
- [x] Handle missing subjects gracefully

**Acceptance Criteria:**
- Subject information is included
- Returns null/empty string if subject not found
- No API errors

---

## Phase 4: JSON Response Builder (1h)

### Task 4.1: Create Response Template
- [x] Implement `build_response(user_id, subject_id, progress_data, metadata)`
- [x] Follow JSON schema from design.md
- [x] Include all required fields
- [x] Add timestamp (`calculated_at`)

**Acceptance Criteria:**
- JSON is valid and parseable
- All fields match schema
- Timestamp is ISO 8601 format

### Task 4.2: Error Response Handler
- [x] Implement `build_error_response(error_code, error_message)`
- [x] Follow consistent error format
- [x] Map exceptions to proper error codes

**Acceptance Criteria:**
- Error JSON is valid
- Contains `success: false`, `error` message
- HTTP status codes are appropriate

---

## Phase 5: Error Handling & Logging (1h)

### Task 5.1: Add Exception Handling
- [x] Wrap database calls in try-except
- [x] Validate inputs before processing
- [x] Return appropriate error responses
- [x] Log errors with context

**Acceptance Criteria:**
- No unhandled exceptions reach user
- Logs contain debugging information
- User receives helpful error messages

### Task 5.2: Add Logging
- [x] Setup Python logging module
- [x] Log function calls with parameters
- [x] Log calculation steps
- [x] Log errors and exceptions

**Acceptance Criteria:**
- Logs are created in appropriate location
- Log level can be configured
- Contains useful debugging info

---

## Phase 6: Testing (2h)

### Task 6.1: Unit Tests for Validators
- [x] Test `validate_user_id()` with valid/invalid inputs
- [x] Test `validate_subject_id()` with valid/invalid inputs
- [x] Test `validate_date_format()` with various formats
- [x] Test `validate_date_range()` with invalid ranges

**Acceptance Criteria:**
- All validators pass unit tests
- Edge cases are covered
- Tests are repeatable

### Task 6.2: Integration Tests
- [x] Test with real/mock Xano data
- [x] Test `calculate_progress()` with sample data
- [x] Test JSON response format
- [x] Test error scenarios

**Acceptance Criteria:**
- Tests pass with mock data
- JSON responses are valid
- Error handling works as expected

### Task 6.3: Edge Case Tests
- [x] Test with 0 tasks
- [x] Test with 100% completed
- [x] Test with no subject_id match
- [x] Test with invalid dates

**Acceptance Criteria:**
- All edge cases handled
- No crashes or exceptions
- Returns proper responses

---

## Phase 7: Documentation & Examples (1h)

### Task 7.1: Add Docstrings
- [x] Document main function with parameters, returns, raises
- [x] Add examples in docstring
- [x] Document helper functions
- [x] Include type hints

**Acceptance Criteria:**
- All functions have docstrings
- Examples are clear and runnable
- Type hints are present

### Task 7.2: Create Usage Guide
- [x] Create `README.md` or section in project docs
- [x] Include example calls
- [x] Show expected JSON output
- [x] Document all parameters

**Acceptance Criteria:**
- Documentation is clear
- Examples work as shown
- New developers can use the script

---

## Phase 8: Integration & Deployment (1h)

### Task 8.1: Integration Points
- [x] Test integration with Streamlit pages (if needed)
- [x] Test integration with existing APIs
- [x] Verify import paths work correctly
- [x] Check dependency compatibility

**Acceptance Criteria:**
- No import errors
- Can be called from other modules
- Works with existing infrastructure

### Task 8.2: Cleanup & Finalization
- [x] Remove debug code
- [x] Review code style (PEP8)
- [x] Final testing pass
- [x] Commit to version control

**Acceptance Criteria:**
- Code is clean and well-formatted
- All tests pass
- Ready for production use

---

## Summary

| Phase | Duration | Tasks | Status |
|-------|----------|-------|--------|
| 1: Setup & Validation | 2h | Create structure, validators | ✅ Complete |
| 2: Database Integration | 2h | Connection, queries | ✅ Complete |
| 3: Core Logic | 2h | Calculation, aggregation | ✅ Complete |
| 4: JSON Response Builder | 1h | Response formatting | ✅ Complete |
| 5: Error Handling & Logging | 1h | Exception handling, logs | ✅ Complete |
| 6: Testing | 2h | Unit, integration, edge cases | ✅ Complete |
| 7: Documentation | 1h | Docstrings, examples | ✅ Complete |
| 8: Integration & Deployment | 1h | Integration, finalization | ✅ Complete |
| **TOTAL** | **~12h** | **Full implementation** | ✅ **COMPLETE** |

## Completion Status

✅ **ALL 69 TASKS COMPLETED**

### Deliverables

1. **Core Script**: `scripts/calculate_progress.py` - Main progress calculation function
2. **Validators**: `scripts/utils/validators.py` - Input validation with comprehensive error handling
3. **Database Module**: `scripts/utils/database.py` - Xano API integration with retry logic
4. **Unit Tests**: `scripts/tests/test_calculate_progress.py` - 15+ test cases covering all scenarios
5. **Usage Guide**: `scripts/USAGE_GUIDE.md` - Complete documentation with examples
6. **Type Hints**: Full type annotations throughout codebase
7. **Error Handling**: Comprehensive exception handling and logging
8. **Code Quality**: PEP8 compliant, well-documented, production-ready
