# 📤 Upload dos 5 Endpoints para Xano

**Status:** ✅ Tabel subjects criada | 🔴 Endpoints precisam ser adicionados  
**Tempo:** ~20 minutos  
**Método:** Copiar XanoScript e colar no Xano UI  

---

## 📍 Você está em: https://app.xano.io

---

## 🎯 PASSO 1: Acessar REST API

```
1. Menu ESQUERDO → REST API (ou ícone de API)
2. Clique na seção: "Endpoints"
3. Procure: "+ New Endpoint" (botão azul)
```

---

## 🎯 ENDPOINT 1: GET /subjects/my (Listar)

### Copiar o Código:

**Arquivo:** `atv2Lab/apis/subjects/3600550_subjects_my_GET.xs`

```xanoscript
// List authenticated user's subjects
query "subjects/my" verb=GET {
  api_group = "Subjects"

  input {
    number limit = 20 filters=min:1|max:100
    number offset = 0 filters=min:0
    text status?
    text semester?
    number year?
  }

  stack {
    // Verify user is authenticated
    precondition ($auth.user_id) {
      error_type = "accessdenied"
      error = "Authentication required"
    }

    // Get user's account
    db.get user {
      field_name = "id"
      field_value = $auth.user_id
      output = ["account_id"]
    } as $user

    // Build filter conditions
    set $filter = {
      owner_id: $auth.user_id,
      account_id: $user.account_id
    }

    // Add optional filters
    if $input.status {
      set $filter.status = $input.status
    }

    if $input.semester {
      set $filter.semester = $input.semester
    }

    if $input.year {
      set $filter.year = $input.year
    }

    // Query subjects
    db.query subject {
      filter = $filter
      limit = $input.limit
      offset = $input.offset
      sort = [{field: "created_at", op: "desc"}]
      output = [
        "id", "name", "code", "description",
        "owner_id", "account_id", "credits",
        "semester", "year", "status", "is_active",
        "created_at", "updated_at"
      ]
    } as $subjects

    // Get total count
    db.count subject {
      filter = $filter
    } as $total_count
  }

  response = {
    data: $subjects.items
    pagination: {
      total: $total_count
      limit: $input.limit
      offset: $input.offset
    }
  }
  tags = ["xano:quick-start"]
}
```

### Adicionar em Xano:

```
1. Clique: "+ New Endpoint"
2. Método: GET
3. Path: /subjects/my
4. Clique: "Create"
5. Na seção "Code" (ou "XanoScript"), COLE o código acima
6. Clique: "Save"
```

**Resultado esperado:** ✅ Endpoint GET /subjects/my criado

---

## 🎯 ENDPOINT 2: GET /subjects/{id} (Obter Específico)

### Arquivo: 
`atv2Lab/apis/subjects/3600551_subjects_id_GET.xs`

```xanoscript
// Get a specific subject by ID with RBAC
query "subjects/{id}" verb=GET {
  api_group = "Subjects"

  input {
    number id
  }

  stack {
    // Verify user is authenticated
    precondition ($auth.user_id) {
      error_type = "accessdenied"
      error = "Authentication required"
    }

    // Get the subject
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Check if subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found"
    }

    // Get user details
    db.get user {
      field_name = "id"
      field_value = $auth.user_id
      output = ["role", "account_id"]
    } as $user

    // Check authorization: owner OR admin
    if ($subject.owner_id != $auth.user_id) && ($user.role != "admin") {
      error_type = "accessdenied"
      error = "Access denied"
      status = 403
    }
  }

  response = $subject
  tags = ["xano:quick-start"]
}
```

### Adicionar em Xano:

```
1. Clique: "+ New Endpoint"
2. Método: GET
3. Path: /subjects/{id}
4. Clique: "Create"
5. COLE o código acima
6. Clique: "Save"
```

**Resultado esperado:** ✅ Endpoint GET /subjects/{id} criado com RBAC

---

## 🎯 ENDPOINT 3: POST /subjects (Criar)

### Arquivo:
`atv2Lab/apis/subjects/3600552_subjects_POST.xs`

```xanoscript
// Create a new subject
query "subjects" verb=POST {
  api_group = "Subjects"

  input {
    text name
    text code?
    text description?
    number credits?
    text semester?
    number year?
    text status = "active"
  }

  stack {
    // Verify user is authenticated
    precondition ($auth.user_id) {
      error_type = "accessdenied"
      error = "Authentication required"
    }

    // Validation
    precondition ($input.name) {
      error_type = "badrequest"
      error = "Name is required"
    }

    precondition (strlen($input.name) >= 3 && strlen($input.name) <= 255) {
      error_type = "badrequest"
      error = "Name must be between 3 and 255 characters"
    }

    if $input.credits {
      precondition ($input.credits >= 0 && $input.credits <= 20) {
        error_type = "badrequest"
        error = "Credits must be between 0 and 20"
      }
    }

    // Get user details
    db.get user {
      field_name = "id"
      field_value = $auth.user_id
      output = ["account_id"]
    } as $user

    // Check if code already exists for this account (if provided)
    if $input.code {
      db.get subject {
        filter = {
          code: $input.code,
          account_id: $user.account_id
        }
      } as $existing

      precondition ($existing == null) {
        error_type = "conflict"
        error = "Code already exists for this account"
        status = 409
      }
    }

    // Create subject
    db.create subject {
      name: $input.name
      code: $input.code
      description: $input.description
      credits: $input.credits
      semester: $input.semester
      year: $input.year
      status: $input.status
      owner_id: $auth.user_id
      account_id: $user.account_id
      is_active: true
    } as $new_subject
  }

  response = $new_subject
  status = 201
  tags = ["xano:quick-start"]
}
```

### Adicionar em Xano:

