# Plano de Implementação — Conclusão do checklist.md (EduTrack AI)

> Roadmap acordado para fechar os requisitos de `checklist.md`. Cobre apenas
> a parte de **código** (Streamlit/Python). A parte que depende de mudanças
> no Xano fica documentada na Fase 7 (proposal OpenSpec), para execução numa
> segunda etapa.

## Situação atual

A maior parte dos itens "obrigatórios" do checklist (Autenticação,
Disciplinas, Tarefas) já está implementada em `pages/1_📚_Disciplinas.py`,
`pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py`, usando os endpoints já
existentes em `apis/subjects`, `apis/tasks` e `apis/authentication`.

Faltam:

- Confirmação antes de excluir (disciplinas/tarefas)
- Fluxo "esqueci minha senha" (endpoints já existem, falta UI)
- Encerrar sessão automaticamente ao expirar o token
- Dashboard real (`app.py` hoje é um stub com métricas fixas em "0")
- Página de Relatórios/Progresso com export
- Identidade visual consistente + tela de boas-vindas + navegação
  condicional (Login/Registro apenas quando não autenticado, conforme
  `agent-estrutura.md`)

Os itens de "Evolução das Disciplinas e Tarefas" (semestre/período em
disciplina, prioridade em tarefa, status rascunho/ativo/arquivado) exigem
**novos campos no Xano** (não existem em `tables/809944_subject.xs` nem em
`tables/842368_academic_task.xs`) — ficam para a Fase 7 (documentação, sem
implementação agora).

Também identificado e corrigido: `apis/subjects/subjects_search_GET.xs`
estava com marcadores de conflito de merge não resolvidos.

---

## Fase 1 — Módulo compartilhado `utils/api_client.py`

Centraliza o que hoje está duplicado em cada página (headers de auth,
chamadas `requests`):

- Constantes de URL fixas no código (`AUTH_URL`, `EDIT_URL`, `SUBJECTS_URL`,
  `TASKS_URL`) — projeto de faculdade não usa `.env`
- `STATUS_LABELS` (fonte única, conforme `agent-estrutura.md`)
- Helpers de sessão: `get_token`, `set_token`, `clear_token`, `is_authenticated`
- `request()`: wrapper genérico que trata `401` limpando a sessão
- `require_session()`: guarda de página (sessão expirada / não autenticado)
- Funções CRUD de subjects, tasks e auth/perfil
- `confirm_delete_button()`: confirmação em 2 passos via `st.session_state`

## Fase 2 — Navegação condicional + Dashboard real (`app.py`)

- Reescrever `app.py` com `st.navigation` / `st.Page`
- Não autenticado → só página de Login/Cadastro
- Autenticado → Dashboard, Disciplinas, Tarefas, Relatórios, Perfil
- Dashboard com métricas reais: disciplinas, tarefas pendentes/atrasadas,
  progresso geral, tarefas por status, progresso por disciplina, próximas
  tarefas, e tela de boas-vindas quando não há disciplinas cadastradas

## Fase 3 — Refatorar Disciplinas e Tarefas

- Usar `utils.api_client` (sem duplicação)
- `require_session()` no lugar da checagem manual de auth
- Confirmação antes de excluir disciplina/tarefa

## Fase 4 — Perfil: refator + "Esqueci minha senha"

- Usar `utils.api_client`
- Aba de login ganha "Esqueci minha senha" (`GET /reset/request-reset-link`)
- Tratamento do magic link via `st.query_params` (`POST /reset/magic-link-login`)
- Observação: o link do e-mail hoje aponta para a demo page do Xano — corrigir
  na Fase 7

## Fase 5 — Página de Relatórios (`pages/4_📈_Relatorios.py`)

- Filtro por período e disciplina
- Histórico de tarefas no período + progresso por disciplina
- Export CSV (stdlib `csv`/`io`, sem novas dependências)

## Fase 6 — Identidade visual e UX

- `.streamlit/config.toml` com tema (cores/fonte)
- Ajustes de layout nas abas de login/cadastro

## Fase 7 — Documentação "fase Xano" (OpenSpec)

`openspec/changes/evolucao-disciplinas-tarefas/` descrevendo, sem implementar:

- `subject`: campo `status` (rascunho/ativo/arquivado) e `semester`/`periodo`
- `academic_task`: campo `priority` (Baixa/Média/Alta)
- Corrigir URL do magic link de reset de senha para apontar ao app Streamlit
- Verificar divergência de valores de `status` entre tabela (inglês) e
  labels do front (português) antes de implementar filtros dependentes

---

## Verificação

- `streamlit run app.py`: nav condicional, Dashboard com dados reais ou tela
  de boas-vindas, confirmação de exclusão, expiração de sessão, Relatórios
  com filtro e export CSV
- Nenhuma página além de `app.py` chama `st.set_page_config`
- `apis/subjects/subjects_search_GET.xs` sem marcadores de conflito
