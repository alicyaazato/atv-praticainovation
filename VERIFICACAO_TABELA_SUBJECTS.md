# ✅ Verificação de Deploy - Tabela Subjects

**Data:** 2026-04-01  
**Status:** Em Verificação  
**Responsável:** User  

---

## 📋 Checklist de Verificação

### ✅ 1. Tabela Criada em Xano

**O que verificar em https://app.xano.io:**

```
1. Database → Tables
2. Procure por "subject" (ID: 753426)
3. Confirme os seguintes campos:
```

| Campo | Tipo | Obrigatório | Validação | Status |
|-------|------|-------------|-----------|--------|
| id | Primary Key (Auto) | Sim | Auto increment | ☐ |
| name | Text | Sim | max:255 | ☐ |
| code | Text | Não | max:50, unique per account | ☐ |
| description | Text | Não | max:2000 | ☐ |
| semester | Text | Não | pattern: ^[0-9]º$ | ☐ |
| year | Number | Não | min:1900, max:2100 | ☐ |
| credits | Number | Não | min:0, max:20 | ☐ |
| status | Enum | Sim | ["active", "archived", "draft"] | ☐ |
| is_active | Boolean | Não | default: true | ☐ |
| owner_id | Link to Users | Sim | Foreign Key → user.id | ☐ |
| account_id | Link to Accounts | Sim | Foreign Key → account.id | ☐ |
| created_at | Timestamp | Auto | auto: now, private | ☐ |
| updated_at | Timestamp | Auto | auto: now, private | ☐ |
| metadata | JSON | Não | private | ☐ |

**Total obrigatório: 14 campos**

---

### ✅ 2. Relacionamentos Verificados

**Verificar em Database → Tables → subject:**

```
1. owner_id → DEVE REFERENCIAR:
   ☐ Tabela: users
   ☐ Campo: id
   ☐ Tipo: Foreign Key
   ☐ Obrigatório: SIM

2. account_id → DEVE REFERENCIAR:
   ☐ Tabela: accounts
   ☐ Campo: id
   ☐ Tipo: Foreign Key
   ☐ Obrigatório: SIM
```

---

### ✅ 3. Indexes Criados

**Verificar em Database → Tables → subject → Indexes:**

```
☐ idx_primary_id (Primary Key)
☐ idx_created_at (created_at DESC)
☐ idx_updated_at (updated_at DESC)
☐ idx_owner_id (owner_id ASC) - Para filtros por dono
☐ idx_account_id (account_id ASC) - Para multi-tenant isolation
☐ idx_account_code (account_id + code UNIQUE) - Para unicidade por conta
☐ idx_status (status ASC) - Para filtros por status
☐ idx_metadata (JSON GIN index) - Para busca em metadata
```

**Total: 8 indexes**

---

### ✅ 4. Triggers Criados

**Verificar em Database → Triggers:**

```
Procure por triggers da tabela "subject":

☐ BEFORE INSERT subject
   └─ Valida Foreign Keys (owner_id, account_id)
   
☐ AFTER INSERT subject
   └─ Log evento: entity="subject", action="created"
   
☐ BEFORE UPDATE subject
   └─ Auto-atualiza updated_at
   
☐ AFTER UPDATE subject
   └─ Log evento: entity="subject", action="updated"
   
☐ BEFORE DELETE subject
   └─ Soft delete: set is_active = false (nunca remove registro)
   
☐ AFTER DELETE subject
   └─ Log evento: entity="subject", action="deleted"
```

**Total: 6 triggers**

---

### ✅ 5. Endpoints Criados

**Verificar em REST API → Endpoints:**

```
☐ 3600550 - GET /subjects/my
   └─ Lista subjects do usuário autenticado (paginação)
   └─ Filtros: status, semester, year, limit, offset
   └─ Retorna: Array de subjects

☐ 3600551 - GET /subjects/{id}
   └─ Retorna subject específico com RBAC
   └─ Checagem: Erro 403 se não é owner/admin
   └─ Retorna: 404 se não existe ou soft-deletado

☐ 3600552 - POST /subjects
   └─ Cria novo subject
   └─ Auto-set owner_id = auth.user_id
   └─ Validação completa de campos
   └─ Retorna: 201 + subject criado

☐ 3600553 - PATCH /subjects/{id}
   └─ Atualiza fields parciais
   └─ RBAC: Só owner ou admin
   └─ Auto-update: updated_at
   └─ Retorna: 200 + subject atualizado

☐ 3600554 - DELETE /subjects/{id}
   └─ Soft delete (via trigger: is_active = false)
   └─ RBAC: Só owner ou admin
   └─ Retorna: 204 No Content

☐ API Group: Subjects
   └─ Organiza os 5 endpoints acima
```

