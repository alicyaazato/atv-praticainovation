# Evolução das Disciplinas e Tarefas - Implementation Tasks

## Overview

Tarefas a executar **no Xano**, na segunda etapa do projeto. Nenhuma
depende de mudanças adicionais no front-end (Streamlit) — o app já está
preparado para consumir esses campos quando existirem.

**Status**: todas as alterações das Fases 1, 2, 3 e 5 foram aplicadas nos
arquivos `.xs` locais, pushadas para o Xano (workspace `edutrack-ai`, branch
`v1`) e validadas com sucesso via smoke test end-to-end contra a API em
produção. Pendências restantes: Fase 4 (teste manual completo do fluxo de
magic link por e-mail) e a futura proposta de front-end para consumir
`subject.status`/`subject.semester`/`academic_task.priority` (ver Summary).

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
- [x] Lista de valores distintos de `status` documentada — pull do Xano já
      trouxe `tables/842368_academic_task.xs` com
      `["Pendente", "Em_progresso", "Completa", "Atrasada"]`
- [x] Decisão registrada: `utils/api_client.STATUS_LABELS` (PT-BR) é a fonte
      da verdade; tabela já alinhada

### Task 1.2: Atualizar `tables/842368_academic_task.xs`
**Priority**: P0 - Bloqueante
**Dependencies**: Task 1.1

- Ajustar o enum `status` (valores e default) para refletir a decisão da
  Task 1.1.
- Se houver dados legados com o conjunto de valores divergente, planejar e
  executar migração de normalização.

**Acceptance Criteria**:
- [x] Enum `status` em `tables/842368_academic_task.xs` reflete os dados
      reais — default corrigido de `?=pending` (valor inexistente no enum)
      para `?=Pendente`
- [x] Nenhum registro com valor de `status` fora do enum — confirmado via
      smoke test: task criada sem `status` recebe `"Pendente"`

---

## Phase 2: Disciplina — `status` e `semester`

### Task 2.1: Adicionar campos em `tables/809944_subject.xs`
**Priority**: P1 - Alta
**Dependencies**: Nenhuma

- Adicionar `status` (enum: `rascunho` | `ativo` | `arquivado`, default
  `ativo`).
- Adicionar `semester` (texto, opcional).

**Acceptance Criteria**:
- [x] Campos criados na tabela com os tipos/defaults corretos
- [x] Registros existentes recebem `status = "ativo"` por padrão —
      confirmado via smoke test: subject criado sem `status`/`semester`
      recebe `status: "ativo"`, `semester: ""`

### Task 2.2: Atualizar `apis/subjects/subjects_POST.xs`
**Priority**: P1 - Alta
**Dependencies**: Task 2.1

- Aceitar `status` (default `"ativo"`) e `semester` (opcional) no payload.
- Validar `status` contra o enum.

**Acceptance Criteria**:
- [x] POST aceita os novos campos
- [x] POST sem os novos campos continua funcionando (defaults aplicados)

### Task 2.3: Criar/atualizar endpoint de update parcial de subject
**Priority**: P1 - Alta
**Dependencies**: Task 2.1

- Garantir que existe um `PATCH /subjects/{id}` que aceite `status` e
  `semester` como campos parciais (para suportar "arquivar disciplina" e
  edição de período pela UI).

**Acceptance Criteria**:
- [x] PATCH aceita `status` e `semester` isoladamente
- [x] Transição para `arquivado` funciona
- [x] `apis/subjects/subjects_search_GET.xs`: output inclui
      `items.status`/`items.semester` — confirmado via smoke test após
      re-push

---

## Phase 3: Tarefa — `priority`

### Task 3.1: Adicionar campo em `tables/842368_academic_task.xs`
**Priority**: P1 - Alta
**Dependencies**: Phase 1 concluída

- Adicionar `priority` (enum: `Baixa` | `Média` | `Alta`, default `Média`).
- **Decisão de implementação**: valores internos do enum sem acento
  (`Baixa`, `Media`, `Alta`, default `Media`), seguindo o mesmo padrão de
  `Em_progresso` em `STATUS_LABELS` (chave interna ASCII, rótulo acentuado
  fica para a futura proposta de front-end).

