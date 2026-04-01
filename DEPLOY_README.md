# XanoScript Deployment Tool

Ferramenta Python para fazer deploy automático do Subject Database para Xano Production.

## Setup Rápido

### 1. Configurar Variáveis de Ambiente

```bash
# Windows PowerShell
$env:XANO_API_KEY="seu_api_key_aqui"
$env:XANO_WORKSPACE_ID="edutrack-ai"
$env:XANO_API_BASE="https://api.xano.io/v1"

# Linux/Mac
export XANO_API_KEY="seu_api_key_aqui"
export XANO_WORKSPACE_ID="edutrack-ai"
export XANO_API_BASE="https://api.xano.io/v1"
```

### 2. Testar Deploy (Dry Run)

```bash
python deploy_xano.py --dry-run
```

**Saída esperada:**
```
============================================================
🚀 XanoScript Subject Database Deployment
============================================================

⚠️  DRY RUN MODE - No actual changes will be made

📊 1. Deploying Database Tables...
  📦 Deploying table: subject (ID: 753426)
     [DRY RUN] Would deploy table
  📦 Deploying table: subject_triggers (ID: 754426)
     [DRY RUN] Would deploy table

🔌 2. Deploying REST API Endpoints...
  🔌 Deploying endpoint: GET /subjects/my (ID: 3600550)
     [DRY RUN] Would deploy endpoint
  ...

⚙️  3. Deploying Backend Functions...
  ⚙️ Deploying function: check_subject_access (ID: 269538)
     [DRY RUN] Would deploy function

============================================================
📋 DEPLOYMENT SUMMARY
============================================================
Total Items:    10
Successful:     10 ✅
Failed:         0 ❌
============================================================
```

### 3. Deploy para Production

```bash
python deploy_xano.py --environment production
```

## Opções de Comando

```bash
# Dry run (recomendado antes de deploy real)
python deploy_xano.py --dry-run

# Deploy para stage
python deploy_xano.py --environment stage

# Deploy para production (padrão)
python deploy_xano.py --environment production

# Pular verificação de ambiente
python deploy_xano.py --skip-verify --environment production
```

## Obtendo Xano API Key

1. Acesse **https://app.xano.io**
2. Vá para **Workspace Settings** → **API Keys**
3. Clique em **+ Create API Key**
4. Copie a chave e salve em variável de ambiente

## O que é Deployado

Total: **10 items** (1 table + 1 triggers + 5 endpoints + 1 API group + 2 functions)

### 📊 Tables
- `753426_subject.xs` - Subject table (14 fields)
- Triggers para audit logging (6 triggers)

### 🔌 Endpoints
- `GET /subjects/my` - List subjects
- `GET /subjects/{id}` - Get subject by ID
- `POST /subjects` - Create subject
- `PATCH /subjects/{id}` - Update subject
- `DELETE /subjects/{id}` - Delete subject

### ⚙️ Functions
- `check_subject_access` - RBAC enforcement

## Verificação Pós-Deploy

Após deploy bem-sucedido, execute:

```bash
# Teste básico - GET /subjects/my
curl -H "Authorization: Bearer {token}" \
     https://api.xano.io/v1/subjects/my

# Teste POST - Create subject
curl -X POST \
     -H "Authorization: Bearer {token}" \
     -H "Content-Type: application/json" \
     -d '{"name":"Matemática","code":"MAT101","credits":4}' \
     https://api.xano.io/v1/subjects

# Teste DELETE - Soft delete
curl -X DELETE \
     -H "Authorization: Bearer {token}" \
     https://api.xano.io/v1/subjects/{id}
```

## Troubleshooting

### ❌ "XANO_API_KEY not set"
```bash
# Solução:
export XANO_API_KEY="sua_chave_aqui"
python deploy_xano.py
```

### ❌ "Unauthorized" (401)
- Verifique se API Key é válida
- Confirme se workspace ID está correto
- Teste acesso em https://app.xano.io

### ❌ "Not Found" (404)
- Verifique se resource IDs existem (753426, 3600550, etc.)
- Confirme workspace no Xano
- Execute `--dry-run` para diagnosticar

### ❌ "Conflict" (409)
- Recurso já existente em production
- Verifique se deploy anterior foi bem-sucedido
- Use rollback se necessário

## Logs de Deploy

Todos os deploys são registrados. Para revisar:

```bash
# Bash/Zsh
python deploy_xano.py --environment production 2>&1 | tee deploy_$(date +%s).log

# PowerShell
python deploy_xano.py --environment production | Tee-Object -FilePath "deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
```

## Rollback

Se deploy falhar:

1. **Identifique items falhados**
   - Revise output do script
   - Procure por "❌" na summary

2. **Rollback manual**
   - Acesse https://app.xano.io
   - Vá para Workspace → Version Control
   - Restaure version anterior

3. **Redeploy**
   - Corrija issues
   - Execute `python deploy_xano.py --dry-run` novamente
   - Deploy com `python deploy_xano.py`

## Próximos Passos

Após deploy bem-sucedido:

- ✅ Run integration tests (ver `subjects_integration_tests.xs`)
- ✅ Monitor event logs (table: `event_log`)
- ✅ Validate RBAC behavior com diferentes roles
- ✅ Test soft delete e data integrity
- ✅ Monitor performance metrics

## Suporte

Para dúvidas:
- Consulte [XANOSCRIPT_PUSH_TO_XANO.md](./XANOSCRIPT_PUSH_TO_XANO.md)
- Review OpenSpec specs em `atv2Lab/openspec/specs/`
- Confira design em `atv2Lab/openspec/projeto1/design.md`
