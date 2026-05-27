# Calculate Progress Script - Specification

## Overview

Complete technical specification for `scripts/calculate_progress.py`, including function signatures, JSON schemas, examples, and implementation details.

---

## Function Signature

```python
def calculate_progress(
    user_id: int,
    subject_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    include_metadata: bool = True
) -> dict
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user_id` | `int` | Yes | - | ID do usuário (aluno) |
| `subject_id` | `int` | Yes | - | ID da disciplina |
| `start_date` | `str` | No | `None` | Data inicial (YYYY-MM-DD) |
| `end_date` | `str` | No | `None` | Data final (YYYY-MM-DD) |
| `include_metadata` | `bool` | No | `True` | Include metadata na resposta |

### Returns

Returns a `dict` with the structure defined in Response Schema below.

### Raises

- `ValueError`: Invalid input parameters or date format
- `KeyError`: Missing required data from database
- `ConnectionError`: Cannot connect to Xano API
- `PermissionError`: User doesn't have access to subject

---

## Request Examples

### Example 1: Basic Request (All Tasks)

```python
result = calculate_progress(user_id=1, subject_id=5)
```

**Query:** All academic_tasks for user 1 in subject 5, without date filtering.

### Example 2: Request with Date Range

```python
result = calculate_progress(
    user_id=1, 
    subject_id=5,
    start_date="2026-01-01",
    end_date="2026-05-26"
)
```

**Query:** academic_tasks for user 1 in subject 5 with due_date between 2026-01-01 and 2026-05-26.

### Example 3: Request without Metadata

```python
result = calculate_progress(
    user_id=1,
    subject_id=5,
    include_metadata=False
)
```

**Response:** Omits `period` field and other metadata.

---

## Response Schema

### Success Response (200)

```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "subject_id": 5,
    "subject_name": "Matemática Avançada",
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

### Error Response (400/403/500)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_USER_ID",
    "message": "User with ID 999 not found",
    "status_code": 400
  }
}
```

---

## Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `success` | `boolean` | Indica sucesso ou falha |
| `data.user_id` | `int` | ID do usuário que foi consultado |
| `data.subject_id` | `int` | ID da disciplina que foi consultada |
| `data.subject_name` | `string` | Nome da disciplina (ex: "Matemática") |
| `data.progress_percentage` | `float` | Porcentagem de conclusão (0-100) |
| `data.tasks.completed` | `int` | Quantidade de tarefas concluídas |
| `data.tasks.pending` | `int` | Quantidade de tarefas pendentes |
| `data.tasks.in_progress` | `int` | Quantidade de tarefas em progresso |
| `data.tasks.overdue` | `int` | Quantidade de tarefas atrasadas |
| `data.tasks.total` | `int` | Total de tarefas |
| `data.calculated_at` | `string` | Timestamp ISO 8601 de quando foi calculado |
| `data.period.start_date` | `string` | Data inicial do filtro (YYYY-MM-DD) |
| `data.period.end_date` | `string` | Data final do filtro (YYYY-MM-DD) |
| `error` | `object` \| `null` | Objeto de erro ou null se sucesso |
| `error.code` | `string` | Código do erro (ex: INVALID_USER_ID) |
| `error.message` | `string` | Mensagem descritiva do erro |
| `error.status_code` | `int` | HTTP status code |

---

## Response Examples

### Example 1: Success - Progress with Tasks

```json
{
  "success": true,
  "data": {
    "user_id": 42,
    "subject_id": 7,
    "subject_name": "Física I",
    "progress_percentage": 73.68,
    "tasks": {
      "completed": 14,
      "pending": 4,
      "in_progress": 1,
      "overdue": 0,
      "total": 19
    },
    "calculated_at": "2026-05-26T15:45:30Z",
    "period": {
      "start_date": null,
      "end_date": null
    }
  },
  "error": null
}
```

### Example 2: Success - No Tasks (0% Progress)

```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "subject_id": 999,
    "subject_name": "English Literature",
    "progress_percentage": 0,
    "tasks": {
      "completed": 0,
      "pending": 0,
      "in_progress": 0,
      "overdue": 0,
      "total": 0
    },
    "calculated_at": "2026-05-26T15:50:00Z",
    "period": {
      "start_date": null,
      "end_date": null
    }
  },
  "error": null
}
```

### Example 3: Success - All Completed (100% Progress)

