# 🛠️ Criar Tabela Subjects Manualmente no Xano

**Status:** 🔴 Tabela NÃO criada  
**Ação:** Criar passo a passo em Xano UI  
**Tempo:** ~10 minutos  

---

## 📍 Você está em: https://app.xano.io

---

## 🎯 PASSO 1: Abrir Database Builder

```
1. Localize o menu ESQUERDO
2. Clique em: DATABASE (ou ícone de banco de dados)
3. Procure por: "Tables"
4. Clique em: "+ New Table" (botão azul no canto superior direito)
```

**Você deve ver uma janela: "Create New Table"**

---

## 🎯 PASSO 2: Nomear a Tabela

```
Na janela "Create New Table":

1. Campo "Table Name": Digite → subject
2. Campo "ID": Deve mostrar auto (deixe como está)
3. Clique: "Create Table"
```

**Resultado esperado:** Você entra no editor da tabela "subject"

---

## 🎯 PASSO 3: Adicionar os 14 Campos

Agora você está no editor da tabela. Veja um painel com:
- Um campo "id" já pré-criado
- Botão "+ Add Field"

### 3.1 - Adicionar Campo: name

```
1. Clique: "+ Add Field"
2. Nome do campo: name
3. Tipo: Text
4. Configurações:
   ☐ Required: SIM (marca a checkbox)
   ☐ Filters: trim
   ☐ Max length: 255
5. Clique: "Save"
```

### 3.2 - Adicionar Campo: code

```
1. Clique: "+ Add Field"
2. Nome: code
3. Tipo: Text
4. Configurações:
   ☐ Required: NÃO
   ☐ Max length: 50
   ☐ Unique: YES (IMPORTANTE - único por conta)
5. Clique: "Save"
```

### 3.3 - Adicionar Campo: description

```
1. Clique: "+ Add Field"
2. Nome: description
3. Tipo: Text (ou Long Text)
4. Configurações:
   ☐ Required: NÃO
   ☐ Max length: 2000
5. Clique: "Save"
```

### 3.4 - Adicionar Campo: credits

```
1. Clique: "+ Add Field"
2. Nome: credits
3. Tipo: Number
4. Configurações:
   ☐ Required: NÃO
   ☐ Min: 0
   ☐ Max: 20
5. Clique: "Save"
```

### 3.5 - Adicionar Campo: semester

```
1. Clique: "+ Add Field"
2. Nome: semester
3. Tipo: Text
4. Configurações:
   ☐ Required: NÃO
   ☐ Pattern: ^[0-9]º$  (aceita "1º", "2º", etc)
5. Clique: "Save"
```

### 3.6 - Adicionar Campo: year

```
1. Clique: "+ Add Field"
2. Nome: year
3. Tipo: Number
4. Configurações:
   ☐ Required: NÃO
   ☐ Min: 1900
   ☐ Max: 2100
5. Clique: "Save"
```

### 3.7 - Adicionar Campo: status

```
1. Clique: "+ Add Field"
2. Nome: status
3. Tipo: SELECT (ou ENUM)
4. Configurações:
   ☐ Required: SIM
   ☐ Opções: 
      - active
      - archived
      - draft
   ☐ Default: active
5. Clique: "Save"
```

### 3.8 - Adicionar Campo: is_active

```
1. Clique: "+ Add Field"
2. Nome: is_active
3. Tipo: Boolean (ou Toggle)
4. Configurações:
   ☐ Required: NÃO
   ☐ Default: true (SIM)
5. Clique: "Save"
```

### 3.9 - Adicionar Campo: owner_id

```
1. Clique: "+ Add Field"
2. Nome: owner_id
3. Tipo: Link to table
4. Configurações:
   ☐ Link to table: users
   ☐ Link field: id
   ☐ Required: SIM (IMPORTANTE - todo subject precisa ter owner)
5. Clique: "Save"
```

**RESULTADO:** owner_id agora aponta para a tabela "users"

### 3.10 - Adicionar Campo: account_id

```
1. Clique: "+ Add Field"
2. Nome: account_id
3. Tipo: Link to table
4. Configurações:
   ☐ Link to table: account (ou accounts)
   ☐ Link field: id
   ☐ Required: SIM (IMPORTANTE - multi-tenant isolation)
5. Clique: "Save"
```

**RESULTADO:** account_id agora aponta para a tabela "account"

