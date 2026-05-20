# Activity Grades - Implementation Tasks

## Overview
Tarefas para implementar o sistema de lançamento de notas (activity_grades) conforme especificado em proposal.md, design.md e spec.md.

**Escopo:** Apenas o que foi solicitado pelo usuário (planejar a funcionalidade de professor lançar notas).

## Task Breakdown

### PHASE 1: Database & Validation

#### Task 1.1: Create table activity_grade
- **Description:** Criar tabela XanoScript com schema completo
- **Files:** `atv2Lab/tables/753427_activity_grade.xs` (supost ID, verificar com Xano)
- **Subtasks:**
  - [x] Definir campos conforme schema em design.md
  - [x] Adicionar validações de range (grade 0-10)
  - [x] Criar indexes para performance
  - [x] Adicionar unique constraint (account_id, activity_id, student_id)
  - [x] Adicionar foreign keys com validações
- **Acceptance Criteria:**
  - ✅ Tabela suporta todos os 13 campos
  - ✅ Validação de grade [0.0, 10.0] funciona
  - ✅ Queries com 10k+ notas executam em <100ms (com indexes)
  - ✅ Tentativa de criar duplicate lança erro

**Estimate:** 2-3 horas

---

#### Task 1.2: Create function - Validate grade input
- **Description:** Função reutilizável para validar inputs de nota
- **Files:** `atv2Lab/functions/269539_validate_grade_input.xs`
- **Subtasks:**
  - [x] Validar grade está entre 0.0 e 10.0
  - [x] Validar professor_id ≠ student_id
  - [x] Validar campos obrigatórios presentes
  - [x] Retornar estrutura {is_valid: boolean, errors: []}
- **Acceptance Criteria:**
  - ✅ Rejeita grade < 0 ou > 10
  - ✅ Rejeita grade onde professor=student
  - ✅ Aceita grades válidas (0.0, 5.5, 10.0)
  - ✅ Retorna mensagens de erro descritivas

**Estimate:** 1-2 horas

---

#### Task 1.3: Create function - Check professor ownership (RBAC)
- **Description:** Verificar se professor é dono da atividade (via subject)
- **Files:** `atv2Lab/functions/269540_check_professor_activity_ownership.xs`
- **Subtasks:**
  - [x] Query activity para obter subject_id
  - [x] Query subject para obter owner_id
  - [x] Comparar owner_id com professor_id
  - [x] Permitir admin (role="admin") bypass
  - [x] Validar account_id match
- **Acceptance Criteria:**
  - ✅ Retorna true se professor é dono
  - ✅ Retorna true se user.role="admin"
  - ✅ Retorna false se outro professor
  - ✅ Valida multi-tenant (account_id)

**Estimate:** 1-2 horas

---

### PHASE 2: API Endpoints

#### Task 2.1: Create endpoint POST /activity-grades
- **Description:** Criar nova nota com validação completa
- **Files:** `atv2Lab/apis/activity-grades/3600555_activity_grades_POST.xs`
- **Subtasks:**
  - [x] Validar autenticação (precondition $auth.user_id)
  - [x] Extrair inputs (account_id, activity_id, student_id, professor_id, grade, feedback)
  - [x] Validar inputs usando função 1.2
  - [x] Verificar ownership usando função 1.3
  - [x] Verificar duplicata (unique constraint)
  - [x] Validar student existe e está ativo
  - [x] Validar activity existe e está ativa
  - [x] Inserir em activity_grade table
  - [x] Logar em event_log (action="activity_grade_created")
  - [x] Retornar 201 + objeto criado
- **Acceptance Criteria:**
  - ✅ POST com dados válidos cria nota e retorna 201
  - ✅ Professor não-dono recebe 403
  - ✅ Admin consegue criar em qualquer activity
  - ✅ Duplicata retorna 409
  - ✅ Nota fora de range retorna 400
  - ✅ Event log criado automaticamente

**Estimate:** 3-4 horas

---