```json
{
  "success": true,
  "data": {
    "user_id": 10,
    "subject_id": 3,
    "subject_name": "Chemistry",
    "progress_percentage": 100,
    "tasks": {
      "completed": 12,
      "pending": 0,
      "in_progress": 0,
      "overdue": 0,
      "total": 12
    },
    "calculated_at": "2026-05-26T16:00:00Z",
    "period": {
      "start_date": "2026-03-01",
      "end_date": "2026-05-26"
    }
  },
  "error": null
}
```

### Example 4: Error - User Not Found (400)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 99999 does not exist in the database",
    "status_code": 400
  }
}
```

### Example 5: Error - Subject Not Found (400)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "SUBJECT_NOT_FOUND",
    "message": "Subject with ID 77777 does not exist",
    "status_code": 400
  }
}
```

### Example 6: Error - Invalid Date Format (400)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_DATE_FORMAT",
    "message": "start_date must be in YYYY-MM-DD format, got: '26-05-2026'",
    "status_code": 400
  }
}
```

### Example 7: Error - Access Denied (403)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ACCESS_DENIED",
    "message": "User 5 does not have access to subject 12",
    "status_code": 403
  }
}
```

### Example 8: Error - Database Connection Error (500)

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "DATABASE_CONNECTION_ERROR",
    "message": "Failed to connect to Xano API: Connection timeout",
    "status_code": 500
  }
}
```

---

## Error Codes Reference

| Code | Status | Description |
|------|--------|-------------|
| `USER_NOT_FOUND` | 400 | user_id não existe no banco |
| `SUBJECT_NOT_FOUND` | 400 | subject_id não existe |
| `INVALID_DATE_FORMAT` | 400 | Formato de data inválido |
| `INVALID_DATE_RANGE` | 400 | start_date > end_date |
| `ACCESS_DENIED` | 403 | User não tem acesso à subject |
| `INVALID_USER_ID` | 400 | user_id não é um inteiro válido |
| `INVALID_SUBJECT_ID` | 400 | subject_id não é um inteiro válido |
| `DATABASE_CONNECTION_ERROR` | 500 | Erro na conexão com Xano |
| `DATABASE_QUERY_ERROR` | 500 | Erro ao executar query |
| `INTERNAL_ERROR` | 500 | Erro interno do servidor |

---

## Calculation Logic

### Progress Percentage Formula

```
progress_percentage = (completed_tasks / total_tasks) * 100
```

**Special Cases:**
- If `total_tasks == 0`, return `progress_percentage = 0`
- Round to 2 decimal places
- Never exceed 100%

### Task Status Definitions

| Status | Description |
|--------|-------------|
| `completed` | Task with status "completed" |
| `pending` | Task with status "pending" |
| `in_progress` | Task with status "in_progress" |
| `overdue` | Task with status "overdue" |

**Completion Rules:**
- Only tasks with status `"completed"` count toward completion
- Overdue tasks are counted as separate category
- In-progress tasks are NOT counted as completed

### Date Filtering Logic

```python
# If start_date or end_date provided:
tasks = filter(tasks, {
    "due_date >= start_date if start_date else True",
    "due_date <= end_date if end_date else True"
})
```

**Rules:**
- Date comparison is based on `due_date` field
- Both dates are INCLUSIVE
- If neither provided, no date filtering applied
- Date format: YYYY-MM-DD

---

## Implementation Notes

### Performance Considerations

- For users with 100+ tasks, consider pagination
- Index on `(user_id, subject_id, due_date)` recommended
- Cache results for 5-10 minutes if same user/subject queried frequently

### Security Considerations

- Always validate that user has access to requested subject
- Sanitize inputs before database queries
- Never expose internal error details to non-admin users
- Log all calculations for audit trail

### Data Consistency

- Use database transactions for multi-step operations
- Handle race conditions if tasks updated during calculation
- Ensure timestamps are consistent (UTC/ISO 8601)

---

## Testing Checklist

- [ ] Calculate with all tasks in progress
- [ ] Calculate with mix of statuses
- [ ] Calculate with no tasks (0%)
- [ ] Calculate with all completed (100%)
- [ ] Calculate with date range that excludes all tasks
- [ ] Validate error handling for missing user
- [ ] Validate error handling for missing subject
- [ ] Validate JSON response format
- [ ] Validate timestamp format (ISO 8601)
- [ ] Validate percentage calculation accuracy
