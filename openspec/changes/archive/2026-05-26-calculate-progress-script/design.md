# Calculate Progress Script - Design

## Architecture Overview

O script `calculate_progress.py` será um módulo reutilizável que centraliza a lógica de cálculo de progresso. Será integrado com o banco de dados Xano e poderá ser chamado por:
- APIs de relatórios
- Funções de background processing
- Aplicação Streamlit (pages)
- Scripts de análise

## Core Function

### `calculate_progress(user_id: int, subject_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict`

**Entrada:**
```json
{
  "user_id": 1,
  "subject_id": 5,
  "start_date": "2026-01-01",  // opcional
  "end_date": "2026-05-26"      // opcional
}
```

**Saída (JSON):**
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

## Data Flow

```
Input Validation
    ↓
Query Database (Xano API or local)
    ↓
Fetch academic_tasks by user_id, subject_id, date_range
    ↓
Count tasks by status
    ↓
Calculate progress_percentage = (completed / total) * 100
    ↓
Build result JSON
    ↓
Return response
```

## Error Handling

| Caso | Status | Response |
|------|--------|----------|
| `user_id` não existe | 400 | `{"success": false, "error": "User not found"}` |
| `subject_id` não existe | 400 | `{"success": false, "error": "Subject not found"}` |
| Sem tarefas para o período | 200 | `{"progress_percentage": 0, "tasks": {"total": 0}}` |
| user não tem acesso à subject | 403 | `{"success": false, "error": "Access denied"}` |
| Data inválida | 400 | `{"success": false, "error": "Invalid date format"}` |
| Erro na conexão com DB | 500 | `{"success": false, "error": "Database connection error"}` |

## Edge Cases

| Cenário | Comportamento |
|---------|---------------|
| Sem tarefas (`total = 0`) | Retorna `progress_percentage: 0` e avisa no JSON |
| Todas concluídas | Retorna `progress_percentage: 100` |
| Tarefas atrasadas (overdue) | Conta como "pendente" ainda não concluída |
| Date range inválido (start > end) | Retorna erro 400 |
| Sem date range | Usa todas as tarefas do usuário na subject |

## Database Query

O script fará query na tabela `academic_task`:

```sql
SELECT 
  status,
  COUNT(*) as count
FROM academic_task
WHERE 
  user_id = $1
  AND subject_id = $2
  AND (start_date IS NULL OR due_date >= start_date)
  AND (end_date IS NULL OR due_date <= end_date)
GROUP BY status
```

## Integration Points

- **Xano API**: Chamadas via `requests` ou SDK Xano
- **Streamlit Pages**: `pages/2_📝_Tarefas.py` pode usar para mostrar barra de progresso
- **APIs Future**: `/api/progress` endpoint pode chamar esta função
- **Reports**: Relatórios de desempenho podem agregar múltiplos usuários/disciplinas

## File Structure

```
scripts/
├── calculate_progress.py      # Script principal
├── __init__.py               # Package init
├── utils/
│   ├── database.py           # Database connection helpers
│   └── validators.py         # Input validation
└── tests/
    └── test_calculate_progress.py  # Unit tests
```

## Dependencies

```
requests>=2.28.0    # HTTP calls to Xano
python-dateutil>=2.8.0  # Date parsing e manipulation
pydantic>=1.9.0     # Data validation
```
