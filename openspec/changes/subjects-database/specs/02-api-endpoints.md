# Subjects Database - API Specification

## REST API Endpoints

### 1. List User's Subjects

**Endpoint**: `GET /subjects/my`
**Auth**: Required
**Role**: User, Admin
**Description**: Listar todas as disciplinas do usuário autenticado

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": 1,
      "name": "Cálculo I",
      "code": "MAT101",
      "description": "Introdução ao Cálculo Diferencial",
      "owner_id": 123,
      "account_id": 456,
      "credits": 4,
      "semester": "1o",
      "year": 2024,
      "status": "active",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 20,
    "offset": 0
  }
}
```

### 2. Get Subject by ID

**Endpoint**: `GET /subjects/:id`
**Auth**: Required
**Role**: User (if owner), Admin
**Description**: Obter detalhes de uma disciplina específica

**Response** (200 OK):
```json
{
  "data": {
    "id": 1,
    "name": "Cálculo I",
    ...
  }
}
```

**Error** (403 Forbidden):
- User não é owner e não é admin da conta

**Error** (404 Not Found):
- Subject não encontrado

### 3. Create Subject

**Endpoint**: `POST /subjects`
**Auth**: Required
**Role**: User, Admin
**Description**: Criar uma nova disciplina

**Request Body**:
```json
{
  "name": "Cálculo I",
  "description": "Introdução ao Cálculo Diferencial",
  "code": "MAT101",
  "account_id": 456,
  "credits": 4,
  "semester": "1o",
  "year": 2024,
  "status": "active"
}
```

**Response** (201 Created):
```json
{
  "data": {
    "id": 1,
    "name": "Cálculo I",
    "owner_id": 123,
    ...
  }
}
```

**Validation**:
- `name`: Required, max 255 chars
- `account_id`: Required, must be valid and user must have access
- `code`: Optional, max 50 chars, unique within account
- `status`: Enum validation
- `credits`: Must be >= 0
- `year`: Valid year range

### 4. Update Subject

**Endpoint**: `PATCH /subjects/:id`
**Auth**: Required
**Role**: Owner, Admin
**Description**: Atualizar uma disciplina

**Request Body** (partial):
```json
{
  "name": "Cálculo I - Avançado",
  "credits": 5
}
```

**Response** (200 OK):
```json
{
  "data": {
    "id": 1,
    "name": "Cálculo I - Avançado",
    "credits": 5,
    "updated_at": "2024-01-20T14:30:00Z"
  }
}
```

**Error** (403 Forbidden):
- User não é owner e não é admin

### 5. Delete Subject

**Endpoint**: `DELETE /subjects/:id`
**Auth**: Required
**Role**: Owner, Admin
**Description**: Deletar uma disciplina

**Response** (204 No Content)

**Note**: Se soft-delete habilitado, apenas marca como inativo

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| SUBJECT_NOT_FOUND | 404 | Disciplina não encontrada |
| SUBJECT_FORBIDDEN | 403 | Acesso negado |
| ACCOUNT_INVALID | 400 | Account inválida |
| ACCOUNT_NOT_FOUND | 404 | Account não encontrada |
| CODE_DUPLICATE | 400 | Código de disciplina já existe na conta |
| VALIDATION_ERROR | 400 | Erro de validação dos dados |
