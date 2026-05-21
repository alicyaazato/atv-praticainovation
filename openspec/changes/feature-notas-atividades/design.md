# Activity Grades - Technical Design

## Overview

Sistema de lançamento de notas que integra atividades acadêmicas, usuários (alunos e professores) e contas, com suporte a auditoria e RBAC.

## Database Schema

### Table: `activity_grade`

```
Field               Type              Constraints                    Purpose
─────────────────────────────────────────────────────────────────────────────────
id                  int               PRIMARY KEY, auto-increment    Identificador único
account_id          int (FK → account)  NOT NULL, indexed            Isolamento multi-tenant
activity_id         int (FK → academic_task)  NOT NULL, indexed      Referência à atividade
student_id          int (FK → user)   NOT NULL, indexed            Aluno que receberá a nota
professor_id        int (FK → user)   NOT NULL, indexed            Professor que dá a nota
grade               decimal(5,2)      NOT NULL, range [0.0, 10.0]  Valor numérico da nota
feedback            text              nullable                      Comentários/feedback do professor
status              text              default="submitted"           Estado (submitted, reviewed, disputed)
is_active           boolean           default=true                  Soft-delete flag
created_at          datetime          NOT NULL, auto               Timestamp de criação
updated_at          datetime          NOT NULL, auto               Timestamp de atualização
created_by          int (FK → user)   NOT NULL                     Quem criou (auditoria)
updated_by          int (FK → user)   NOT NULL                     Quem atualizou (auditoria)
```

### Indexes (Performance)

```
CREATE INDEX idx_account_id ON activity_grade(account_id)
CREATE INDEX idx_activity_id ON activity_grade(activity_id)
CREATE INDEX idx_student_id ON activity_grade(student_id)
CREATE INDEX idx_professor_id ON activity_grade(professor_id)
CREATE INDEX idx_activity_student ON activity_grade(activity_id, student_id) -- UNIQUE constraint for single grade per student per activity
```

### Foreign Key Relationships

```
activity_grade.account_id      → account.id         (ON DELETE RESTRICT)
activity_grade.activity_id     → academic_task.id   (ON DELETE RESTRICT)
activity_grade.student_id      → user.id            (ON DELETE RESTRICT)
activity_grade.professor_id    → user.id            (ON DELETE RESTRICT)
activity_grade.created_by      → user.id            (ON DELETE RESTRICT)
activity_grade.updated_by      → user.id            (ON DELETE RESTRICT)
```

### Unique Constraints

```
UNIQUE(account_id, activity_id, student_id)  -- Um aluno recebe uma nota por atividade
```

## API Endpoints

### REST Endpoints

```
GET    /activity-grades                    - Listar notas (admin) ou minhas notas lançadas (professor)
POST   /activity-grades                    - Criar nota (professor lança)
GET    /activity-grades/{id}               - Consultar nota específica
PATCH  /activity-grades/{id}               - Atualizar nota (professor ou admin)
DELETE /activity-grades/{id}               - Deletar nota (professor ou admin)
GET    /activity-grades/my-grades          - Listar minhas notas (aluno - notas que recebi)
GET    /activity-grades/activity/{id}      - Listar todas as notas de uma atividade (professor ou admin)
```

## Access Control (RBAC)

### Permission Matrix

```
Action               Professor (owner)    Professor (other)    Admin       Student
─────────────────────────────────────────────────────────────────────────────────
Create grade         ✅ (in own activity) ❌                 ✅          ❌
Read own grade       ✅                   ✅ (if no feedback)  ✅          ✅ (own)
Update grade         ✅ (in own activity) ❌                 ✅          ❌
Delete grade         ✅ (in own activity) ❌                 ✅          ❌
Admin view all       ❌                   ❌                 ✅          ❌
```

### Validation Rules

1. **Student não pode ser o próprio professor**: student_id ≠ professor_id
2. **Nota deve estar entre 0.0 e 10.0**: 0.0 ≤ grade ≤ 10.0
3. **Feedback é opcional**: text field, nullable
4. **Atividade deve existir e estar ativa**: activity_id must reference active task
5. **Professor deve ser owner da activity (via subject)**: Verificar propriedade transitiva
6. **Multi-tenant**: account_id deve corresponder ao account do usuário autenticado

## Event Logging Integration

Todas as operações devem logar em `event_log`:

```
Event Type               Trigger         Metadata Recorded
──────────────────────────────────────────────────────────────
activity_grade_created   POST            {activity_id, student_id, grade, professor_id}
activity_grade_updated   PATCH           {activity_id, grade_old, grade_new, feedback_old, feedback_new}
activity_grade_deleted   DELETE          {activity_id, student_id, grade}
```

## Data Validation & Error Handling

| Scenario                                | HTTP Status | Error Code |
|-----------------------------------------|------------|-----------|
| Nota já existe para aluno+atividade     | 409        | DUPLICATE_GRADE |
| Professor não é dono da atividade      | 403        | FORBIDDEN |
| Valor de nota fora do range            | 400        | INVALID_GRADE_VALUE |
| Estudante não encontrado               | 404        | STUDENT_NOT_FOUND |
| Atividade não encontrada               | 404        | ACTIVITY_NOT_FOUND |
| Acesso negado (não é professor)        | 403        | UNAUTHORIZED |
| Dados obrigatórios faltando            | 400        | REQUIRED_FIELDS_MISSING |

## Security Considerations

1. **Input Validation**: Todos os inputs devem ser validados (type, length, range)
2. **SQL Injection Prevention**: Use parameterized queries (Xano natively)
3. **Authorization**: Verificar professor_id == auth.user_id ou role == admin
4. **Multi-tenant Isolation**: Filtrar sempre por account_id do usuário autenticado
5. **Auditoria**: Log de created_by/updated_by em cada operação
6. **Rate Limiting**: Preparar para futuras proteções (não implementar agora)

## Scalability & Performance

- **Expected Volume**: 1000s de notas por conta
- **Query Optimization**: Indexes sobre activity_id, student_id, professor_id
- **Pagination**: Implementar limit/offset em GET /activity-grades (default: 50)
- **Soft Delete**: Usar is_active=false em vez de hard delete

## Migration Path

### Phase 1 (Now)
- Criar tabela activity_grade
- Criar 5 endpoints CRUD
- Implementar RBAC e event logging

### Phase 2 (Future)
- Adicionar triggers para auditoria (auto-managed timestamps)
- Criar função agregadora de médias
- Implementar notificações por email
- Adicionar endpoints de dashboard/estatísticas