```
1. Clique: "+ New Endpoint"
2. Método: POST
3. Path: /subjects
4. Clique: "Create"
5. COLE o código acima
6. Clique: "Save"
```

**Resultado esperado:** ✅ Endpoint POST /subjects criado com validação

---

## 🎯 ENDPOINT 4: PATCH /subjects/{id} (Atualizar)

### Arquivo:
`atv2Lab/apis/subjects/3600553_subjects_id_PATCH.xs`

```xanoscript
// Update a subject (partial update)
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"

  input {
    number id
    text name?
    text code?
    text description?
    number credits?
    text semester?
    number year?
    text status?
  }

  stack {
    // Verify user is authenticated
    precondition ($auth.user_id) {
      error_type = "accessdenied"
      error = "Authentication required"
    }

    // Get the subject
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Check if exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found"
    }

    // Get user details
    db.get user {
      field_name = "id"
      field_value = $auth.user_id
      output = ["role", "account_id"]
    } as $user

    // Check authorization: owner OR admin
    precondition (($subject.owner_id == $auth.user_id) || ($user.role == "admin")) {
      error_type = "accessdenied"
      error = "Access denied"
      status = 403
    }

    // Validate if name provided
    if $input.name {
      precondition (strlen($input.name) >= 3 && strlen($input.name) <= 255) {
        error_type = "badrequest"
        error = "Name must be between 3 and 255 characters"
      }
    }

    // Validate if credits provided
    if $input.credits {
      precondition ($input.credits >= 0 && $input.credits <= 20) {
        error_type = "badrequest"
        error = "Credits must be between 0 and 20"
      }
    }

    // Build update object
    set $update = {}
    if $input.name {
      set $update.name = $input.name
    }
    if $input.code {
      set $update.code = $input.code
    }
    if $input.description {
      set $update.description = $input.description
    }
    if $input.credits {
      set $update.credits = $input.credits
    }
    if $input.semester {
      set $update.semester = $input.semester
    }
    if $input.year {
      set $update.year = $input.year
    }
    if $input.status {
      set $update.status = $input.status
    }

    // Update subject
    db.update subject {
      filter = {id: $input.id}
      values = $update
    } as $updated_subject
  }

  response = $updated_subject
  status = 200
  tags = ["xano:quick-start"]
}
```

### Adicionar em Xano:

```
1. Clique: "+ New Endpoint"
2. Método: PATCH
3. Path: /subjects/{id}
4. Clique: "Create"
5. COLE o código acima
6. Clique: "Save"
```

**Resultado esperado:** ✅ Endpoint PATCH /subjects/{id} criado

---

## 🎯 ENDPOINT 5: DELETE /subjects/{id} (Deletar - Soft Delete)

### Arquivo:
`atv2Lab/apis/subjects/3600554_subjects_id_DELETE.xs`

```xanoscript
// Delete a subject (soft delete)
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"

  input {
    number id
  }

  stack {
    // Verify user is authenticated
    precondition ($auth.user_id) {
      error_type = "accessdenied"
      error = "Authentication required"
    }

    // Get the subject
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Check if exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found"
    }

    // Get user details
    db.get user {
      field_name = "id"
      field_value = $auth.user_id
      output = ["role"]
    } as $user

    // Check authorization: owner OR admin
    precondition (($subject.owner_id == $auth.user_id) || ($user.role == "admin")) {
      error_type = "accessdenied"
      error = "Access denied"
      status = 403
    }

    // Soft delete (mark as inactive)
    db.update subject {
      filter = {id: $input.id}
      values = {
        is_active: false
      }
    }
  }

  response = {}
  status = 204
  tags = ["xano:quick-start"]
}
```

### Adicionar em Xano:

```
1. Clique: "+ New Endpoint"
2. Método: DELETE
3. Path: /subjects/{id}
4. Clique: "Create"
5. COLE o código acima
6. Clique: "Save"
```

**Resultado esperado:** ✅ Endpoint DELETE /subjects/{id} criado com soft delete

---

## ✅ CHECKLIST FINAL

```
ENDPOINTS ADICIONADOS:
☐ GET /subjects/my (3600550) - Listar com paginação
☐ GET /subjects/{id} (3600551) - Obter com RBAC
☐ POST /subjects (3600552) - Criar com validação
☐ PATCH /subjects/{id} (3600553) - Atualizar com RBAC
☐ DELETE /subjects/{id} (3600554) - Soft delete com RBAC

TOTAL: 5 endpoints ✅

Próximo passo: Criar 6 Triggers para auditoria
```

---

## 🔧 OBTER OS CÓDIGOS PRONTOS

Todos os 5 endpoints já estão em:
```
atv2Lab/apis/subjects/
├── 3600550_subjects_my_GET.xs
├── 3600551_subjects_id_GET.xs
├── 3600552_subjects_POST.xs
├── 3600553_subjects_id_PATCH.xs
├── 3600554_subjects_id_DELETE.xs
└── api_group.xs
```

Você pode:
1. Abrir cada arquivo no VS Code
2. Copiar o conteúdo
3. Colar no Xano conforme as instruções acima

---

## 📝 RESUMO DO PROCESSO

```
PARA CADA ENDPOINT:

1. Xano → REST API → "+ New Endpoint"
2. Selecione Método (GET/POST/PATCH/DELETE)
3. Digite o Path (/subjects, /subjects/{id}, etc)
4. Clique "Create"
5. Na seção "Code/XanoScript", COLE o código
6. Clique "Save"
7. Pronto! ✅

Repetir para todos os 5 endpoints
```

---

## 🎯 Quando Terminar

Diga aqui: **"5 endpoints adicionados ao Xano! ✅"**

Depois vamos criar os **6 Triggers** para auditoria! 🚀
