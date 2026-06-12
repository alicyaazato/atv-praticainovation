# Evolução das Disciplinas e Tarefas - Implementation Tasks

## Overview

Tarefas a executar **no Xano**, na segunda etapa do projeto. Nenhuma
depende de mudanças adicionais no front-end (Streamlit) — o app já está
preparado para consumir esses campos quando existirem.

## Phase 1: Conciliação do enum `status` (academic_task)

### Task 1.1: Auditar valores de `status` gravados
**Priority**: P0 - Bloqueante
**Dependencies**: Nenhuma

- Consultar a tabela `academic_task` no Xano e listar os valores distintos
  de `status` em uso.
- Comparar com `utils/api_client.STATUS_LABELS` (`Pendente`,
  `Em_progresso`, `Completa`, `Atrasada`) e com o enum documentado em
  `tables/842368_academic_task.xs` (`pending`, `in_progress`, `completed`,
  `overdue`).

**Acceptance Criteria**:
- [ ] Lista de valores distintos de `status` documentada
- [ ] Decisão registrada: qual conjunto de valores é a fonte da verdade

### Task 1.2: Atualizar `tables/842368_academic_task.xs`
**Priority**: P0 - Bloqueante
**Dependencies**: Task 1.1

- Ajustar o enum `status` (valores e default) para refletir a decisão da
  Task 1.1.
- Se houver dados legados com o conjunto de valores divergente, planejar e
  executar migração de normalização.

**Acceptance Criteria**:
- [ ] Enum `status` em `tables/842368_academic_task.xs` reflete os dados
      reais
- [ ] Nenhum registro com valor de `status` fora do enum

---

## Phase 2: Disciplina — `status` e `semester`

### Task 2.1: Adicionar campos em `tables/809944_subject.xs`
**Priority**: P1 - Alta
**Dependencies**: Nenhuma

- Adicionar `status` (enum: `rascunho` | `ativo` | `arquivado`, default
  `ativo`).
- Adicionar `semester` (texto, opcional).

**Acceptance Criteria**:
- [ ] Campos criados na tabela com os tipos/defaults corretos
- [ ] Registros existentes recebem `status = "ativo"` por padrão

### Task 2.2: Atualizar `apis/subjects/subjects_POST.xs`
**Priority**: P1 - Alta
**Dependencies**: Task 2.1

- Aceitar `status` (default `"ativo"`) e `semester` (opcional) no payload.
- Validar `status` contra o enum.

**Acceptance Criteria**:
- [ ] POST aceita os novos campos
- [ ] POST sem os novos campos continua funcionando (defaults aplicados)

### Task 2.3: Criar/atualizar endpoint de update parcial de subject
**Priority**: P1 - Alta
**Dependencies**: Task 2.1

- Garantir que existe um `PATCH /subjects/{id}` que aceite `status` e
  `semester` como campos parciais (para suportar "arquivar disciplina" e
  edição de período pela UI).

**Acceptance Criteria**:
- [ ] PATCH aceita `status` e `semester` isoladamente
- [ ] Transição para `arquivado` funciona

---

## Phase 3: Tarefa — `priority`

### Task 3.1: Adicionar campo em `tables/842368_academic_task.xs`
**Priority**: P1 - Alta
**Dependencies**: Phase 1 concluída

- Adicionar `priority` (enum: `Baixa` | `Média` | `Alta`, default `Média`).

**Acceptance Criteria**:
- [ ] Campo criado com tipo/default corretos
- [ ] Registros existentes recebem `priority = "Média"` por padrão

### Task 3.2: Atualizar `apis/tasks/tasks_POST.xs` e update parcial
**Priority**: P1 - Alta
**Dependencies**: Task 3.1

- Aceitar `priority` (default `"Média"`) no POST.
- Aceitar `priority` como campo parcial no PATCH de update de tarefa.

**Acceptance Criteria**:
- [ ] POST e PATCH aceitam `priority`
- [ ] Requisições sem `priority` continuam funcionando (default aplicado)

---

## Phase 4: Magic link de redefinição de senha

### Task 4.1: Corrigir URL no template de e-mail
**Priority**: P2 - Média
**Dependencies**: Nenhuma

- Atualizar `apis/authentication/3600536_reset_request_reset_link_GET.xs`
  para montar o link apontando para a página **Perfil** do app Streamlit
  publicado, com `magic_token` e `email` na query string.

**Acceptance Criteria**:
- [ ] E-mail de redefinição contém link para o app Streamlit
- [ ] Fluxo completo testado: solicitar reset → clicar no link → app loga
      o usuário e exibe o formulário de nova senha (já implementado em
      `pages/3_👤_Perfil.py`)

---

## Summary

**Ordem recomendada**: Phase 1 → Phase 2 e Phase 3 (podem ser paralelas) →
Phase 4 (independente, pode ser feita em qualquer momento).

**Após conclusão**, abrir uma nova proposta de front-end para consumir
`subject.status`/`subject.semester` (Dashboard, Disciplinas) e
`academic_task.priority` (Tarefas, Relatórios).
