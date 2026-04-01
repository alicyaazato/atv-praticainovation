# Subjects Database - Event Logging Specification

## Event Logging Requirements

Todas as operações sobre subjects devem gerar eventos na tabela `event_logs` para auditoria e rastreamento.

### Event Categories

#### 1. subject.created
**Trigger**: Quando um novo subject é criado
**Event Type**: CREATE
**Actor**: user_id do criador (owner)
**Description**: Disciplina criada com sucesso

**Payload Example**:
```json
{
  "event": "subject.created",
  "subject_id": 1,
  "subject_name": "Cálculo I",
  "account_id": 456,
  "owner_id": 123,
  "details": {
    "code": "MAT101",
    "credits": 4,
    "status": "active"
  }
}
```

#### 2. subject.updated
**Trigger**: Quando um subject é modificado
**Event Type**: UPDATE
**Actor**: user_id do editor
**Description**: Disciplina atualizada

**Payload Example**:
```json
{
  "event": "subject.updated",
  "subject_id": 1,
  "account_id": 456,
  "changes": {
    "credits": { "from": 4, "to": 5 },
    "status": { "from": "draft", "to": "active" }
  }
}
```

#### 3. subject.deleted
**Trigger**: Quando um subject é deletado
**Event Type**: DELETE
**Actor**: user_id do deletor
**Description**: Disciplina removida

**Payload Example**:
```json
{
  "event": "subject.deleted",
  "subject_id": 1,
  "subject_name": "Cálculo I",
  "account_id": 456,
  "reason": "manual_deletion"
}
```

#### 4. subject.accessed
**Trigger**: Quando um subject é acessado (GET)
**Event Type**: READ
**Actor**: user_id que acessou
**Description**: Disciplina visualizada

**Payload Example**:
```json
{
  "event": "subject.accessed",
  "subject_id": 1,
  "account_id": 456,
  "accessor_role": "owner"
}
```

### Implementation

#### Xano Triggers

- **Before INSERT**: Validar integridade referencial
- **After INSERT**: Chamar função create_event_log com tipo subject.created
- **Before UPDATE**: Capturar valores antigos para comparação
- **After UPDATE**: Chamar função create_event_log com tipo subject.updated com diff
- **Before DELETE**: Capturar dados do subject
- **After DELETE**: Chamar função create_event_log com tipo subject.deleted

#### API Middleware

- **After GET /subjects/:id**: Chamar função create_event_log com tipo subject.accessed
- **After GET /subjects/my**: Log aggregado (opcional, pode ser pesado)

### Event Log Fields

Usar estrutura existente de event_logs:

```
- id: number (PK)
- user_id: number (FK to user)
- account_id: number (FK to account)
- event_type: string (CREATE|UPDATE|DELETE|READ)
- object_type: string = "subject"
- object_id: number (subject.id)
- details: json (payload com informações específicas)
- ip_address: string (opcional)
- user_agent: string (opcional)
- created_at: datetime (auto timestamp)
```

### Access to Event Logs

- **Account Admin**: Pode visualizar todos os eventos da conta
- **User**: Pode visualizar eventos de suas próprias disciplinas
- **Owner**: Pode visualizar eventos de suas disciplinas

Usar endpoint existente: `GET /logs/admin/account/events` com filtros
