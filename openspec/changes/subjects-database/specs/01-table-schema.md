# Subjects Database - Table Specification

## Xano Table Definition: subject

### Field Specifications

| Field | Type | Required | Primary Key | Foreign Key | Validation | Notes |
|-------|------|----------|-------------|-------------|-----------|-------|
| id | number | ✓ | ✓ | - | Auto-increment | Primary key |
| name | text | ✓ | - | - | Max 255 chars | Nome da disciplina |
| description | text | - | - | - | Max 2000 chars | Descrição e ementa |
| code | text | - | - | - | Max 50 chars, unique per account | Código como CCNA101 |
| owner_id | number | ✓ | - | user.id | Valid user ID | Proprietário da disciplina |
| account_id | number | ✓ | - | account.id | Valid account ID | Conta proprietária |
| credits | number | - | - | - | 0-20 | Créditos da disciplina |
| semester | text | - | - | - | Enum: 1o,2o,3o,... | Semestre do curso |
| year | number | - | - | - | 1900-2100 | Ano acadêmico |
| status | text | ✓ | - | - | Enum: active,archived,draft | Estado da disciplina |
| is_active | boolean | ✓ | - | - | default: true | Flag de atividade |
| created_at | datetime | ✓ | - | - | auto timestamp | Sistema |
| updated_at | datetime | ✓ | - | - | auto timestamp on update | Sistema |

### Indexes

- `idx_owner_id`: (owner_id) - Para queries rápidas por proprietário
- `idx_account_id`: (account_id) - Para queries rápidas por conta
- `idx_account_code`: (account_id, code) - Para unicidade de code por conta
- `idx_status`: (status) - Para filtros de status

### Constraints

- `owner_id` referencia `user.id` - deve existir
- `account_id` referencia `account.id` - deve existir
- `code` deve ser único por `account_id`
- `status` limitado aos valores definidos
- `credits` deve ser >= 0
- `year` deve ser um ano válido

### Triggers

- **OnCreate**: Registrar evento `subject.created` na tabela event_logs
- **OnUpdate**: Registrar evento `subject.updated` na tabela event_logs
- **OnDelete**: Registrar evento `subject.deleted` na tabela event_logs e aplicar soft-delete se configurado
