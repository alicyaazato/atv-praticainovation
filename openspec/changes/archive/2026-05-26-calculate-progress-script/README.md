# Calculate Progress Script - Implementation Plan

## 📋 Overview

A complete implementation plan for `scripts/calculate_progress.py`, a Python script that calculates student progress in academic subjects by dividing completed tasks by total tasks and returning results in JSON format.

**Created:** 2026-05-26  
**Status:** 📝 Planned & Designed  
**Estimated Duration:** ~12 hours (8 phases)

---

## 📁 Documentation Structure

```
openspec/changes/calculate-progress-script/
├── .openspec.yaml           # Metadata and artifact references
├── proposal.md              # Problem statement, solution, goals
├── design.md                # Architecture, data model, integration points
├── SPECIFICATION.md         # Technical specs, JSON schemas, examples
├── tasks.md                 # Implementation tasks (Phase 1-8)
└── README.md                # This file
```

---

## 🎯 Quick Summary

| Aspect | Details |
|--------|---------|
| **What** | Python script to calculate academic progress percentage |
| **Where** | `scripts/calculate_progress.py` |
| **Input** | user_id, subject_id, optional date range |
| **Output** | JSON with progress %, task counts, metadata |
| **Usage** | Called by APIs, Streamlit pages, reports |
| **Timeline** | 8 phases, ~12 hours total |

---

## 📊 Key Features

✅ **Core Functionality**
- Calculate progress: `(completed_tasks / total_tasks) * 100`
- Support multiple users and subjects
- Filter by date range (optional)
- Handle edge cases (0 tasks, 100% complete, etc.)

✅ **Data Integration**
- Query `academic_task` table from Xano
- Join with `subject` table for subject info
- Validate user access permissions

✅ **Error Handling**
- Comprehensive input validation
- Proper HTTP status codes
- Clear error messages with codes
- Logging for debugging

✅ **Output Format**
- Valid JSON response
- Success/error distinction
- Structured metadata
- ISO 8601 timestamps

---

## 🏗️ Architecture

```
Request Input
    ↓
[1] Validate Inputs (user_id, subject_id, dates)
    ↓
[2] Check User Access & Permissions
    ↓
[3] Query Database (academic_task by filters)
    ↓
[4] Aggregate Task Counts (by status)
    ↓
[5] Calculate Progress %
    ↓
[6] Fetch Subject Details
    ↓
[7] Build JSON Response
    ↓
Return JSON (success or error)
```

---

## 📈 Implementation Phases

### Phase 1: Setup & Validation (2h)
- Create directory structure
- Build input validators
- **Status:** Prerequisite for all phases

### Phase 2: Database Integration (2h)
- Setup Xano connection
- Create query functions
- **Status:** Required for Phase 3

### Phase 3: Core Logic (2h)
- Implement progress calculation
- Count tasks by status
- **Status:** Heart of the implementation

### Phase 4: JSON Response Builder (1h)
- Format response objects
- Build error responses
- **Status:** Depends on Phase 3

### Phase 5: Error Handling & Logging (1h)
- Add exception handling
- Setup logging
- **Status:** Concurrent with Phase 3-4

### Phase 6: Testing (2h)
- Unit tests for validators
- Integration tests
- Edge case testing
- **Status:** Parallel to Phase 5

### Phase 7: Documentation (1h)
- Add docstrings and examples
- Create usage guide
- **Status:** After Phase 6

### Phase 8: Integration & Deployment (1h)
- Test with existing modules
- Code review and cleanup
- **Status:** Final phase

**Total Estimated Time:** ~12 hours

---

## 📊 Response Example

### Success (200 OK)
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "subject_id": 5,
    "subject_name": "Matemática",
    "progress_percentage": 75.5,
    "tasks": {
      "completed": 15,
      "pending": 3,
      "in_progress": 2,
      "overdue": 1,
      "total": 21
    },
    "calculated_at": "2026-05-26T14:30:00Z",
    "period": {
      "start_date": "2026-01-01",
      "end_date": "2026-05-26"
    }
  },
  "error": null
}
```

### Error (400 Bad Request)
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 999 not found",
    "status_code": 400
  }
}
```

---

## 🔗 Integration Points

- **Xano Database**: Fetch academic_task data
- **Streamlit Pages**: Show progress bars in subject/task pages
- **APIs**: `/api/progress` endpoint (future)
- **Reports**: Aggregate progress across students
- **Automation**: Trigger notifications based on progress

---

## 📋 Acceptance Criteria

- [ ] Script executes without errors
- [ ] Calculates progress correctly (formula verified)
- [ ] Returns valid JSON matching schema
- [ ] Handles all edge cases gracefully
- [ ] Provides clear error messages
- [ ] Includes comprehensive documentation
- [ ] All unit/integration tests pass
- [ ] Ready for production deployment

---

## 🚀 Next Steps

1. **Review** this plan and provide feedback
2. **Start Phase 1**: Create directory structure and validators
3. **Track progress** using tasks.md checklist
4. **Test thoroughly** with real/mock data
5. **Document** usage and integration points
6. **Deploy** and integrate with existing systems

---

## 📝 Related Documents

- **proposal.md** - Problem, solution, goals, non-goals
- **design.md** - Architecture, data model, error handling
- **SPECIFICATION.md** - Complete technical specification
- **tasks.md** - Detailed implementation tasks (8 phases)

---

## 📞 Questions & Notes

- [ ] Xano API auth method finalized?
- [ ] Edge case priority (0 tasks, access denied)?
- [ ] Performance requirements for large datasets?
- [ ] Logging level and destination configured?
- [ ] Date timezone handling (UTC vs local)?

---

**Status:** ✅ Plan Complete - Ready for Implementation
