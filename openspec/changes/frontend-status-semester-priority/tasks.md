# Frontend: Status/Semestre da Disciplina e Prioridade da Tarefa - Implementation Tasks

## Overview

Implementação **no front-end (Streamlit)**, consumindo os campos
`subject.status`, `subject.semester` e `academic_task.priority` já
disponíveis na API (validados em `evolucao-disciplinas-tarefas`). Nenhuma
mudança adicional no Xano é necessária.

**Ordem recomendada**: Phase 1 (helpers compartilhados) bloqueia as demais.
Phases 2 e 3 podem ser feitas em paralelo. Phases 4 e 5 dependem de 1, 2 e 3.

---

## Phase 1: `utils/api_client.py` — labels e helper compartilhados

### Task 1.1: Adicionar mapas de status/prioridade
**Priority**: P0 - Bloqueante
**Dependencies**: Nenhuma

- Adicionar `SUBJECT_STATUS_LABELS` / `SUBJECT_STATUS_OPTIONS`
  (`rascunho`/`ativo`/`arquivado`).
- Adicionar `PRIORITY_LABELS` / `PRIORITY_OPTIONS` / `PRIORITY_ICONS` /
  `PRIORITY_WEIGHT` (`Baixa`/`Media`/`Alta`), seguindo o padrão de
  `STATUS_LABELS` (`utils/api_client.py:17-23`).

**Acceptance Criteria**:
- [x] Constantes adicionadas e exportadas
- [x] Nenhuma página hardcoda os valores de enum diretamente

### Task 1.2: Adicionar `build_subject_payload()`
**Priority**: P0 - Bloqueante
**Dependencies**: Nenhuma

- Análogo a `build_task_payload()` (`utils/api_client.py:198-209`), incluindo
  `name`, `professor`, `carga_horaria`, `status`, `semester`.

**Acceptance Criteria**:
- [x] Função disponível e usada pelas edições de disciplina (Phase 2)

---

## Phase 2: Disciplinas (`pages/1_📚_Disciplinas.py`)

### Task 2.1: Campos `status`/`semester` no formulário "Nova Disciplina"
**Priority**: P1 - Alta
**Dependencies**: Task 1.1

- Adicionar seletor de Status (default "Ativo") e campo de texto
  Semestre/Período (opcional) ao formulário de criação.
- Incluir `status`/`semester` no payload de `create_subject`.

**Acceptance Criteria**:
- [x] Criar disciplina sem informar status/semestre continua funcionando
      (defaults da API: `ativo`/`""`)
- [x] Criar disciplina com `status="rascunho"` e `semester="2026/1"` reflete
      esses valores na listagem — testado via `AppTest`: disciplina criada
      pelo formulário aparece com `status: "rascunho"`, `semester: "2026/1"`

### Task 2.2: Edição de `status`/`semester` + atalho arquivar/reativar
**Priority**: P1 - Alta
**Dependencies**: Task 1.1, Task 1.2

- Adicionar os mesmos dois campos ao formulário de edição de cada
  disciplina, com valores atuais como default.
- Botão "📦 Arquivar" (quando `status != "arquivado"`) / "♻️ Reativar"
  (quando `status == "arquivado"`) que faz PATCH só de `status` via
  `build_subject_payload`.

**Acceptance Criteria**:
- [x] Editar semestre de uma disciplina existente persiste e aparece após
      `st.rerun()` — testado via `AppTest`: editar `status`/`semester` no
      formulário e salvar reflete `status: "arquivado", semester: "2026/2"`
      na API
- [x] "📦 Arquivar" muda `status` para `arquivado` e o botão alterna para
      "♻️ Reativar" — testado via `AppTest`: clicar em "📦 Arquivar" altera
      `status` para `"arquivado"` na API
- [x] "♻️ Reativar" retorna `status` para `ativo`

### Task 2.3: Filtro por status na aba "Minhas Disciplinas"
**Priority**: P1 - Alta
**Dependencies**: Nenhuma

- Adicionar `st.selectbox` "Mostrar": Ativas (default) / Arquivadas /
  Rascunhos / Todas.
- Exibir semestre (se preenchido) e ícone 📦 (se arquivada) no título do
  `st.expander`.

**Acceptance Criteria**:
- [x] Filtro "Ativas" (default) oculta disciplinas arquivadas — testado via
      `AppTest`: disciplina `status: "rascunho"` não aparece com "Ativas"
- [x] Filtro "Arquivadas"/"Rascunhos" mostra só os respectivos `status`
- [x] Filtro "Todas" mostra tudo, com badges de status/semestre — título do
      expander exibe `· {semester}` e `📦` quando arquivada

### Task 2.4: Exibir `status`/`semester` na aba "Buscar"
**Priority**: P2 - Média
**Dependencies**: Nenhuma

- Mostrar status (se != "ativo") e semestre (se preenchido) nos resultados
  de busca, mesmo formato da Task 2.3.

**Acceptance Criteria**:
- [x] Resultado de busca de uma disciplina arquivada/rascunho exibe o status
      — testado via `AppTest`: busca retorna `**Status:** Arquivado`
- [x] Resultado com `semester` preenchido exibe o período — testado via
      `AppTest`: busca retorna `**Semestre:** 2026/2`

---

## Phase 3: Tarefas (`pages/2_📝_Tarefas.py`)

### Task 3.1: Campo `priority` no formulário "Nova Tarefa"
**Priority**: P1 - Alta
**Dependencies**: Task 1.1

- Adicionar seletor de Prioridade (default "Média").
- Incluir `priority` no payload de `create_task`.

**Acceptance Criteria**:
- [x] Criar tarefa sem definir prioridade continua funcionando (default
      `Media`) — testado via `AppTest`: seletor "Prioridade" no formulário
      "Nova Tarefa" tem default `Media`
