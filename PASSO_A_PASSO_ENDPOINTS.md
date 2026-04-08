# 🚀 Adicionar 5 Endpoints no Xano - Passo a Passo Detalhado

**Status:** ✅ Tabela "subject" criada  
**Próximo:** ❌ Endpoints precisam ser adicionados  

---

## 🎯 RESUMO: O que você vai fazer

Você vai adicionar **5 endpoints REST** que já estão prontos em:
```
atv2Lab/apis/subjects/
├── 3600550_subjects_my_GET.xs
├── 3600551_subjects_id_GET.xs
├── 3600552_subjects_POST.xs
├── 3600553_subjects_id_PATCH.xs
├── 3600554_subjects_id_DELETE.xs
```

---

## 📍 PRIMEIRO: Preparar os Códigos

Abra VS Code e:

```
1. Vá em: atv2Lab/apis/subjects/
2. Você vai ver os 5 arquivos .xs
3. Ambra cada um (um por um) e copie o conteúdo
```

Ou, para economizar tempo, uso um método mais rápido:

```bash
# Terminal PowerShell
cd c:\Users\sayuri\Desktop\edutrack-ai
type atv2Lab\apis\subjects\3600550_subjects_my_GET.xs
# Copy o output
```

---

## 🎯 AGORA NO XANO:

### PASSO 1: Abrir Xano

```
1. Vá para: https://app.xano.io
2. Selecione seu workspace "edutrack-ai"
3. Clique: "Builder" (ícone de código)
```

### PASSO 2: Ir para REST API

```
Menu ESQUERDO:
├─ Database
├─ REST API ← CLIQUE AQUI
├─ Functions
└─ etc
```

### PASSO 3: Acessar Endpoints

```
REST API:
├─ Base Settings
├─ Endpoints ← CLIQUE AQUI
└─ etc
```

---

## ✅ ADICIONAR ENDPOINT 1: GET /subjects/my

### Passo A: Criar Novo Endpoint

```
Na página "Endpoints":
1. Procure: "+ New Endpoint" (botão azul)
2. Clique nele
```

Você verá uma caixa de diálogo:

```
┌─────────────────────────────────┐
│ Create New Endpoint             │
├─────────────────────────────────┤
│ Method: [GET] ▼                 │
│ Path: [              ]          │
│ API Group: [Subjects] ▼         │
├─────────────────────────────────┤
│ [ Create ]                      │
└─────────────────────────────────┘
```

### Passo B: Preencher Dados

```
1. Method: Deixe como "GET"
2. Path: Digite → /subjects/my
3. API Group: Deixe como "Subjects" (ou crie se não tiver)
4. Clique: [ Create ]
```

### Passo C: Adicionar o Código

```
Você entra no editor do endpoint.
Você verá:
- Abas (Inputs, Logic, Response)
- Um campo "Code" (ou "XanoScript")
```

**Procure pela abaw "Logic" ou "Code" e clique.**

### Passo D: Colar o XanoScript

```
1. Abra o arquivo: atv2Lab/apis/subjects/3600550_subjects_my_GET.xs
2. Copie TODO o conteúdo (Ctrl+A, Ctrl+C)
3. Volte ao Xano
4. Cole no campo "Code/Logic" (Ctrl+V)
5. Clique: "Save" (canto superior direito)
```

**Resultado esperado:** ✅ Endpoint GET /subjects/my criado

---

## ✅ ADICIONAR ENDPOINT 2: GET /subjects/{id}

### Passo A: Novo Endpoint

```
1. "+ New Endpoint"
```

### Passo B: Preencher

```
Method: GET
Path: /subjects/{id}
API Group: Subjects
[ Create ]
```

### Passo C: Colar Código

```
1. Abra: atv2Lab/apis/subjects/3600551_subjects_id_GET.xs
2. Copie TUDO
3. Cole no Xano (aba "Logic" ou "Code")
4. Clique: "Save"
```

**Resultado:** ✅ Endpoint GET /subjects/{id} criado

---

## ✅ ADICIONAR ENDPOINT 3: POST /subjects

### Passo A: Novo Endpoint

```
1. "+ New Endpoint"
```

### Passo B: Preencher

```
Method: POST (mude de GET para POST)
Path: /subjects
API Group: Subjects
[ Create ]
```

### Passo C: Colar Código

```
1. Abra: atv2Lab/apis/subjects/3600552_subjects_POST.xs
2. Copie TUDO
3. Cole no Xano
4. Clique: "Save"
```

**Resultado:** ✅ Endpoint POST /subjects criado

---

## ✅ ADICIONAR ENDPOINT 4: PATCH /subjects/{id}

### Passo A: Novo Endpoint

```
1. "+ New Endpoint"
```

### Passo B: Preencher

```
Method: PATCH (mudde se não tiver)
Path: /subjects/{id}
API Group: Subjects
[ Create ]
```

### Passo C: Colar Código

```
1. Abra: atv2Lab/apis/subjects/3600553_subjects_id_PATCH.xs
2. Copie TUDO
3. Cole no Xano
4. Clique: "Save"
```

**Resultado:** ✅ Endpoint PATCH /subjects/{id} criado

---

## ✅ ADICIONAR ENDPOINT 5: DELETE /subjects/{id}

### Passo A: Novo Endpoint

```
1. "+ New Endpoint"
```

### Passo B: Preencher

```
Method: DELETE (mude para DELETE)
Path: /subjects/{id}
API Group: Subjects
[ Create ]
```

### Passo C: Colar Código

```
1. Abra: atv2Lab/apis/subjects/3600554_subjects_id_DELETE.xs
2. Copie TUDO
3. Cole no Xano
4. Clique: "Save"
```

**Resultado:** ✅ Endpoint DELETE /subjects/{id} criado

---

## 📋 CHECKLIST FINAL

```
☐ GET /subjects/my ............... ✅
☐ GET /subjects/{id} ............ ✅
☐ POST /subjects ............... ✅
☐ PATCH /subjects/{id} ......... ✅
☐ DELETE /subjects/{id} ....... ✅

TOTAL: 5 endpoints ✅
```

---

## 🎯 PRÓXIMO PASSO

Quando terminar de adicionar os 5 endpoints:

1. Diga: **"5 endpoints adicionados!" ✅**
2. Depois vamos criar os **6 Triggers** para auditoria

---

## 💡 DICA RÁPIDA

Se der erro ao colar o código:

```
1. Clique na abá "Inputs" primeiro
2. Deixe os inputs que estão lá (limit, offset, etc)
3. Depois coloque o código na seção "Logic" ou "Code"
4. Salve
```

---

## 🔗 REFERÊNCIA

**Todos os arquivos estão em:**
```
c:\Users\sayuri\Desktop\edutrack-ai\atv2Lab\apis\subjects\

3600550_subjects_my_GET.xs      ← GET /subjects/my
3600551_subjects_id_GET.xs      ← GET /subjects/{id}
3600552_subjects_POST.xs        ← POST /subjects
3600553_subjects_id_PATCH.xs    ← PATCH /subjects/{id}
3600554_subjects_id_DELETE.xs   ← DELETE /subjects/{id}
```

---

**Quando terminar: Diga "Pronto!" ✅**