**Total: 5 endpoints + 1 API Group**

---

### ✅ 6. Função RBAC Criada

**Verificar em Functions:**

```
☐ check_subject_access (ID: 269538)
   └─ Parâmetros: subject_id, user_id, account_id
   └─ Retorna: 
      • true se: owner_id == user_id
      • true se: user.role == "admin"
      • false se: outro usuário
   └─ Usado em: GET /subjects/{id}, PATCH, DELETE

Lógica:
1. SELECT subject WHERE id = subject_id
2. IF subject.owner_id == auth.user_id → ALLOW (200)
3. IF auth.user.role == "admin" → ALLOW (200)
4. ELSE → DENY (403 Forbidden)
5. IF subject não existe → 404 Not Found
```

---

## 🧪 Testes Pós-Deploy

### Teste 1: Criar Subject
```
POST /subjects
{
  "name": "Matemática Avançada",
  "code": "MAT310",
  "description": "Cálculo avançado e análise",
  "credits": 4,
  "semester": "3º",
  "year": 2024,
  "status": "active"
}

Resultado esperado:
- Status: 201 Created
- owner_id: auto-preenchido (auth.user_id)
- created_at: auto-preenchido
- id: retornado
```

### Teste 2: Listar Subjects
```
GET /subjects/my?limit=10&offset=0

Resultado esperado:
- Status: 200 OK
- Retorna array de subjects do usuário
- Filtra por owner_id automaticamente
```

### Teste 3: Obter Subject Específico
```
GET /subjects/{id}

Resultado esperado:
- Se owner: Status 200 OK + subject
- Se outro usuário: Status 403 Forbidden
- Se não existe: Status 404 Not Found
```

### Teste 4: Atualizar Subject
```
PATCH /subjects/{id}
{
  "status": "archived"
}

Resultado esperado:
- Se owner: Status 200 OK + subject atualizado
- updated_at: auto-atualizado
```

### Teste 5: Deletar Subject (Soft Delete)
```
DELETE /subjects/{id}

Resultado esperado:
- Status: 204 No Content
- is_active: false (soft delete, não remove)
- event_log: novo entrada com action="deleted"
- GET /subjects/{id}: retorna 404 (porque is_active=false filtra)
```

---

## 📊 Verificação de Conformidade

Comparar com specification:

| Item | Specification | Implementação | Status |
|------|----------------|---------------|--------|
| Tabela | 14 campos definidos | ✅ 753426_subject.xs | ☐ |
| FK owner_id | → users table | ✅ owner_id field | ☐ |
| FK account_id | → accounts table | ✅ account_id field | ☐ |
| RBAC | 3 levels (owner/admin/member) | ✅ check_subject_access | ☐ |
| Soft Delete | is_active = false | ✅ BEFORE DELETE trigger | ☐ |
| Event Log | 6 eventos (CRUD) | ✅ 6 triggers | ☐ |
| Endpoints | 5 CRUD operations | ✅ 3600550-3600554 | ☐ |
| Validation | 8+ tipos de validação | ✅ name, code, credits, etc | ☐ |
| Indexes | 8 indexes otimizados | ✅ incluindo unique, GIN | ☐ |

---

## 📝 Checklist Final

```
TABELA E ESTRUTURA:
☐ Tabela "subject" criada em Xano
☐ 14 campos presentes e configurados
☐ 8 indexes criados
☐ 6 triggers registrados
☐ 2 Foreign Keys funcionando (owner_id, account_id)

ENDPOINTS:
☐ 5 endpoints criados (GET/POST/PATCH/DELETE)
☐ Todos retornam status code correto
☐ RBAC implementado em GET/{id}, PATCH, DELETE

FUNCTIONS:
☐ check_subject_access criada e funcionando

CIÊNCIA:
☐ Dados em production
☐ Backups verificados
☐ Documentação atualizada

PRONTO PARA PRODUÇÃO:
☐ Testes executados
☐ RBAC validado
☐ Event logs funcionando
☐ Soft delete testado
```

---

## 📌 Próximos Passos

1. **AGORA:** Verificar cada item acima em https://app.xano.io
2. **DEPOIS:** Marcar ☐ conforme verifica
3. **FINAL:** Confirmar que tudo está:
   - ✅ Criado
   - ✅ Relacionado corretamente
   - ✅ Pronto para documentar no OpenSpec

---

**Status de Deploy:** 🟡 **Aguardando Verificação Manual em Xano**

Próxima ação: Você confirma que tabela foi criada? 👀