### 3.11 - Adicionar Campo: created_at

```
1. Clique: "+ Add Field"
2. Nome: created_at
3. Tipo: Timestamp (ou Date/Time)
4. Configurações:
   ☐ Required: NÃO
   ☐ Default: NOW (ou current_timestamp)
   ☐ Visibility: Private (não retorna em API)
5. Clique: "Save"
```

### 3.12 - Adicionar Campo: updated_at

```
1. Clique: "+ Add Field"
2. Nome: updated_at
3. Tipo: Timestamp (ou Date/Time)
4. Configurações:
   ☐ Required: NÃO
   ☐ Default: NOW (ou current_timestamp)
   ☐ Visibility: Private (não retorna em API)
5. Clique: "Save"
```

### 3.13 - Adicionar Campo: metadata

```
1. Clique: "+ Add Field"
2. Nome: metadata
3. Tipo: JSON
4. Configurações:
   ☐ Required: NÃO
   ☐ Visibility: Private (não retorna em API)
5. Clique: "Save"
```

### ✅ RESUMO DOS 14 CAMPOS ADICIONADOS:

```
✅ id (auto - já existe)
✅ name (Text, required, max:255)
✅ code (Text, optional, max:50, unique)
✅ description (Text, optional, max:2000)
✅ credits (Number, optional, 0-20)
✅ semester (Text, optional, pattern)
✅ year (Number, optional, 1900-2100)
✅ status (Enum, required, default:active)
✅ is_active (Boolean, optional, default:true)
✅ owner_id (Link to users, required) ← FOREIGN KEY
✅ account_id (Link to account, required) ← FOREIGN KEY
✅ created_at (Timestamp, auto: now, private)
✅ updated_at (Timestamp, auto: now, private)
✅ metadata (JSON, optional, private)

TOTAL: 14 campos ✅
```

---

## 🎯 PASSO 4: Salvar a Tabela

```
1. No topo da página, clique: "SAVE" ou "Done"
2. A tabela "subject" deve aparecer em: Database → Tables → subject
```

---

## ✅ PASSO 5: Verificar Relacionamentos

```
1. Volte para: Database → Tables
2. Clique na tabela: "subject"
3. Procure pelos campos:
   ☐ owner_id → Valor deve ser "Link to: users"
   ☐ account_id → Valor deve ser "Link to: account"
4. Se aparecer assim, está correto! ✅
```

---

## 📊 Verificação Visual

**Você deve vê na tela algo assim:**

```
TABLE: subject
├─ id (Primary Key, Auto)
├─ name (Text, Required)
├─ code (Text, Unique)
├─ description (Text)
├─ credits (Number)
├─ semester (Text)
├─ year (Number)
├─ status (Enum: active, archived, draft)
├─ is_active (Boolean, Default: true)
├─ owner_id (Link to users) ← FOREIGN KEY
├─ account_id (Link to account) ← FOREIGN KEY
├─ created_at (Timestamp, Auto)
├─ updated_at (Timestamp, Auto)
└─ metadata (JSON)
```

---

## 🎯 PRÓXIMO PASSO

Quando terminar de criar a tabela:

1. **Confirme aqui:** "Tabela subject criada com 14 campos! ✅"
2. **Depois vamos criar:**
   - 5 Endpoints (GET/POST/PATCH/DELETE)
   - 6 Triggers (para auditoria)
   - 1 Função RBAC

---

## 💡 DICAS

- Se errou um campo, clique no campo e depois clique "Delete" para remover
- Depois recrie o campo corretamente
- Não precisa fazer tudo de uma vez - pode salvar após cada campo
- Se precisar voltar, sempre clique "Save" antes de sair da tabela

---

## ⏱️ PRÓXIMAS AÇÕES

```
AGORA (5-10 min):
✅ Criar tabela "subject" com 14 campos
✅ Verificar owner_id → users
✅ Verificar account_id → account

DEPOIS (10-15 min):
⏳ Criar 5 endpoints REST
⏳ Criar 6 triggers de auditoria
⏳ Criar função RBAC

FINAL (5 min):
⏳ Testar POST /subjects (criar)
⏳ Testar GET /subjects/my (listar)
⏳ Testar DELETE (soft delete)
```

---

**Quando terminar, diga: "Pronto, tabela criada!" ✅**
