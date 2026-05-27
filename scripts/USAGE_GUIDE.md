# Calculate Progress Script - Usage Guide

## Overview

The `calculate_progress` module provides a Python function to calculate student progress in academic subjects. It computes the percentage of completed tasks and returns structured JSON data.

## Installation

### 1. Ensure Dependencies are Installed

```bash
pip install requests python-dateutil pydantic
```

### 2. Configure Xano API

Set environment variables:

```bash
export XANO_API_URL="https://api.xano.io"
export XANO_API_KEY="your-api-key"
```

Or update in `scripts/utils/database.py`:

```python
XANO_API_URL = "https://your-xano-instance.com"
XANO_API_KEY = "your-api-key"
```

## Usage

### Basic Usage

```python
from scripts.calculate_progress import calculate_progress

# Calculate progress for a student in a subject
result = calculate_progress(user_id=1, subject_id=5)

if result['success']:
    print(f"Progress: {result['data']['progress_percentage']}%")
    print(f"Completed: {result['data']['tasks']['completed']} tasks")
else:
    print(f"Error: {result['error']['message']}")
```

### With Date Range

```python
# Calculate progress for a specific period
result = calculate_progress(
    user_id=1,
    subject_id=5,
    start_date="2026-01-01",
    end_date="2026-05-26"
)
```

### Without Metadata

```python
# Get minimal response without period metadata
result = calculate_progress(
    user_id=1,
    subject_id=5,
    include_metadata=False
)
```

## Response Format

### Success Response

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

### Error Response

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

## Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| `VALIDATION_ERROR` | 400 | Invalid input parameters |
| `USER_NOT_FOUND` | 400 | User ID doesn't exist |
| `SUBJECT_NOT_FOUND` | 400 | Subject ID doesn't exist |
| `INVALID_DATE_FORMAT` | 400 | Date format is not YYYY-MM-DD |
| `INVALID_DATE_RANGE` | 400 | Start date is after end date |
| `ACCESS_DENIED` | 403 | User doesn't have access to subject |
| `DATABASE_ERROR` | 500 | Error querying database |
| `DATABASE_CONNECTION_ERROR` | 500 | Cannot connect to Xano API |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Integration with Streamlit

Example integration in a Streamlit page:

```python
import streamlit as st
from scripts.calculate_progress import calculate_progress

def display_progress():
    """Display student progress in a Streamlit app."""
    user_id = st.session_state.get('user_id')
    subject_id = st.query_params.get('subject_id')
    
    if not user_id or not subject_id:
        st.warning("Missing user or subject")
        return
    
    result = calculate_progress(
        user_id=int(user_id),
        subject_id=int(subject_id)
    )
    
    if result['success']:
        data = result['data']
        st.metric(
            label="Progress",
            value=f"{data['progress_percentage']:.1f}%"
        )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Completed", data['tasks']['completed'])
        with col2:
            st.metric("Pending", data['tasks']['pending'])
        with col3:
            st.metric("In Progress", data['tasks']['in_progress'])
        with col4:
            st.metric("Overdue", data['tasks']['overdue'])
    else:
        st.error(result['error']['message'])

if __name__ == "__main__":
    display_progress()
```

## Integration with FastAPI

Example API endpoint using the progress script:

```python
from fastapi import FastAPI, Query, HTTPException
from scripts.calculate_progress import calculate_progress

app = FastAPI()

@app.get("/api/progress")
def get_progress(
    user_id: int,
    subject_id: int,
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    """Get progress for a student in a subject."""
    result = calculate_progress(
        user_id=user_id,
        subject_id=subject_id,
        start_date=start_date,
        end_date=end_date
    )
    
    if result['success']:
        return result['data']
    else:
        error = result['error']
        raise HTTPException(
            status_code=error['status_code'],
            detail=error['message']
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Testing

Run unit tests:

```bash
cd scripts/tests
python -m unittest test_calculate_progress.py -v
```

Run specific test class:

```bash
python -m unittest test_calculate_progress.TestValidateUserId -v
```

Run specific test method:

```bash
python -m unittest test_calculate_progress.TestValidateUserId.test_valid_positive_integer -v
```

## Parameters Reference

### `calculate_progress()`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user_id` | `int` | Yes | - | Student user ID |
| `subject_id` | `int` | Yes | - | Subject ID |
| `start_date` | `str` | No | `None` | Start date (YYYY-MM-DD) |
| `end_date` | `str` | No | `None` | End date (YYYY-MM-DD) |
| `include_metadata` | `bool` | No | `True` | Include period in response |

