# 🚀 Deployment Guide - Instruções Completas

Escolha seu método de deployment baseado no seu sistema operacional e preferência.

---

## 📋 Resumo de Ferramentas

### 1. **Python Script** (`deploy_xano.py`) - ✨ Recomendado
- **Plataforma:** Windows, macOS, Linux
- **Pré-requisitos:** Python 3.7+, biblioteca `requests`
- **Melhor para:** Prod deploys automatizados, CI/CD pipelines
- **Features:** Progress tracking, detailed error handling

### 2. **Bash Script** (`deploy_xano.sh`) - 🐧 Linux/macOS
- **Plataforma:** macOS, Linux
- **Pré-requisitos:** Bash, `curl`, optionally `jq`
- **Melhor para:** Shell automation, Unix-like environments
- **Features:** Native bash, color output, simple operations

### 3. **PowerShell Script** - 🪟 Windows
- **Plataforma:** Windows PowerShell 5.1+
- **Pré-requisitos:** PowerShell 5.1+
- **Melhor para:** Windows native environment
- **Features:** Windows integration, registry support

---

## 🎯 Escolha Rápida

```
┌─────────────────────────────┬──────────────────────────┐
│ Seu Ambiente                 │ Recomendação             │
├─────────────────────────────┼──────────────────────────┤
│ Windows + Python             │ python deploy_xano.py    │
│ Windows PowerShell only      │ PowerShell script (v1)   │
│ macOS / Linux                │ bash deploy_xano.sh      │
│ CI/CD Pipeline               │ python deploy_xano.py    │
│ Docker Container             │ python deploy_xano.py    │
└─────────────────────────────┴──────────────────────────┘
```

---

## 💻 SETUP - Todas as Plataformas

### Passo 1: Obter Xano API Key

1. Acesse https://app.xano.io
2. Clique em **Workspace Settings** (ícone de engrenagem)
3. Vá para **API Keys** → **Create API Key**
4. Copie a chave gerada
5. Salve num local seguro (será usada nos próximos passos)

### Passo 2: Verificar Workspace ID

Seu Workspace ID aparece na URL:
```
https://app.xano.io/workspaces/{WORKSPACE_ID}/builder
```

Default: `edutrack-ai` (já configurado)

---

## 🐍 Método 1: Python Script (Recomendado)

### Setup

```bash
# Instalar requests se não tiver
pip install requests

# Linux/macOS - Setup variáveis de ambiente
export XANO_API_KEY="sua_chave_aqui"
export XANO_WORKSPACE_ID="edutrack-ai"

# Windows PowerShell - Setup variáveis de ambiente
$env:XANO_API_KEY = "sua_chave_aqui"
$env:XANO_WORKSPACE_ID = "edutrack-ai"

# Windows CMD - Setup permanente
setx XANO_API_KEY "sua_chave_aqui"
setx XANO_WORKSPACE_ID "edutrack-ai"
```

### Executar Deploy

```bash
# 1. Teste dry-run primeiro (recomendado!)
python deploy_xano.py --dry-run

# 2. Se tudo ok, deploy para production
python deploy_xano.py --environment production

# 3. Deploy para stage (opcional)
python deploy_xano.py --environment stage
```

### Saída Esperada

```
============================================================
🚀 XanoScript Subject Database Deployment
============================================================

📊 1. Deploying Database Tables...
  📦 Deploying table: subject (ID: 753426)
     ✅ Successfully deployed
  📦 Deploying table: subject_triggers (ID: 754426)
     ✅ Successfully deployed

🔌 2. Deploying REST API Endpoints...
  🔌 Deploying endpoint: GET /subjects/my (ID: 3600550)
     ✅ Successfully deployed
  🔌 Deploying endpoint: GET /subjects/{id} (ID: 3600551)
     ✅ Successfully deployed
  🔌 Deploying endpoint: POST /subjects (ID: 3600552)
     ✅ Successfully deployed
  🔌 Deploying endpoint: PATCH /subjects/{id} (ID: 3600553)
     ✅ Successfully deployed
  🔌 Deploying endpoint: DELETE /subjects/{id} (ID: 3600554)
     ✅ Successfully deployed

⚙️  3. Deploying Backend Functions...
  ⚙️ Deploying function: check_subject_access (ID: 269538)
     ✅ Successfully deployed

============================================================
📋 DEPLOYMENT SUMMARY
============================================================
Total Items:    10
Successful:     10 ✅
Failed:         0 ❌
============================================================
```

---

## 🐧 Método 2: Bash Script (Linux/macOS)

### Setup

```bash
# Dar permissão de execução
chmod +x deploy_xano.sh

# Configurar variáveis de ambiente
export XANO_API_KEY="sua_chave_aqui"
export XANO_WORKSPACE_ID="edutrack-ai"
export XANO_API_BASE="https://api.xano.io/v1"
```