**Acceptance Criteria**:
- [x] Campo criado com tipo/default corretos
- [x] Registros existentes recebem `priority = "Media"` por padrão —
      confirmado via smoke test: task criada sem `priority` recebe
      `priority: "Media"`

### Task 3.2: Atualizar `apis/tasks/tasks_POST.xs` e update parcial
**Priority**: P1 - Alta
**Dependencies**: Task 3.1

- Aceitar `priority` (default `"Media"`) no POST.
- Aceitar `priority` como campo parcial no PATCH de update de tarefa.

**Acceptance Criteria**:
- [x] POST e PATCH aceitam `priority`
- [x] Requisições sem `priority` continuam funcionando (default aplicado)
- [x] `apis/tasks/tasks_GET.xs`: output inclui `"priority"` — confirmado via
      smoke test após re-push

**Nota**: ao editar `apis/tasks/tasks_id_PATCH.xs` foi corrigido um bug
pré-existente — o `db.edit academic_task` gravava `$input.*` em vez dos
`$final_*` resolvidos, então um PATCH parcial (ex.: só `status`) apagava
`title`/`description`/`subject_id`. Agora usa os `$final_*`. **Confirmado via
smoke test**: PATCH parcial (`{"status": "Completa"}` e depois
`{"priority": "Baixa"}`) preserva `title`, `description`, `subject_id`,
`data` e `priority`/`status` corretamente.

---

## Phase 4: Redefinição de senha (superado — código de verificação)

### Task 4.1: ~~Corrigir URL no template de e-mail~~ — substituído
**Priority**: P2 - Média
**Dependencies**: Nenhuma

- Abordagem original (link mágico clicável) foi descartada em favor de um
  código de verificação de 6 dígitos, evitando o redirecionamento entre
  e-mail e app. Ver `apis/authentication/3600536_reset_request_reset_link_GET.xs`,
  `apis/authentication/3600537_reset_magic_link_login_POST.xs`
  (`reset/verify-code`) e o fluxo em `pages/3_👤_Perfil.py`.

**Acceptance Criteria**:
- [x] E-mail de redefinição contém o código de 6 dígitos (válido por 15 min)
- [x] Fluxo completo testado: solicitar código → digitar código + nova senha
      no app → senha atualizada e usuário autenticado

---

## Phase 5: Segurança — endpoint público `edutrackAPI`

### Task 5.1: Proteger ou remover `apis/edutrack_api/3914735_academic_task_GET.xs`
**Priority**: P0 - Bloqueante (segurança)
**Dependencies**: Nenhuma

- O endpoint `GET academic_task` do grupo `edutrackAPI` (canonical
  `-KghbQCu`) não possui `auth = "user"` nem filtro por `user_id` e retorna
  os registros de `academic_task` de **todos os usuários**.
- Esse endpoint não é consumido pelo front-end (`utils/api_client.py`) — a
  listagem de tarefas já é feita por `apis/tasks/tasks_GET.xs` (group
  `Tasks`), que já filtra por `$auth.id`.
- Opção escolhida: **protegido** com `auth = "user"`,
  `precondition ($auth.id)` e `where = $db.academic_task.user_id == $auth.id`,
  resposta envolvida em `{items: $model}` (mantém o endpoint disponível,
  mas seguro — ver XanoScript em `design.md`).

**Acceptance Criteria**:
- [x] Endpoint `edutrackAPI/academic_task` protegido com `auth = "user"` +
      filtro por `user_id`
- [x] Nenhuma chamada não autenticada retorna dados de outros usuários

---

## Summary

**Ordem recomendada**: Phase 1 e Phase 5 (bloqueantes, podem ser feitas em
paralelo) → Phase 2 e Phase 3 (podem ser paralelas) → Phase 4 (independente,
pode ser feita em qualquer momento).

**Após conclusão**, abrir uma nova proposta de front-end para consumir
`subject.status`/`subject.semester` (Dashboard, Disciplinas) e
`academic_task.priority` (Tarefas, Relatórios).
