# Academic Tasks Database - Design

## Architecture Overview

A tabela `academic_task` será uma entidade central que conecta tarefas acadêmicas aos usuários e disciplinas. A arquitetura segue padrões existentes de propriedade, auditoria e acesso.

## Data Model

### Table: academic_task

```
- id: number (primary key)
- title: string (required) - Título da tarefa
- description: string - Descrição detalhada da tarefa
- user_id: number (foreign key to user) - Usuário proprietário (aluno)
- subject_id: number (foreign key to subject) - Disciplina vinculada
- due_date: date - Data de vencimento da tarefa
- status: string (enum) - Estado da tarefa (pending, in_progress, completed, overdue)
- created_at: datetime - Timestamp de criação (auto)
- updated_at: datetime - Timestamp de atualização (auto)
```

## Relationships

```
academic_task.user_id -> user.id (aluno proprietário)
academic_task.subject_id -> subject.id (disciplina)
```

## Constraints

- **NOT NULL**: `title`, `user_id`, `subject_id`, `due_date`, `status`
- **Default**: `status = "pending"`, `created_at`, `updated_at`
- **Validation**: `due_date` must be valid date format

## Indexes

Para otimizar queries comuns:
- `user_id` - Listar tarefas por aluno
- `subject_id` - Listar tarefas por disciplina
- `status` - Filtrar por status
- `(user_id, status)` - Composite: tarefas pendentes do aluno
- `due_date` - Ordenar por data de vencimento

## Access Control

- **Owner**: Aluno proprietário pode editar, deletar e visualizar sua tarefa
- **Subject Owner**: Professor/owner da disciplina pode visualizar tarefas vinculadas
- **Account Admin**: Pode gerir todas as tarefas da conta
- **Other Users**: Sem acesso (privado do aluno)

## Event Logging

Todas as mudanças em `academic_task` geram eventos via `event_logs`:
- `academic_task.created` - Quando aluno cria uma nova tarefa
- `academic_task.updated` - Quando tarefa é modificada
- `academic_task.deleted` - Quando tarefa é removida
- `academic_task.status_changed` - Quando status muda (pendente → concluído, etc)

## Integration Points

1. **User Management**: Tarefas linkedadas a usuários proprietários
2. **Subject Management**: Tarefas vinculadas a disciplinas específicas
3. **Event Logging**: Auditoria automática de mudanças
4. **Future APIs**: CRUD endpoints para gerenciamento de tarefas
5. **Future Automations**: Notificações de prazos, relatórios de conclusão

## Status Lifecycle

```
pending
  ↓
in_progress (opcional)
  ├→ completed (sucesso)
  └→ overdue (falhou deadline)
```

**Regra**: Uma tarefa marcada como `overdue` por um cron job noturno se `due_date < today` e `status != completed`.
