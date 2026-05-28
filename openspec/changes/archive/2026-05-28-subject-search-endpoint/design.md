## Context

O projeto já tem: tabela `subject` (com `owner_id`, `name`, `is_active`), tabela `academic_task` (com `subject_id`, `due_date`, `status`, `user_id`) e os endpoints CRUD de subjects. O Xano suporta funções Python nativas, que podem executar lógica arbitrária dentro do stack de uma API. A busca por nome pode ser feita via `db.query` com filtro `ILIKE`, mas a detecção de tarefas atrasadas exige cruzar as duas tabelas — o que se beneficia de uma função Python para manter o endpoint legível e reutilizável.

## Goals / Non-Goals

**Goals:**
- Endpoint `GET /subjects/search` protegido por `auth = "user"` que aceita `q` (texto) e/ou `has_overdue_tasks` (booleano)
- Função Python `filter_overdue_subjects(subject_ids, user_id)` que retorna os IDs com tarefas vencidas
- OR lógico: se ambos os filtros forem fornecidos, retorna a união dos resultados
- Paginação via `limit` / `offset`
- UI Streamlit com campo de busca e checkbox

**Non-Goals:**
- Busca full-text em outros campos (descrição, código)
- Ordenação customizável pelo cliente
- Compartilhar disciplinas entre usuários (sem acesso cruzado)

## Decisions

**1 — Python para detecção de atraso, não JOIN no Xano**

O Xano não suporta JOINs arbitrários em `db.query`. A alternativa seria fazer dois queries separados e unir em JS dentro do stack, mas isso dispersa a lógica. Usar uma função Python centraliza a regra de negócio "tarefa atrasada = `due_date < agora AND status != completed`" em um lugar versionável e testável.

_Alternativa descartada_: filtrar no frontend — expõe dados desnecessários e não escala.

**2 — OR lógico entre os dois filtros**

Se o usuário informa `q=calc` e `has_overdue_tasks=true`, o endpoint retorna disciplinas cujo nome contém "calc" **ou** que têm tarefas atrasadas. Isso maximiza os resultados úteis sem exigir duas chamadas separadas.

_Alternativa descartada_: AND lógico — restritivo demais, dificultaria descoberta de disciplinas com atraso que não batem no texto buscado.

**3 — Reuso do grupo de API `subjects` existente**

O novo endpoint entra no mesmo `api_group = "Subjects"` e segue o mesmo padrão de segurança (`auth = "user"` + `owner_id == $auth.user_id`). Não cria um novo grupo.

**4 — Função Python recebe `subject_ids` + `user_id` como entrada**

A função não faz query de subjects — recebe os IDs já filtrados pelo Xano e só verifica a tabela `academic_task`. Isso evita acesso indevido a tarefas de outros usuários.

## Risks / Trade-offs

- **Performance com muitas disciplinas**: A função Python itera sobre IDs de subjects. Se um usuário tiver centenas de subjects, o array pode crescer. → Mitigação: aplicar `limit` no query de subjects antes de passar os IDs para a função Python.
- **Falso positivo de atraso**: Se `due_date` for `null` (tarefa sem prazo), não deve ser considerada atrasada. → Mitigação: a função Python filtra `due_date IS NOT NULL` antes de comparar com `now`.
- **Função Python pode falhar silenciosamente**: Xano trata exceções Python como erro 500. → Mitigação: envolver a chamada em bloco try/catch no stack e retornar lista vazia em caso de falha, sem derrubar o endpoint.
- **Duplicatas no resultado OR**: Uma disciplina pode aparecer tanto na busca por nome quanto na de tarefas atrasadas. → Mitigação: deduplicar por `id` antes de retornar.

## Migration Plan

1. Criar a função Python `filter_overdue_subjects` em `atv2Lab/functions/`
2. Criar o endpoint `.xs` em `atv2Lab/apis/subjects/`
3. Atualizar a página Streamlit
4. Sem alterações em tabelas ou dados existentes — rollback é simplesmente remover os novos arquivos

## Open Questions

- O campo `due_date` na tabela `academic_task` é timestamp ou date? Impacta a comparação com `now` na função Python. _(Verificar `tables/753428_academic_task.xs` na implementação.)_
