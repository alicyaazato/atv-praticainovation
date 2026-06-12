# agent-estrutura.md

Especificações de estrutura e UX do Edutrack-ai.
Alimentado incrementalmente conforme novas regras/hábitos forem definidos.

## Navegação (Sidebar)

### Usuário não autenticado
- A sidebar exibe apenas duas opções: Login e Registro.
- Nenhuma página do sistema (Dashboard, Disciplinas, Tarefas, Perfil) fica
  acessível antes da autenticação.

### Usuário autenticado
- Após login/registro, a sidebar libera a navegação entre:
  Dashboard, Disciplinas, Tarefas, Perfil.
- Botão de Logout sempre visível na sidebar quando autenticado.

## Princípios de Design
- Estrutura minimalista: priorizar simplicidade e fácil intuição.
- Evitar duplicação de navegação (não usar o multipage automático do
  Streamlit junto com a navegação customizada — usar pasta `views/`).

## Módulo: Disciplinas (Subjects)

- API: grupo "Subject CRUD" (`SUBJECT_API_URL`).
- Campos do domínio: `name`, `professor`, `cargahoraria`.
- Estrutura da página (`views/disciplinas_page.py`): 3 abas —
  "📋 Minhas Disciplinas", "➕ Nova Disciplina", "🔍 Buscar".
- Validação de duplicata (mesmo nome + professor) antes de criar/editar.
- Sem aba de "tarefas em atraso" — removida por não fazer sentido ao projeto.

## Módulo: Dashboard

- API: grupo "Dashboard" (`DASHBOARD_API_URL`, `api:5sx9vVEG`).
- Endpoints: `GET /Diciplinas-dashboard` (disciplinas com `status`:
  rascunho/ativo/arquivado) e `GET /Tarefas-dashboard` (tarefas com
  `subject_name`).
- Métricas exibidas:
  - **Disciplinas Ativas**: disciplinas com `status == "ativo"`.
  - **Tarefas Pendentes**: tarefas com `status_tarefa != "completa"`.
  - **Progresso Geral**: média da taxa de conclusão de tarefas por
    disciplina (cada disciplina tem peso igual). Ex: 3 disciplinas com 1
    tarefa cada, sendo 1 completa => (100% + 0% + 0%) / 3 = 33%.
- Seções da página:
  - "Tarefas por Status": contagem por status (`STATUS_LABELS`,
    centralizado em `utils/api_client.py`).
  - "Progresso por Disciplina": barra de progresso por disciplina.
  - "Próximas Tarefas": as 5 tarefas pendentes mais próximas, ordenadas
    por data.

## Módulo: Tarefas (Academic Tasks)

- API: grupo "Academic Tasks" (`TASK_API_URL`, `api:Zb1x7tiT`).
- Campos do domínio: `subject_id`, `title`, `description`, `data`, `status_tarefa`
  (`pendente` | `em_progresso` | `completa`).
- Estrutura da página (`views/tarefas_page.py`): 3 abas —
  "📋 Minhas Tarefas", "➕ Nova Tarefa", "🔍 Buscar".
- Regra de negócio: um usuário pode ter N tarefas por disciplina, e N
  disciplinas (relação N:N entre tarefas e disciplinas).
- A lista de tarefas (`get_tasks`) é deduplicada por `id`, pois o `list-all`
  da API pode retornar a mesma tarefa repetida (join com disciplinas/matrículas).

## Padrões de Implementação (Streamlit)

- **Confirmação de exclusão**: usar `st.session_state` (`*_confirm_delete_id`)
  para persistir o estado de "confirmar exclusão" entre reruns — botões
  aninhados dentro de `if st.button(...)` não sobrevivem ao próximo rerun.
- **Modo de edição**: usar `st.session_state` (`*_edit_mode_id`) para abrir o
  formulário de edição inline, abaixo do card do item.
- **Cache**: toda função de listagem usa `@st.cache_data`; toda função de
  criar/editar/excluir chama `st.cache_data.clear()` ao final.
- **Chaves de widgets**: prefixar com o nome do domínio (`task_`, `edit_`,
  `delete_`, etc.) para evitar colisão de `key` entre páginas/abas.

## Estrutura de Pastas

- `views/`: páginas autenticadas (Dashboard, Disciplinas, Tarefas, Perfil).
- `utils/api_client.py`: única camada de acesso à API Xano (constantes
  `*_API_URL` por grupo de API + funções CRUD por domínio).
- Raiz do projeto mantida limpa: sem `__pycache__`, arquivos `.tmp`, ou docs
  duplicados — `.gitignore` cobre `__pycache__/` e `*.pyc`.
