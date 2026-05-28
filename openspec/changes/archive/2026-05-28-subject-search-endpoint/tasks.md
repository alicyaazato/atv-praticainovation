## 1. Função Python — Detecção de Tarefas Atrasadas

- [x] 1.1 Criar arquivo `atv2Lab/functions/filter_overdue_subjects.xs` com a função Python `filter_overdue_subjects`
- [x] 1.2 Implementar a lógica: receber `subject_ids` (lista de int) e `user_id` (int), consultar `academic_task` onde `due_date IS NOT NULL AND due_date < now AND status != "completed" AND subject_id IN subject_ids AND user_id = user_id`
- [x] 1.3 Retornar lista de `subject_id` únicos que satisfazem os critérios
- [x] 1.4 Tratar caso de `subject_ids` vazio retornando lista vazia sem erro
- [x] 1.5 Adicionar try/except para evitar erro 500 em caso de falha isolada

## 2. Endpoint Xano — GET /subjects/search

- [x] 2.1 Criar arquivo `atv2Lab/apis/subjects/<id>_subjects_search_GET.xs` com `auth = "user"` e `api_group = "Subjects"`
- [x] 2.2 Definir inputs: `q` (text, opcional), `has_overdue_tasks` (boolean, opcional), `limit` (number, default 20, min 1, max 100), `offset` (number, default 0)
- [x] 2.3 Adicionar `precondition` que exige pelo menos um de `q` ou `has_overdue_tasks = true` (HTTP 400 caso contrário)
- [x] 2.4 Implementar busca por nome: se `q` fornecido, query em `subject` com filtro `name ILIKE "%q%"`, `owner_id = $auth.user_id` e `is_active = true`
- [x] 2.5 Implementar busca por tarefas atrasadas: se `has_overdue_tasks = true`, buscar todos os `subject_id` ativos do usuário e chamar `function.run "filter_overdue_subjects"` com os IDs
- [x] 2.6 Implementar OR lógico: unir os dois conjuntos de IDs, deduplicar, e buscar os subjects correspondentes
- [x] 2.7 Aplicar `limit` e `offset` na query final e retornar `items` e `count`
- [x] 2.8 Envolver chamada à função Python em try/catch no stack; em caso de falha, retornar apenas o resultado da busca por nome sem erro

## 3. Testes de Integração

- [x] 3.1 Verificar que `GET /subjects/search?q=<texto>` retorna apenas subjects do usuário autenticado que batem no nome
- [x] 3.2 Verificar que `GET /subjects/search?has_overdue_tasks=true` retorna subjects com pelo menos uma tarefa atrasada
- [x] 3.3 Verificar que a combinação `q + has_overdue_tasks=true` retorna a união dos resultados sem duplicatas
- [x] 3.4 Verificar que `GET /subjects/search` sem parâmetros retorna HTTP 400
- [x] 3.5 Verificar que subjects de outro usuário não aparecem nos resultados
- [x] 3.6 Verificar que tasks sem `due_date` não contam como atrasadas
- [x] 3.7 Verificar que subjects com `is_active = false` não aparecem nos resultados

## 4. Frontend Streamlit — Painel de Busca

- [x] 4.1 Adicionar nova tab "🔍 Buscar" na página `pages/1_📚_Disciplinas.py`
- [x] 4.2 Implementar campo de texto para busca por nome e checkbox "Mostrar disciplinas com tarefas atrasadas"
- [x] 4.3 Implementar função `search_subjects(q, has_overdue_tasks)` que chama `GET /subjects/search` com o token de auth
- [x] 4.4 Exibir resultados em cards com nome, código e indicador visual de atraso (se `has_overdue_tasks=true` foi usado)
- [x] 4.5 Exibir mensagem informativa quando nenhum resultado for encontrado