- [x] Criar tarefa com `priority="Alta"` reflete esse valor na listagem —
      testado via `AppTest`: tarefa criada pelo formulário com `priority="Alta"`
      aparece com `priority: "Alta"` na API

### Task 3.2: Campo `priority` na edição + badge na listagem
**Priority**: P1 - Alta
**Dependencies**: Task 1.1

- Adicionar seletor de Prioridade ao formulário de edição (valor atual como
  default), incluído em `build_task_payload`.
- Prefixar o título de cada `st.expander` com o ícone de
  `PRIORITY_ICONS[t.get("priority", "Media")]`.

**Acceptance Criteria**:
- [x] Alterar prioridade de uma tarefa existente persiste e aparece após
      `st.rerun()` — testado via `AppTest`: editar prioridade de "Media" para
      "Alta" e salvar reflete `priority: "Alta"` na API
- [x] Tarefas com prioridade "Alta" exibem 🔴 no título — testado via
      `AppTest`: título do expander começa com `🔴` para prioridade Alta, `🟡`
      para Média e `🟢` para Baixa

### Task 3.3: Filtro e agrupamento por prioridade
**Priority**: P2 - Média
**Dependencies**: Task 1.1

- Adicionar filtro "Prioridade" (Todas / Baixa / Média / Alta), combinável
  com o filtro de status existente.
- Adicionar "Prioridade" como opção de "Agrupar por", ordenando os grupos por
  `PRIORITY_WEIGHT` decrescente (Alta primeiro).

**Acceptance Criteria**:
- [x] Filtro "Prioridade = Alta" mostra só tarefas com `priority == "Alta"` —
      testado via `AppTest`: com filtro "Alta", apenas a tarefa de prioridade
      Alta aparece na listagem
- [x] "Agrupar por: Prioridade" lista os grupos na ordem Alta → Média → Baixa —
      testado via `AppTest`: cabeçalhos `### Alta`, `### Média`, `### Baixa`
      aparecem nessa ordem

---

## Phase 4: Dashboard (`app.py`)

### Task 4.1: Métrica "Disciplinas Ativas"
**Priority**: P1 - Alta
**Dependencies**: Task 1.1

- Métrica "📚 Disciplinas" passa a contar só `status == "ativo"` e é
  renomeada para "Disciplinas Ativas".
- "Progresso por Disciplina" e `progresso_geral` usam apenas disciplinas
  ativas.
- Tela de boas-vindas (`if not subjects`) continua considerando todas as
  disciplinas (não muda).

**Acceptance Criteria**:
- [x] Disciplina arquivada não conta na métrica nem no progresso geral —
      testado via `AppTest`: com 1 disciplina ativa e 1 arquivada, métrica
      "📚 Disciplinas Ativas" = 1 e "Progresso por Disciplina" mostra só a
      ativa
- [x] Usuário com só disciplinas arquivadas/rascunho ainda vê a tela de
      boas-vindas (se `subjects` total estiver vazio) ou o dashboard vazio
      de ativas (se houver arquivadas mas nenhuma ativa) — testado via
      `AppTest`: usuário com 1 disciplina arquivada (nenhuma ativa) não vê a
      tela de boas-vindas, métrica = 0, "Progresso Geral" = 0% e
      "Progresso por Disciplina" exibe "Nenhuma disciplina ativa."

### Task 4.2: Seção "Tarefas por Prioridade"
**Priority**: P2 - Média
**Dependencies**: Task 1.1

- Nova seção espelhando "Tarefas por Status", em uma segunda linha de
  colunas abaixo de `col_status`/`col_progress`.

**Acceptance Criteria**:
- [x] Seção mostra contagem de tarefas por prioridade com ícone — testado via
      `AppTest`: linhas `🟢 **Baixa:** 1`, `🟡 **Média:** 2`, `🔴 **Alta:** 1`
- [x] Soma das contagens é igual ao total de tarefas — testado via `AppTest`:
      1+2+1 = 4, igual ao total de tarefas criadas

---

## Phase 5: Relatórios (`pages/4_📈_Relatorios.py`)

### Task 5.1: Coluna "Prioridade" no histórico/CSV
**Priority**: P2 - Média
**Dependencies**: Task 1.1

- Adicionar `"Prioridade"` ao dict `linhas` do histórico de tarefas.

**Acceptance Criteria**:
- [ ] Coluna "Prioridade" aparece na tabela e no CSV exportado

### Task 5.2: Checkbox "Incluir disciplinas arquivadas"
**Priority**: P2 - Média
**Dependencies**: Task 1.1

- Checkbox (default desmarcado) que inclui/exclui disciplinas com
  `status == "arquivado"` da seção "Progresso por Disciplina".

**Acceptance Criteria**:
- [ ] Por padrão, disciplinas arquivadas não aparecem em "Progresso por
      Disciplina"
- [ ] Marcando o checkbox, elas voltam a aparecer

---

## Verificação

- `streamlit run app.py` localmente:
  - Criar disciplina com status "Rascunho" e semestre "2026/2" → aparece
    correto na listagem e na busca.
  - Arquivar uma disciplina → some do filtro "Ativas" do Dashboard e da aba
    "Minhas Disciplinas" (default), métrica "Disciplinas Ativas" diminui.
  - Reativar → volta a aparecer.
  - Criar/editar tarefa com prioridade "Alta" → badge 🔴 na listagem, aparece
    em "Tarefas por Prioridade" no Dashboard e na coluna "Prioridade" dos
    Relatórios/CSV.
  - Filtros e agrupamento por prioridade em Tarefas funcionam combinados com
    o filtro de status existente.
