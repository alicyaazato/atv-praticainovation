# 🚀 XanoScript: Push Stage Changes to Xano

## Objetivo: Fazer Deploy dos Arquivos Subject Database para Xano Production

Como você criou/modificou arquivos XanoScript em **Stage**, agora precisa fazer push/deploy para **Xano Production**.

---

## 📋 Checklist de Arquivos a Fazer Push

### ✅ Arquivos Criados (Prontos para Deploy)

```
✅ TABELAS:
   └─ atv2Lab/tables/753426_subject.xs (nova tabela)
   └─ atv2Lab/tables/triggers/754426_subject_triggers.xs (novos triggers)

✅ APIs (5 Endpoints):
   └─ atv2Lab/apis/subjects/3600550_subjects_my_GET.xs
   └─ atv2Lab/apis/subjects/3600551_subjects_id_GET.xs
   └─ atv2Lab/apis/subjects/3600552_subjects_POST.xs
   └─ atv2Lab/apis/subjects/3600553_subjects_id_PATCH.xs
   └─ atv2Lab/apis/subjects/3600554_subjects_id_DELETE.xs
   └─ atv2Lab/apis/subjects/api_group.xs

✅ FUNCTIONS:
   └─ atv2Lab/functions/getting_started_template/269538_check_subject_access.xs

Total: 10 arquivos XanoScript para deploy
```

---

## 🔧 Método 1: Via Xano UI (Manual)

### Passo 1: Acessar Xano Dashboard

```
1. Abra: https://app.xano.io
2. Login com suas credenciais
3. Selecione o workspace edutrack-ai
4. Acesse Version Control ou Staging
```

### Passo 2: Sincronizar Database (Tabela + Triggers)

```
📁 Database → Tables
  1. Procure por: subject (753426)
  2. Clique em "Review Changes"
  3. Confirme os campos (14 campos)
  4. Deploy para Production

📁 Database → Triggers
  1. Procure por: 754426_subject_triggers
  2. Clique em "Review Changes"
  3. Confirme os 6 triggers
  4. Deploy para Production
```

### Passo 3: Sincronizar Endpoints API

```
📁 API → Endpoints
  1. Procure por: GET /subjects/my (3600550)
  2. Review code
  3. Deploy → Production
  
  4. Repita para cada um dos 5 endpoints:
     - 3600551 (GET by ID)
     - 3600552 (POST create)
     - 3600553 (PATCH update)
     - 3600554 (DELETE)
     - api_group.xs
```

### Passo 4: Sincronizar Functions

```
📁 Backend Logic → Functions
  1. Procure por: check_subject_access (269538)
  2. Review code (RBAC checks)
  3. Deploy → Production
```

---

## 🔧 Método 2: Via CLI/Script (Automático)

### Opção A: Xano CLI (se disponível)

```bash
# 1. Ativar virtualenv (se necessário)
. .venv/Scripts/activate

# 2. Fazer push das mudanças
xano push --stage="stage" --environment="production" \
  --table="753426_subject" \
  --table="754426_subject_triggers" \
  --apis="subjects"

# 3. Verificar status
xano status --environment="production"
```

### Opção B: Script Python para Deploy

```python
# deploy_to_xano.py
import requests
import json

XANO_BASE_URL = "https://api.xano.io/v1"
XANO_API_KEY = "YOUR_XANO_API_KEY"  # Defina como env var

def deploy_table(table_id, table_name):
    """Deploy uma tabela para Xano Production"""
    endpoint = f"{XANO_BASE_URL}/tables/{table_id}/deploy"
    headers = {"Authorization": f"Bearer {XANO_API_KEY}"}
    payload = {"action": "deploy", "to_environment": "production"}
    
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ {table_name} deployed successfully")
    else:
        print(f"❌ {table_name} deployment failed: {response.text}")
    return response.status_code == 200

def deploy_api_endpoint(api_id, endpoint_path):
    """Deploy um endpoint para Xano Production"""
    endpoint = f"{XANO_BASE_URL}/apis/{api_id}/deploy"
    headers = {"Authorization": f"Bearer {XANO_API_KEY}"}
    payload = {"action": "deploy", "to_environment": "production"}
    
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ {endpoint_path} deployed successfully")
    else:
        print(f"❌ {endpoint_path} deployment failed: {response.text}")
    return response.status_code == 200

# Main deployment
print("🚀 Starting Subject Database Deployment to Production...\n")

# Deploy tables
print("1. Deploying Database Tables...")
deploy_table("753426", "subject (table)")
deploy_table("754426", "subject_triggers")

# Deploy API endpoints
print("\n2. Deploying REST API Endpoints...")
endpoints = [
    ("3600550", "GET /subjects/my"),
    ("3600551", "GET /subjects/{id}"),
    ("3600552", "POST /subjects"),
    ("3600553", "PATCH /subjects/{id}"),
    ("3600554", "DELETE /subjects/{id}"),
]

for api_id, path in endpoints:
    deploy_api_endpoint(api_id, path)

# Deploy functions
print("\n3. Deploying Backend Functions...")
deploy_api_endpoint("269538", "check_subject_access")

print("\n✅ Deployment complete!")
```

**Para usar:**
```bash
# 1. Defina seu API key como variável
export XANO_API_KEY="seu_api_key_aqui"

# 2. Execute o script
python deploy_to_xano.py
```

---

## 🔧 Método 3: Via Xano Version Control (Git-like)

### Se Xano tiver controle de versão integrado:

```bash
# 1. Ver mudanças staged
xano diff --staged

# 2. Confirmar mudanças locais
xano add atv2Lab/tables/753426_subject.xs
xano add atv2Lab/tables/triggers/754426_subject_triggers.xs
xano add atv2Lab/apis/subjects/*.xs
xano add atv2Lab/functions/getting_started_template/269538_check_subject_access.xs

# 3. Fazer commit
xano commit -m "Deploy Subject Database (table, triggers, 5 CRUD endpoints, RBAC function)"

# 4. Push para production
xano push
```

---

## ✅ Verificação Pós-Deploy

### Passo 1: Verificar se Tabela Existe

```bash
curl -X GET "https://your-workspace.xano.io/api/v1/subjects" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Esperado: Array vazio ou mensagem de sucesso
# Status: 200 OK
```

### Passo 2: Testar Endpoint POST (Criar Disciplina)

```bash
curl -X POST "https://your-workspace.xano.io/api/v1/subjects" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Introduction to Python",
    "code": "CS101",
    "credits": 3,
    "account_id": 456
  }'

# Esperado: 201 Created com objeto subject
```

### Passo 3: Testar Endpoint GET (Listar Minhas Disciplinas)

```bash
curl -X GET "https://your-workspace.xano.io/api/v1/subjects/my" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Esperado: 200 OK com array de subjects
```

### Passo 4: Verificar Triggers

```sql
-- Via Xano Database Query
SELECT * FROM event_logs 
WHERE action LIKE 'subject.%' 
ORDER BY created_at DESC 
LIMIT 10;

-- Esperado: Eventos de criação/atualização/delete de subjects
```

### Passo 5: Verificar RBAC

```bash
# Teste com usuário diferente (sem permissão)
curl -X GET "https://your-workspace.xano.io/api/v1/subjects/1001" \
  -H "Authorization: Bearer DIFFERENT_USER_JWT"

# Esperado: 403 Forbidden OU 404 Not Found (sem leak de informação)
```

---

## 🎯 Checklist de Deploy

```
Deploy da Tabela:
  ☐ subject (753426) - 14 campos
  ☐ subject_triggers (754426) - 6 triggers
  ☐ Índices criados (7+)
  ☐ Foreign keys OK

Deploy de Endpoints:
  ☐ GET /subjects/my (3600550) - List
  ☐ GET /subjects/{id} (3600551) - Get
  ☐ POST /subjects (3600552) - Create
  ☐ PATCH /subjects/{id} (3600553) - Update
  ☐ DELETE /subjects/{id} (3600554) - Delete
  ☐ API Group - `subjects`

Deploy de Functions:
  ☐ check_subject_access (269538) - RBAC Function

Testes Pós-Deploy:
  ☐ Tabela acessível via API
  ☐ POST endpoint cria registro
  ☐ GET endpoint retorna dados
  ☐ RBAC enforcement funciona
  ☐ Event logging registra operações
  ☐ Validações aplicadas

Monitoramento:
  ☐ Error logs verificados
  ☐ Performance aceitável
  ☐ Nenhum downtime
  ☐ Backup realizado antes do deploy
```

---

## 🚨 Troubleshooting

### Erro: "Table already exists"
```
Causa: Tabela já existe em production
Solução: 
  1. Verifique se é realmente "753426_subject"
  2. Se estiver desatualizada, delete e recrie
  3. Ou execute UPDATE ao invés de CREATE
```

### Erro: "Foreign Key Constraint Failed"
```
Causa: Tabelas referenciadas não existem
Solução:
  1. Verifique se user (753421) existe
  2. Verifique se account (753422) existe
  3. Se não, crie-as primeiro
```

### Erro: "Permission Denied"
```
Causa: Usuário não tem permissions para deploy
Solução:
  1. Verifique credenciais/API key
  2. Solicite permissão ao admin Xano
  3. Use conta com privilégios de admin
```

### Erro: "Endpoint Already Exists"
```
Causa: API endpoint já deployado
Solução:
  1. Atualize ao invés de criar novo
  2. Ou delete o antigo primeiro
```

---

## 📊 Status Pós-Deploy

Depois de completar todos os passos, você terá:

```
✅ Tabela subject em Production
✅ 6 Triggers em Production (auditoria 100%)
✅ 5 Endpoints CRUD em Production
✅ RBAC Function em Production
✅ 14 campos validados em Production
✅ Event logging funcionando
✅ Multi-tenant isolation ativo
✅ Pronto para usuários reais
```

---

## 🎯 Próximos Passos

1. ✅ **Deploy Realizado?** → Ir para Step 2
2. ⏳ **Testes em Production** (1-2h)
   - CRUD tests
   - RBAC scenarios
   - Performance tests
3. ⏳ **Monitoramento** (ongoing)
   - Error rates
   - Performance metrics
   - User feedback
4. ⏳ **Phase 2: Automações** (futuro)
   - Workflows
   - Scheduled tasks
   - Webhooks

---

## 📞 Suporte

Se encontrar problemas durante o deploy:

1. Consulte: `SUBJECTS_IMPLEMENTATION_SUMMARY.md`
2. Verifique: `subjects_api_openapi.yaml` (API spec)
3. Revise: Arquivos XanoScript implementados
4. Teste: Scripts de verificação acima

---

**Status: 🚀 PRONTO PARA DEPLOY**

Todos os 10 arquivos XanoScript estão implementados e prontos para fazer push para Xano Production.

Execute o método de deploy que melhor se adequa ao seu setup e siga o checklist de verificação pós-deploy.

Boa sorte! 🎉