### Executar Deploy

```bash
# 1. Teste dry-run
./deploy_xano.sh --dry-run

# 2. Deploy para production
./deploy_xano.sh --production

# 3. Deploy para stage
./deploy_xano.sh --stage

# 4. Ver todas as opções
./deploy_xano.sh --help
```

### Colorized Output

```
🔍 Verifying environment...
✅ Environment verified
   API Base: https://api.xano.io/v1
   Workspace: edutrack-ai
   Environment: production

📊 1. Deploying Database Tables...
  📦 Deploying table: subject (ID: 753426)... ✅ Deployed
  📦 Deploying table: subject_triggers (ID: 754426)... ✅ Deployed
...
```

---

## 🪟 Método 3: PowerShell (Windows)

### Setup

```powershell
# Criar script PowerShell
$env:XANO_API_KEY = "sua_chave_aqui"
$env:XANO_WORKSPACE_ID = "edutrack-ai"

# Permitir execução de scripts (se necessário)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Executar via PowerShell

```powershell
# 1. Teste dry-run
python deploy_xano.py --dry-run

# 2. Deploy production
python deploy_xano.py --environment production
```

---

## ✅ Checklist Pós-Deploy

Após deployment bem-sucedido, execute esta verificação:

### 1. Verificar Tabela no Banco

```bash
# Acessar Xano Editor
1. Vá para https://app.xano.io
2. Database → Tables → Procure por "subject" (753426)
3. Confirme 14 campos presentes:
   - id, name, code, description
   - credits, semester, year
   - status, is_active
   - owner_id, account_id
   - created_at, updated_at, metadata
```

### 2. Testar Endpoints

```bash
# GET /subjects/my (listar)
curl -H "Authorization: Bearer {SEU_TOKEN}" \
     https://seu-workspace.xano.io/rest/v1/subjects/my

# POST /subjects (criar)
curl -X POST \
     -H "Authorization: Bearer {SEU_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Teste Subject",
       "code": "TST101",
       "credits": 4,
       "semester": 1,
       "year": 2024,
       "description": "Subject para teste"
     }' \
     https://seu-workspace.xano.io/rest/v1/subjects

# GET /subjects/{id} (individual)
curl -H "Authorization: Bearer {SEU_TOKEN}" \
     https://seu-workspace.xano.io/rest/v1/subjects/{ID_RETORNADO}

# PATCH /subjects/{id} (atualizar)
curl -X PATCH \
     -H "Authorization: Bearer {SEU_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"status": "archived"}' \
     https://seu-workspace.xano.io/rest/v1/subjects/{ID}

# DELETE /subjects/{id} (deletar soft)
curl -X DELETE \
     -H "Authorization: Bearer {SEU_TOKEN}" \
     https://seu-workspace.xano.io/rest/v1/subjects/{ID}
```

### 3. Verificar RBAC

```bash
# Teste com usuário sem acesso (deve retornar 403)
curl -H "Authorization: Bearer {OUTRO_TOKEN}" \
     https://seu-workspace.xano.io/rest/v1/subjects/{ID_DE_OUTRO_USUARIO}

# Saída esperada: { "error": "Access denied" }
```

### 4. Verificar Event Log

```bash
# Acessar logs de auditoria
1. Database → Tables → event_log (753423)
2. Procure por registros com:
   - entity_type: "subject"
   - action: "created", "updated", "deleted"
   - user_id: Seu ID de usuário
```

### 5. Testar Triggers

```bash
# Confirmar soft delete (is_active = false não remove registro)
curl -H "Authorization: Bearer {TOKEN}" \
     https://seu-workspace.xano.io/rest/v1/subjects/{ID}

# Resposta esperada: 404 (porque trigger completa delete é soft)
```

---

## 🐛 Troubleshooting

### ❌ "XANO_API_KEY not set"

**Solução:**
```bash
# Verificar se variável está configurada
echo $XANO_API_KEY  # Linux/macOS
echo %XANO_API_KEY%  # Windows CMD
$env:XANO_API_KEY  # Windows PowerShell

# Se vazio, configurar:
export XANO_API_KEY="sua_chave"  # Linux/macOS
set XANO_API_KEY=sua_chave  # Windows CMD
$env:XANO_API_KEY = "sua_chave"  # Windows PowerShell
```

### ❌ "Unauthorized" (401)

**Causas possíveis:**
- API Key inválida ou expirada
- API Key de workspace errado
- Permissões insuficientes

**Solução:**
```bash
# 1. Regerar API Key em https://app.xano.io
# 2. Verificar workspace correto
# 3. Testar key manualmente
curl -H "Authorization: Bearer SEU_KEY" \
     https://api.xano.io/v1/me
