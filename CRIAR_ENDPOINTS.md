# 🔌 Criar 5 Endpoints REST no Xano

**Status:** ✅ Tabela "subject" criada  
**Próximo:** Criar endpoints  
**Tempo:** ~15 minutos  

---

## 📍 Você está em: https://app.xano.io

---

## 🎯 PREPARAÇÃO: Abrir REST API Builder

```
1. Menu ESQUERDO → REST API (ou ícone de API)
2. Procure na lista por: "Endpoints"
3. Clique: "+ New Endpoint"
```

**Você vai criar 5 endpoints:**

| ID | Método | Rota | Ação |
|-------|--------|------|------|
| 3600550 | GET | /subjects/my | Listar subjects do usuário |
| 3600551 | GET | /subjects/{id} | Obter subject específico |
| 3600552 | POST | /subjects | Criar subject |
| 3600553 | PATCH | /subjects/{id} | Atualizar subject |
| 3600554 | DELETE | /subjects/{id} | Deletar subject (soft delete) |

---

## 🎯 ENDPOINT 1: GET /subjects/my (Listar)

```
1. Clique: "+ New Endpoint"
2. Método: GET
3. Rota: /subjects/my
4. Clique: "Create"
```

### Configurar Endpoint

**Na seção "Variables" (canto superior esquerdo):**

```
Query Parameters:
  ☐ limit (Type: Number, Default: 10)
  ☐ offset (Type: Number, Default: 0)
  ☐ status (Type: Text, Optional)
  ☐ semester (Type: Text, Optional)
  ☐ year (Type: Number, Optional)
```

**Na seção "Logic/Response" (parte principal):**

```
1. Clique: "+ Add Action"
2. Procure por: "Database" → "Query Records"
3. Selectione: Table "subject"
4. Configure:
   ☐ WHERE owner_id = {auth.user_id}
   ☐ If status parameter → AND status = {status}
   ☐ If year parameter → AND year = {year}
   ☐ LIMIT {limit}
   ☐ OFFSET {offset}
   ☐ ORDER BY created_at DESC

5. Clique: "Save"
```

**Resultado esperado:** Retorna array de subjects do usuário autenticado

---

## 🎯 ENDPOINT 2: GET /subjects/{id} (Obter Específico)

```
1. Clique: "+ New Endpoint"
2. Método: GET
3. Rota: /subjects/{id}
4. Clique: "Create"
```

### Configurar Endpoint

**Na seção "Variables":**

```
URL Parameter:
  ☐ id (Type: Number, Required)
```

**Na seção "Logic/Response":**

```
1. Clique: "+ Add Action"
2. Query Records → Table "subject"
3. WHERE id = {id}

2. Clique: "+ Add Action"
3. "Condition": IF record.owner_id != {auth.user_id} AND {auth.user.role} != "admin"
   → THEN: Return Error 403 "Access Denied"
   
4. ELSE: Return record

5. Clique: "Save"
```

**Resultado esperado:** 
- ✅ Se é owner: retorna 200 + subject
- ✅ Se é admin: retorna 200 + subject
- ✅ Se outro usuário: retorna 403 Forbidden

---

## 🎯 ENDPOINT 3: POST /subjects (Criar)

```
1. Clique: "+ New Endpoint"
2. Método: POST
3. Rota: /subjects
4. Clique: "Create"
```

### Configurar Endpoint

**Na seção "Body" (JSON input):**

```
Defina o schema:
{
  "name": "string (required, max:255)",
  "code": "string (optional, max:50)",
  "description": "string (optional, max:2000)",
  "credits": "number (optional, 0-20)",
  "semester": "string (optional)",
  "year": "number (optional)",
  "status": "string (optional, default: active)"
}
```

**Na seção "Logic/Response":**

```
1. Clique: "+ Add Action"
2. Validations:
   ☐ IF name is empty → Return Error 400 "Name required"
   ☐ IF credits < 0 or credits > 20 → Return Error 400 "Invalid credits"
   ☐ IF code provided AND code already exists for this account → Return Error 409 "Code already exists"

3. Clique: "+ Add Action"
4. Database → "Create Record"
5. Table: subject
6. Configure os valores:
   ☐ name: {body.name}
   ☐ code: {body.code}
   ☐ description: {body.description}
   ☐ credits: {body.credits}
   ☐ semester: {body.semester}
   ☐ year: {body.year}
   ☐ status: {body.status} or "active"
   ☐ owner_id: {auth.user_id} (AUTO-SET - o user que criou é o dono)
   ☐ account_id: {auth.user.account_id} (AUTO-SET - conta do user)
   ☐ is_active: true (default)

7. Clique: "Save"
```

