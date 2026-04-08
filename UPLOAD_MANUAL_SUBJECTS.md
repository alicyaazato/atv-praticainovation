# 📤 GUIA DE UPLOAD MANUAL - SUBJECTS

Como a API de Deploy não funciona diretamente, faremos upload manual no Xano UI.

---

## 🔧 **PASSO A PASSO**

### **1. Acesse o Xano**
- Vá para: https://app.xano.io
- Selecione seu workspace: **edutrack-ai**

### **2. Para cada arquivo abaixo:**

1. Abra o arquivo em VS Code ou copie o conteúdo
2. No Xano, vá para **API → Endpoints**
3. Procure pelo endpoint
4. Cole o código
5. Clique em **Save**
6. Clique em **Publish** ou **Deploy**

---

## 📋 **ARQUIVOS A FAZER UPLOAD**

### **Arquivo 1: GET /subjects/my - Listar Subjects do Usuário**
- **ID:** 3600550
- **Tipo:** GET
- **Localização local:** `atv2Lab/apis/subjects/3600550_subjects_my_GET.xs`
- **Conteúdo:** [abrir arquivo para copiar]

### **Arquivo 2: GET /subjects/{id} - Obter Subject por ID**
- **ID:** 3600551
- **Tipo:** GET
- **Localização local:** `atv2Lab/apis/subjects/3600551_subjects_id_GET.xs`
- **Conteúdo:** [abrir arquivo para copiar]

### **Arquivo 3: POST /subjects - Criar Subject**
- **ID:** 3600552
- **Tipo:** POST
- **Localização local:** `atv2Lab/apis/subjects/3600552_subjects_POST.xs`
- **Conteúdo:** [abrir arquivo para copiar]

### **Arquivo 4: PATCH /subjects/{id} - Atualizar Subject**
- **ID:** 3600553
- **Tipo:** PATCH
- **Localização local:** `atv2Lab/apis/subjects/3600553_subjects_id_PATCH.xs`
- **Conteúdo:** [abrir arquivo para copiar]

### **Arquivo 5: DELETE /subjects/{id} - Deletar Subject**
- **ID:** 3600554
- **Tipo:** DELETE
- **Localização local:** `atv2Lab/apis/subjects/3600554_subjects_id_DELETE.xs`
- **Conteúdo:** [abrir arquivo para copiar]

### **Arquivo 6: API Group**
- **ID:** subjects_api_group
- **Tipo:** API Group
- **Localização local:** `atv2Lab/apis/subjects/api_group.xs`
- **Conteúdo:** [abrir arquivo para copiar]

---

## 🗂️ **TABELAS E FUNÇÕES (Se necessário)**

Se você também precisa fazer upload da tabela subjects:

- **Tabela:** `atv2Lab/tables/753426_subject.xs`
- **Triggers:** `atv2Lab/tables/triggers/754426_subject_triggers.xs`
- **Função:** `atv2Lab/functions/getting_started_template/269538_check_subject_access.xs`

---

## ✅ **Após fazer upload de tudo:**

1. Teste os endpoints no Xano
2. Verifique se estão publicados em Production
3. Teste via Postman ou cURL

