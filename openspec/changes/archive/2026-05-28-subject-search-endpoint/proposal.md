## Why

O sistema possui listagem de disciplinas por dono, mas não oferece busca textual nem visibilidade sobre disciplinas com tarefas atrasadas. Sem essa capacidade, o aluno precisa percorrer toda a lista para encontrar uma disciplina específica ou identificar quais têm pendências vencidas.

## What Changes

- Novo endpoint `GET /subjects/search` com suporte a filtro por `name` (busca parcial, case-insensitive) e/ou flag `has_overdue_tasks` (booleano)
- Nova função Python no Xano (`filter_overdue_subjects`) que recebe uma lista de `subject_id` e retorna apenas os que possuem tarefas com `due_date < now` e `status != "completed"`
- Os dois filtros podem ser usados de forma independente ou combinada (OR lógico: retorna disciplinas que batem no nome **ou** que têm tarefas atrasadas)
- Atualização da página Streamlit de Disciplinas com campo de busca e toggle "Mostrar com tarefas atrasadas"

## Capabilities

### New Capabilities
- `subject-search`: Endpoint de busca de disciplinas com filtro por nome e/ou tarefas atrasadas, integrando lógica Python para detecção de atraso

### Modified Capabilities
- `subjects-crud`: Adiciona o novo endpoint `GET /subjects/search` ao grupo de API existente (sem breaking changes nos endpoints atuais)

## Impact

- **Backend (Xano)**: novo arquivo `.xs` em `atv2Lab/apis/subjects/` e nova função Python em `atv2Lab/functions/`
- **Tabelas dependentes**: `subject` e `academic_task` (já existentes)
- **Frontend**: `pages/1_📚_Disciplinas.py` — novo painel de busca
- **Segurança**: mesmo padrão dos endpoints existentes — `auth = "user"` + `owner_id == $auth.user_id`
- **Sem breaking changes**: endpoints existentes (`/subjects/my`, `/subjects/{id}`, etc.) não são alterados