### Response Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | int | Student ID |
| `subject_id` | int | Subject ID |
| `subject_name` | string | Subject name |
| `progress_percentage` | float | Progress 0-100 |
| `tasks.completed` | int | Count of completed tasks |
| `tasks.pending` | int | Count of pending tasks |
| `tasks.in_progress` | int | Count of in-progress tasks |
| `tasks.overdue` | int | Count of overdue tasks |
| `tasks.total` | int | Total number of tasks |
| `calculated_at` | string | ISO 8601 timestamp |
| `period.start_date` | string | Filter start date |
| `period.end_date` | string | Filter end date |

## Examples

### Example 1: Check if Student is On Track

```python
from scripts.calculate_progress import calculate_progress

def is_student_on_track(user_id, subject_id, threshold=70.0):
    """Check if student progress is above threshold."""
    result = calculate_progress(user_id, subject_id)
    
    if result['success']:
        progress = result['data']['progress_percentage']
        return progress >= threshold
    return False

# Usage
if is_student_on_track(user_id=1, subject_id=5, threshold=75):
    print("Student is on track!")
else:
    print("Student needs attention")
```

### Example 2: Bulk Progress Report

```python
from scripts.calculate_progress import calculate_progress

def generate_class_report(subject_id, user_ids):
    """Generate progress report for all students in a class."""
    report = {
        "subject_id": subject_id,
        "students": []
    }
    
    for user_id in user_ids:
        result = calculate_progress(user_id, subject_id)
        if result['success']:
            report['students'].append(result['data'])
    
    return report

# Usage
report = generate_class_report(subject_id=5, user_ids=[1, 2, 3, 4, 5])
for student in report['students']:
    print(f"User {student['user_id']}: {student['progress_percentage']}%")
```

### Example 3: Progress Monitoring with Notifications

```python
from scripts.calculate_progress import calculate_progress

def check_and_notify(user_id, subject_id):
    """Check progress and send notification if low."""
    result = calculate_progress(user_id, subject_id)
    
    if not result['success']:
        print(f"Error: {result['error']['message']}")
        return
    
    data = result['data']
    progress = data['progress_percentage']
    
    if progress < 50:
        # Send urgent notification
        notify_student(
            user_id,
            f"Your progress in {data['subject_name']} is only {progress}%. "
            f"Please complete pending tasks."
        )
    elif progress < 75:
        # Send reminder
        notify_student(
            user_id,
            f"You're making good progress in {data['subject_name']}. "
            f"Current: {progress}%"
        )
```

## Troubleshooting

### Connection Errors

**Problem**: `DATABASE_CONNECTION_ERROR`

**Solution**: 
- Verify Xano API URL is correct
- Check API key is valid
- Ensure network connectivity
- Check API rate limits

### Validation Errors

**Problem**: `VALIDATION_ERROR: user_id must be a positive integer`

**Solution**:
- Ensure user_id is a valid integer > 0
- Check that date format is YYYY-MM-DD
- Verify start_date is before end_date

### No Tasks Found

**Problem**: Progress is 0% with 0 tasks

**Solution**:
- Verify user is enrolled in the subject
- Check that tasks exist in the database
- Verify date range filter if using one
- Check data consistency in academic_task table

## Performance Considerations

- Caching: Consider caching results for 5-10 minutes
- Batch Operations: For reports with many users, batch the queries
- Pagination: For subjects with 100+ tasks, consider pagination
- Indexing: Ensure database has indexes on (user_id, subject_id, due_date)

## Contributing

To extend or modify the progress calculation:

1. Update validators in `scripts/utils/validators.py`
2. Update database queries in `scripts/utils/database.py`
3. Update calculation logic in `scripts/calculate_progress.py`
4. Add tests in `scripts/tests/test_calculate_progress.py`
5. Update this documentation

## Support

For issues or questions:
- Check error messages and error codes
- Review logs in application directory
- Consult specification in `SPECIFICATION.md`
- Review design documentation in `design.md`
