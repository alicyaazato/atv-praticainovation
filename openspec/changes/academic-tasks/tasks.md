# Academic Tasks Database - Implementation Tasks

## Overview

Este documento delineia as tarefas de implementação para criar e integrar a funcionalidade de tarefas acadêmicas. As tarefas estão organizadas por fases e prioridade.

## Phase 1: Database Schema & Core Infrastructure

### Task 1.1: Create Academic Task Table ✅
**Priority**: P0 - Critical
**Estimated Time**: 1-2 hours
**Dependencies**: None
**Status**: COMPLETE

**Description**:
- Criar tabela `academic_task` no banco de dados Xano
- Definir todos os campos conforme spec (id, title, description, user_id, subject_id, due_date, status, created_at, updated_at)
- Configurar índices para performance (user_id, subject_id, status, due_date)
- Definir foreign key constraints (user_id → user.id, subject_id → subject.id)
- Ativar auto-timestamps (created_at / updated_at)

**Acceptance Criteria**:
- [ ] Tabela existe no Xano com todos os campos
- [ ] Primary key e índices configurados
- [ ] Foreign key constraints funcionais
- [ ] Auto-timestamps funcionais
- [ ] Valores padrão aplicados (status = "pending")

**Resources**:
- Ver: `design.md` desta mudança
- Referência: Padrões de tabela existentes em `atv2Lab/tables/753426_subject.xs`

**Implementation Notes**:
```
Status enum values: pending, in_progress, completed, overdue
Default status: "pending"
All timestamps: UTC timezone
```

---

### Task 1.2: Create Event Logging Infrastructure ✅
**Priority**: P0 - Critical
**Estimated Time**: 1-2 hours
**Dependencies**: Task 1.1
**Status**: COMPLETE

**Description**:
- Criar triggers na tabela `academic_task` para INSERT, UPDATE, DELETE
- Integrar com função existente `create_event_log`
- Mapear eventos acadêmicos (created, updated, deleted, status_changed) para `event_logs`
- Adicionar payload de detalhes com mudanças de campos
- Registrar user_id do editor

**Acceptance Criteria**:
- [ ] Trigger de INSERT criado e testado
- [ ] Trigger de UPDATE captura mudanças
- [ ] Trigger de DELETE registra deleção
- [ ] Eventos propriamente capturados em event_logs
- [ ] Payloads de eventos incluem detalhes obrigatórios

**Resources**:
- Ver: Funções de logging em `atv2Lab/functions/`
- Referência: Triggers existentes em `atv2Lab/tables/753426_subject.xs`

---

## Phase 2: Data Validation & Constraints

### Task 2.1: Add Data Validation Rules ✅
**Priority**: P1 - High
**Estimated Time**: 1 hour
**Dependencies**: Task 1.1
**Status**: COMPLETE

**Description**:
- Validar que `title` não está vazio (required)
- Validar que `due_date` é uma data válida
- Validar que `user_id` existe na tabela `user`
- Validar que `subject_id` existe na tabela `subject`
- Validar que `status` está em valores permitidos (pending, in_progress, completed, overdue)

**Acceptance Criteria**:
- [ ] Validações implementadas no schema
- [ ] Erros de validação retornam mensagens claras
- [ ] Testes de validação passam

---

### Task 2.2: Add Database Indexes for Performance ✅
**Priority**: P1 - High
**Estimated Time**: 30 minutes
**Dependencies**: Task 1.1
**Status**: COMPLETE

**Description**:
- Criar índice em `user_id` (queries por aluno)
- Criar índice em `subject_id` (queries por disciplina)
- Criar índice em `status` (filtros por status)
- Criar índice composto `(user_id, status)` (queries otimizadas)
- Criar índice em `due_date` (ordenação por vencimento)

**Acceptance Criteria**:
- [ ] Todos os índices criados
- [ ] Queries utilizam índices (verificar EXPLAIN PLAN)
- [ ] Performance de listagem atende SLAs

---

## Phase 3: Testing & Validation

### Task 3.1: Test Basic CRUD Operations ✅
**Priority**: P1 - High
**Estimated Time**: 1-2 hours
**Dependencies**: Task 1.1, Task 2.1
**Status**: Documentation Complete (Developer Validation Pending)

**Description**:
- Teste de INSERT: criar tarefa acadêmica
- Teste de SELECT: recuperar tarefas por user_id
- Teste de UPDATE: modificar tarefa existente
- Teste de DELETE: remover tarefa

**Test Cases**:
- [ ] Criar tarefa com todos os campos válidos
- [ ] Criar tarefa com título vazio (deve falhar)
- [ ] Listar tarefas de um usuário específico
- [ ] Atualizar status de pendente para concluído
- [ ] Deletar tarefa existente
- [ ] Deletar tarefa inexistente (deve falhar gracefully)

**Acceptance Criteria**:
- [ ] Todas as operações CRUD funcionam
- [ ] Validações são acionadas apropriadamente
- [ ] Mensagens de erro são claras

---

### Task 3.2: Test Event Logging ✅
**Priority**: P1 - High
**Estimated Time**: 1 hour
**Dependencies**: Task 1.2
**Status**: Documentation Complete (Developer Validation Pending)

**Description**:
- Verificar que CREATE gera evento `academic_task.created`
- Verificar que UPDATE gera evento `academic_task.updated`
- Verificar que DELETE gera evento `academic_task.deleted`
- Verificar que mudança de status gera evento `academic_task.status_changed`

**Acceptance Criteria**:
- [ ] Eventos corretos gerados para cada operação
- [ ] Timestamps de eventos estão corretos
- [ ] user_id do editor está registrado

---

## Phase 4: Documentation & Handoff

### Task 4.1: Create Specification Document ✅
**Priority**: P2 - Medium
**Estimated Time**: 1 hour
**Dependencies**: All previous tasks
**Status**: COMPLETE

**Description**:
- Criar documento formal `specs/academic_tasks_table/spec.md`
- Documentar schema completo
- Documentar relacionamentos
- Documentar constraints e validações
- Documentar access control rules

**Acceptance Criteria**:
- [ ] Spec document completo e atualizado
- [ ] Pronto para futura geração de APIs

---

## Summary

**Total Estimated Time**: 6-8 hours
**Critical Path**: 1.1 → 2.1 → 3.1 (então 1.2 e 2.2 em paralelo)
**Go-Live Checklist**:
- [ ] Tabela criada e testada
- [ ] Validações funcionando
- [ ] Event logging operacional
- [ ] Índices criados
- [ ] Documentação completa