#### Task 2.2: Create endpoint GET /activity-grades
- **Description:** Listar notas com paginação e filtros
- **Files:** `atv2Lab/apis/activity-grades/3600556_activity_grades_GET.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair query params (limit, offset, activity_id?, student_id?)
  - [x] Validar limit <= 100, limit >= 1
  - [x] Set default limit=50 se não fornecido
  - [x] Query com filtro account_id = auth.user.account_id
  - [x] Se professor, filtrar por professor_id = auth.user_id
  - [x] Se admin, listar todas da conta
  - [x] Aplicar offset/limit
  - [x] Retornar array + metadados {total_count, limit, offset}
- **Acceptance Criteria:**
  - ✅ Admin vê todas as notas da conta
  - ✅ Professor vê apenas suas notas lançadas
  - ✅ Paginação funciona (offset/limit)
  - ✅ Retorna 200 + array

**Estimate:** 2-3 horas

---

#### Task 2.3: Create endpoint GET /activity-grades/{id}
- **Description:** Consultar nota específica com controle de acesso
- **Files:** `atv2Lab/apis/activity-grades/3600557_activity_grades_get_by_id_GET.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair id do path param
  - [x] Query activity_grade por ID
  - [x] Validar que account_id corresponde
  - [x] Permitir: professor (dono), estudante (student_id), admin
  - [x] Retornar 404 se não encontra
  - [x] Retornar 403 se acesso negado
  - [x] Retornar 200 + objeto se permitido
- **Acceptance Criteria:**
  - ✅ Professor dono consegue ler
  - ✅ Aluno consegue ler sua nota
  - ✅ Outro professor recebe 403
  - ✅ Admin consegue ler qualquer uma
  - ✅ ID inválido retorna 404

**Estimate:** 2 horas

---

#### Task 2.4: Create endpoint PATCH /activity-grades/{id}
- **Description:** Atualizar nota com auditoria
- **Files:** `atv2Lab/apis/activity-grades/3600558_activity_grades_id_PATCH.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair ID e body {grade?, feedback?}
  - [x] Query nota atual
  - [x] Validar ownership (professor dono ou admin)
  - [x] Validar nova grade se fornecida (0-10)
  - [x] Atualizar campos fornecidos
  - [x] Logar em event_log com old/new values
  - [x] Retornar 200 + nota atualizada
- **Acceptance Criteria:**
  - ✅ Professor dono consegue atualizar
  - ✅ Apenas campos fornecidos são atualizados
  - ✅ Validação de grade funciona
  - ✅ Event log registra changes
  - ✅ updated_at atualizado automaticamente

**Estimate:** 2-3 horas

---

#### Task 2.5: Create endpoint DELETE /activity-grades/{id}
- **Description:** Deletar nota com auditoria
- **Files:** `atv2Lab/apis/activity-grades/3600559_activity_grades_id_DELETE.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair ID
  - [x] Query nota
  - [x] Validar ownership (professor dono ou admin)
  - [x] Deletar note (hard delete conforme non-goals)
  - [x] Logar em event_log (action="activity_grade_deleted")
  - [x] Retornar 204
- **Acceptance Criteria:**
  - ✅ Professor dono consegue deletar
  - ✅ Admin consegue deletar
  - ✅ Outro professor recebe 403
  - ✅ Event log criado
  - ✅ Retorna 204 (sem body)

**Estimate:** 1-2 horas

---