**Resultado esperado:** Retorna 201 Created + novo subject

---

## 🎯 ENDPOINT 4: PATCH /subjects/{id} (Atualizar)

```
1. Clique: "+ New Endpoint"
2. Método: PATCH
3. Rota: /subjects/{id}
4. Clique: "Create"
```

### Configurar Endpoint

**Na seção "Variables":**

```
URL Parameter:
  ☐ id (Type: Number, Required)

Body (partial update):
{
  "name": "string (optional)",
  "code": "string (optional)",
  "description": "string (optional)",
  "credits": "number (optional)",
  "semester": "string (optional)",
  "year": "number (optional)",
  "status": "string (optional)"
}
```

**Na seção "Logic/Response":**

```
1. Query subject by id
2. IF subject doesn't exist → Return 404

3. Check RBAC:
   IF subject.owner_id != {auth.user_id} AND {auth.user.role} != "admin"
   → Return 403 "Access Denied"

4. Update record:
   ☐ if body.name provided → update name
   ☐ if body.code provided → update code
   ☐ if body.status provided → update status
   (... other fields similarly)
   ☐ updated_at: NOW (auto via trigger)

5. Return 200 + updated subject
```

**Resultado esperado:** Retorna 200 OK + subject atualizado

---

## 🎯 ENDPOINT 5: DELETE /subjects/{id} (Deletar - Soft Delete)

```
1. Clique: "+ New Endpoint"
2. Método: DELETE
3. Rota: /subjects/{id}
4. Clique: "Create"
```

### Configurar Endpoint

**Na seção "Variables":**

```
URL Parameter:
  ☐ id (Type: Number, Required)
```

**Na seção "Logic/Response":**

```
1. Query subject by id
2. IF subject doesn't exist → Return 404

3. Check RBAC:
   IF subject.owner_id != {auth.user_id} AND {auth.user.role} != "admin"
   → Return 403 "Access Denied"

4. Soft Delete (via trigger):
   Database → Update Record
   ☐ Table: subject
   ☐ WHERE id = {id}
   ☐ SET is_active = false
   ☐ Trigger automatically logs to event_log

5. Return 204 No Content (vazio)
```

**Resultado esperado:** Retorna 204 (sucesso sem body)

---

## ✅ RESUMO DOS 5 ENDPOINTS

```
✅ GET /subjects/my (3600550)
   └─ Lista subjects do usuário (paginação + filtros)
   
✅ GET /subjects/{id} (3600551)
   └─ Obter subject com RBAC (owner/admin can access)
   
✅ POST /subjects (3600552)
   └─ Criar subject (auto-set owner_id e account_id)
   
✅ PATCH /subjects/{id} (3600553)
   └─ Atualizar partial (com RBAC)
   
✅ DELETE /subjects/{id} (3600554)
   └─ Soft delete via trigger (com RBAC)
```

---

## 📊 Fluxo de Autenticação

Todos os 5 endpoints precisam de:

```
Header: Authorization: Bearer {token}

Onde {token} contém:
- auth.user_id (ID do usuário)
- auth.user.role (admin, member, owner, etc)
- auth.user.account_id (conta do usuário)
```

---

## 🎯 PRÓXIMO PASSO

Quando terminar de criar os 5 endpoints:

1. **Confirme aqui:** "5 endpoints criados! ✅"
2. **Depois vamos criar:**
   - 6 Triggers (para auditoria e soft delete)
   - 1 Função RBAC (check_subject_access)

---

## ⏱️ CHECKLIST

```
ENDPOINTS:
☐ GET /subjects/my (lista com paginação)
☐ GET /subjects/{id} (com RBAC)
☐ POST /subjects (criar com validação)
☐ PATCH /subjects/{id} (atualizar com RBAC)
☐ DELETE /subjects/{id} (soft delete com RBAC)

TOTAL: 5 endpoints ✅
```

---

**Quando terminar, diga: "5 endpoints criados!" ✅**