```

### ❌ "Not Found" (404)

**Causas possíveis:**
- Resource ID incorreto (753426, 3600550, etc)
- Workspace não existe
- Resource foi deletado

**Solução:**
```bash
# Verificar IDs em cada seção do XANOSCRIPT_PUSH_TO_XANO.md
# Confirmar Workspace ID em https://app.xano.io
# Usar --dry-run para testar sem modificar
python deploy_xano.py --dry-run
```

### ❌ "timeout"

**Solução:**
```bash
# Aguardar e tentar novamente
sleep 30
python deploy_xano.py --environment production

# Ou testar conectividade
curl -I https://api.xano.io/v1
```

### ❌ Deployment parcial (alguns items falharam)

**Solução:**
```bash
# 1. Revisar output para identificar items falhados
# 2. Corrigir issues (ex: sintaxe XanoScript)
# 3. Redeploy só dos items falhados manualmente
# 4. Ou fazer rollback (ver próxima seção)
```

---

## 🔄 Rollback (Desfazer Deploy)

Se algo der errado:

### Opção 1: Rollback via Xano UI (Recomendado)

```
1. Acesse https://app.xano.io
2. Workspace Settings → Version Control
3. Procure pela version anterior (data/hora antes do deploy)
4. Clique "Restore" naquela version
5. Confirme ação
```

### Opção 2: Manual Rollback

```bash
# Deletar tables via API
curl -X DELETE \
     -H "Authorization: Bearer {ADMIN_KEY}" \
     https://api.xano.io/v1/tables/753426

# Deletar endpoints
curl -X DELETE \
     -H "Authorization: Bearer {ADMIN_KEY}" \
     https://api.xano.io/v1/endpoints/3600550
```

---

## 📊 Deploy Matrix - O Que é Deployado

| Item ID | Nome | Tipo | Status | Descrição |
|---------|------|------|--------|-----------|
| 753426 | subject | Table | ✅ Deploy | Subject (Discipline) table - 14 fields |
| 754426 | subject_triggers | Triggers | ✅ Deploy | 6 triggers for audit+soft delete |
| 3600550 | GET /subjects/my | Endpoint | ✅ Deploy | List user's subjects (paginated) |
| 3600551 | GET /subjects/{id} | Endpoint | ✅ Deploy | Get single subject (RBAC) |
| 3600552 | POST /subjects | Endpoint | ✅ Deploy | Create subject (validated) |
| 3600553 | PATCH /subjects/{id} | Endpoint | ✅ Deploy | Update subject (partial) |
| 3600554 | DELETE /subjects/{id} | Endpoint | ✅ Deploy | Delete subject (soft delete) |
| N/A | Subjects API Group | API Group | ✅ Deploy | API group organization |
| 269538 | check_subject_access | Function | ✅ Deploy | RBAC enforcement function |

**Total: 10 items**

---

## 🎓 Próximos Passos

Após deployment bem-sucedido:

1. **✅ Executar testes de integração**
   - Rodar: `subjects_integration_tests.xs`
   - Verificar: Todos os 10 testes devem passar

2. **✅ Validar RBAC completo**
   - Testar acesso como owner
   - Testar acesso como admin
   - Testar acesso negado (outro usuário)

3. **✅ Monitorar logs**
   - Acompanhar: `event_log` table
   - Verificar: Ações criadas, atualizadas, deletadas

4. **✅ Validar soft delete**
   - Deletar um subject
   - Confirmar: `is_active` = false
   - Confirmar: Registro preservado para auditoria

5. **✅ Documentar processo**
   - Atualizar: DEPLOYMENT_LOG.md
   - Registrar: Data, hora, responsável, issues

---

## 📚 Referências

- **Deployment Guide Completo:** [XANOSCRIPT_PUSH_TO_XANO.md](./XANOSCRIPT_PUSH_TO_XANO.md)
- **Design Document:** [atv2Lab/openspec/projeto1/design.md](atv2Lab/openspec/projeto1/design.md)
- **Specification:** [atv2Lab/openspec/projeto1/specs/spec.md](atv2Lab/openspec/projeto1/specs/spec.md)
- **Tasks:** [atv2Lab/openspec/projeto1/tasks.md](atv2Lab/openspec/projeto1/tasks.md)
- **Python Script Help:**
  ```bash
  python deploy_xano.py --help
  ```
- **Bash Script Help:**
  ```bash
  ./deploy_xano.sh --help
  ```

---

## 💬 Suporte

Para dúvidas ou problemas:

1. Consulte [TROUBLESHOOTING.md](#troubleshooting-1) (neste documento)
2. Revise [XANOSCRIPT_PUSH_TO_XANO.md](./XANOSCRIPT_PUSH_TO_XANO.md) completamente
3. Verifique logs de deploy
4. Teste com `--dry-run` primeiro

---

**Last Updated:** 2024-01-17  
**Deployment Tools Version:** 1.0  
**Status:** ✅ Ready for Production Deployment  

🚀 **Você está pronto para fazer deploy em production!**