#### Task 2.6: Create endpoint GET /activity-grades/activity/{activity_id}
- **Description:** Listar todas as notas de uma atividade
- **Files:** `atv2Lab/apis/activity-grades/3600560_activity_grades_activity_id_GET.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair activity_id do path
  - [x] Query activity para validar + obter subject_id
  - [x] Query subject para obter owner_id
  - [x] Verificar: professor=owner OU role=admin
  - [x] Retornar 403 se acesso negado
  - [x] Query todas as notas da atividade com paginação
  - [x] Retornar 200 + array
- **Acceptance Criteria:**
  - ✅ Professor dono consegue listar
  - ✅ Admin consegue listar
  - ✅ Outro professor recebe 403
  - ✅ Paginação funciona
  - ✅ Retorna todas as notas da atividade

**Estimate:** 2-3 horas

---

#### Task 2.7: Create endpoint GET /activity-grades/my-grades
- **Description:** Listar notas recebidas pelo aluno (minhas notas)
- **Files:** `atv2Lab/apis/activity-grades/3600561_activity_grades_my_grades_GET.xs`
- **Subtasks:**
  - [x] Validar autenticação
  - [x] Extrair query params (limit, offset)
  - [x] Query todas as notas onde student_id = auth.user_id
  - [x] Filtrar por account_id
  - [x] Aplicar paginação
  - [x] Retornar 200 + array (feedback opcional, pode omitir detalhes sensíveis)
- **Acceptance Criteria:**
  - ✅ Aluno vê apenas suas notas (student_id=auth.user_id)
  - ✅ Paginação funciona
  - ✅ Admin vê conforme seu account
  - ✅ Retorna 200 + array

**Estimate:** 1-2 horas

---

#### Task 2.8: Create API group config
- **Description:** Agrupar endpoints de activity-grades
- **Files:** `atv2Lab/apis/activity-grades/api_group.xs`
- **Subtasks:**
  - [x] Definir group name = "Activity Grades"
  - [x] Adicionar descrição
  - [x] Referenciar todos os 7 endpoints
- **Acceptance Criteria:**
  - ✅ Group criado com sucesso
  - ✅ Endpoints aparecem agrupados no Xano UI

**Estimate:** 30 minutos

---

### PHASE 3: Integration & Testing

#### Task 3.1: Integration test - Complete flow
- **Description:** Teste de ponta a ponta (professor cria nota → aluno vê)
- **Files:** `atv2Lab/workflow_tests/activity_grades_integration_tests.xs`
- **Subtasks:**
  - [x] Setup: Criar usuários professor e aluno, subject e activity
  - [x] Test 1: Professor cria nota
  - [x] Test 2: Nota aparece em GET /activity-grades (professor)
  - [x] Test 3: Aluno vê nota em GET /activity-grades/my-grades
  - [x] Test 4: Professor atualiza nota
  - [x] Test 5: Outro professor recebe 403 ao tentar atualizar
  - [x] Test 6: Admin consegue atualizar
  - [x] Test 7: Deletar nota
  - [x] Validate event logs foram criados
- **Acceptance Criteria:**
  - ✅ Todos os 7 testes passam
  - ✅ RBAC enforcement validado
  - ✅ Event logging confirmado

**Estimate:** 3-4 horas

---

#### Task 3.2: Edge case testing
- **Description:** Testar casos extremos e erros
- **Subtasks:**
  - [x] Grade = 0.0 (mínimo)
  - [x] Grade = 10.0 (máximo)
  - [x] Grade = -0.1 (rejeitar)
  - [x] Grade = 10.1 (rejeitar)
  - [x] Feedback muito longo (performance)
  - [x] Duplicata - tentar criar segunda nota
  - [x] Activity inexistente
  - [x] Student inexistente
  - [x] Professor = Student (rejeitar)
- **Acceptance Criteria:**
  - ✅ Todos os casos tratados corretamente
  - ✅ Erros retornam status/mensagens apropriadas

**Estimate:** 2-3 horas

---

## Summary

| Phase | Tasks | Estimate | Owner |
|-------|-------|----------|-------|
| **Phase 1** Database & Validation | 3 | 4-7 horas | Backend |
| **Phase 2** API Endpoints | 8 | 15-20 horas | Backend |
| **Phase 3** Integration & Testing | 2 | 5-7 horas | QA |
| **TOTAL** | 13 | 24-34 horas | |

---

## Implementation Order

1. ✅ Phase 1.1 - Table (foundation)
2. ✅ Phase 1.2 - Validation function
3. ✅ Phase 1.3 - Ownership check function
4. ✅ Phase 2.1-2.5 - Core 5 CRUD endpoints (can parallelize)
5. ✅ Phase 2.6-2.7 - Additional query endpoints
6. ✅ Phase 2.8 - API group
7. ✅ Phase 3.1-3.2 - Testing

---

## Non-Goals (Explicitamente Excluídas)

As seguintes tarefas **NÃO** estão incluídas neste planejamento (conforme proposal.md):

- ❌ Cálculo automático de médias
- ❌ Notificações por email
- ❌ Dashboard/UI de visualização
- ❌ Importação em lote de notas
- ❌ Soft-delete (apenas hard delete)
- ❌ Triggers de auditoria (usar funções inline)
- ❌ Rate limiting

Estes podem ser adicionados em futuras iterações.

---

## Success Criteria - Final

- ✅ Todos os 23+ requisitos em spec.md implementados
- ✅ 7 endpoints CRUD funcionais e testados
- ✅ RBAC enforcement 100% validado
- ✅ Event logging para todas as operações
- ✅ Multi-tenant isolation confirmado
- ✅ Performance <500ms para queries com 10k+ notas
- ✅ Testes de integração passando
