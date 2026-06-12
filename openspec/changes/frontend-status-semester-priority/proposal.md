# Frontend: Status/Semestre da Disciplina e Prioridade da Tarefa - Proposal

## Summary

A proposta `evolucao-disciplinas-tarefas` já foi implementada e validada no
Xano: `subject` agora tem `status` (`rascunho`/`ativo`/`arquivado`) e
`semester`, e `academic_task` agora tem `priority`
(`Baixa`/`Media`/`Alta`). Esta proposta cobre o **front-end (Streamlit)**
para que o usuário consiga visualizar, definir e filtrar por esses campos —
hoje a API já os retorna, mas nenhuma página os exibe ou edita.

## Problem

- **Disciplinas**: não é possível arquivar uma disciplina (encerrar o
  semestre sem excluir o histórico), nem informar/visualizar o
  semestre/período. O formulário de "Nova Disciplina" e o de edição em
  `pages/1_📚_Disciplinas.py` não enviam `status`/`semester`.
- **Tarefas**: não é possível definir ou ver a prioridade de uma tarefa.
  `pages/2_📝_Tarefas.py` não tem campo de prioridade no formulário de
  criação/edição, nem exibe/filtra por `priority`.
- **Dashboard** (`app.py`): a métrica "📚 Disciplinas" conta todas as
  disciplinas, inclusive arquivadas/rascunho, o que infla o número conforme
  o usuário avança nos semestres. Não há visão de tarefas por prioridade.
- **Relatórios** (`pages/4_📈_Relatorios.py`): o histórico de tarefas e o CSV
  exportado não incluem `priority`; "Progresso por Disciplina" mistura
  disciplinas ativas e arquivadas.
- `utils/api_client.py` já tem `STATUS_LABELS`/`STATUS_OPTIONS` para o status
  da tarefa, mas não tem equivalentes para `subject.status` ou
  `academic_task.priority` — cada página teria que hardcodar esses valores
  de novo.

## Solution

1. **`utils/api_client.py`**: adicionar `SUBJECT_STATUS_LABELS`/
   `SUBJECT_STATUS_OPTIONS` (rascunho/ativo/arquivado) e `PRIORITY_LABELS`/
   `PRIORITY_OPTIONS` (Baixa/Média/Alta), seguindo o mesmo padrão de
   `STATUS_LABELS` (chave ASCII interna -> rótulo acentuado exibido).
   Adicionar `build_subject_payload()` análogo ao `build_task_payload()` já
   existente, para PATCH parcial sem apagar campos.
2. **Disciplinas** (`pages/1_📚_Disciplinas.py`):
   - Formulário "Nova Disciplina": campo opcional **Semestre/Período**
     (texto, ex.: "2026/1") e seletor de **Status** (default "Ativo").
   - Formulário de edição: os mesmos campos, mais um botão de atalho
     "📦 Arquivar" / "♻️ Reativar" que faz PATCH só de `status`.
   - Aba "Minhas Disciplinas": filtro por status (Ativas / Arquivadas /
     Rascunhos / Todas — default "Ativas"), exibir badge de semestre.
   - Aba "Buscar": exibir status/semestre nos resultados.
3. **Tarefas** (`pages/2_📝_Tarefas.py`):
   - Formulário "Nova Tarefa": seletor de **Prioridade** (default "Média").
   - Formulário de edição: mesmo seletor.
   - Aba "Minhas Tarefas": filtro adicional por prioridade, opção de
     "Agrupar por" incluindo "Prioridade", badge de prioridade no título do
     expander (ex.: 🔥 para Alta).
4. **Dashboard** (`app.py`):
   - Métrica "📚 Disciplinas" passa a contar apenas `status == "ativo"`
     (renomear para "Disciplinas Ativas"); disciplinas arquivadas/rascunho
     não entram no cálculo de progresso geral.
   - Nova seção "Tarefas por Prioridade" (mesmo padrão de "Tarefas por
     Status"), usando `PRIORITY_LABELS`.
5. **Relatórios** (`pages/4_📈_Relatorios.py`):
   - Coluna "Prioridade" no histórico de tarefas e no CSV exportado.
   - "Progresso por Disciplina" passa a considerar só disciplinas com
     `status == "ativo"` por padrão, com checkbox "Incluir arquivadas".

## Goals

- Expor `subject.status`, `subject.semester` e `academic_task.priority` em
  todas as páginas relevantes (criação, edição, listagem, busca, dashboard,
  relatórios).
- Permitir arquivar/reativar uma disciplina sem excluí-la.
- Permitir definir e filtrar tarefas por prioridade.
- Manter o padrão existente de `*_LABELS`/`*_OPTIONS` centralizados em
  `utils/api_client.py` (mesma convenção de `STATUS_LABELS`).

## Non-Goals

- Migração de dados — os defaults (`status = "ativo"`, `semester = ""`,
  `priority = "Media"`) já são aplicados pelo Xano para registros existentes
  e novos.
- Ordenação automática/drag-and-drop por prioridade.
- Notificações, automações ou regras de negócio adicionais.
- Alterações no backend Xano (já concluídas em `evolucao-disciplinas-tarefas`).
