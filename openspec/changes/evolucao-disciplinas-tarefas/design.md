# Evolução das Disciplinas e Tarefas - Design

## Data Model

### Table: subject (`tables/809944_subject.xs`)

Campos novos:

```
- status: string (enum) - "rascunho" | "ativo" | "arquivado", default "ativo"
- semester: string (opcional) - período/semestre em texto livre, ex: "2026/1"
```

Campos atuais (sem alteração): `id`, `created_at`, `name?`, `professor?`,
`CargaHoraria?`, `user_id?`.

### Table: academic_task (`tables/842368_academic_task.xs`)

Campo novo:

```
- priority: string (enum) - "Baixa" | "Média" | "Alta", default "Média"
```

**Implementado** com valores internos sem acento (`Baixa` | `Media` | `Alta`,
default `Media`), seguindo o padrão já usado em `status`
(`Em_progresso` é a chave interna; "Em progresso" é o rótulo exibido em
`STATUS_LABELS`). O mapeamento `priority -> rótulo acentuado` (ex.: um futuro
`PRIORITY_LABELS`) fica para a proposta de front-end.

Campo existente a conciliar:

```
- status: string (enum) - hoje documentado como
    "pending" | "in_progress" | "completed" | "overdue" (default "pending")
  mas o front-end (utils/api_client.STATUS_LABELS) usa
    "Pendente" | "Em_progresso" | "Completa" | "Atrasada"
```

## Conciliação do enum `status` (academic_task)

Antes de qualquer mudança em `priority` ou em filtros novos:

1. Consultar registros existentes na tabela `academic_task` no Xano e
   verificar quais valores de `status` estão realmente gravados.
2. Caso os dados gravados usem as chaves em português (cenário mais
   provável, já que o front funciona hoje), atualizar
   `tables/842368_academic_task.xs` para refletir o enum real
   (`Pendente`, `Em_progresso`, `Completa`, `Atrasada`, default `Pendente`).
3. Caso existam registros com os dois conjuntos de valores (dados
   legados), planejar uma migração de normalização antes de habilitar
   filtros que dependam de `status`.
4. `utils/api_client.STATUS_LABELS` é a fonte única do lado do front e não
   deve mudar sem uma migração coordenada no Xano.

## API Endpoints a atualizar

### `apis/subjects/subjects_POST.xs`
- Aceitar `status` (default `"ativo"` se omitido) e `semester` (opcional).
- Validar `status` contra o enum `rascunho | ativo | arquivado`.

### `apis/subjects/subjects_id_PATCH.xs` (ou equivalente de update)
- Aceitar `status` e `semester` como campos parciais.
- Permitir transição para `arquivado` (usada pela UI para "arquivar
  disciplina").

### `apis/tasks/tasks_POST.xs`
- Aceitar `priority` (default `"Média"` se omitido).
- Validar contra o enum `Baixa | Média | Alta`.

### `apis/tasks/tasks_id_PATCH.xs` (ou equivalente de update)
- Aceitar `priority` como campo parcial.

## Redefinição de senha

**Superado**: a abordagem original de magic link (e-mail com link clicável,
tratado via `st.query_params` em `pages/3_👤_Perfil.py`) foi substituída por
um fluxo de código de verificação de 6 dígitos digitado dentro do app, para
evitar o redirecionamento entre e-mail e app. Ver
`apis/authentication/3600536_reset_request_reset_link_GET.xs` (envia o
código por e-mail via `generate_reset_code`) e
`apis/authentication/3600537_reset_magic_link_login_POST.xs` (endpoint
`reset/verify-code`, troca o código por um auth token).

## Segurança: endpoint público `edutrackAPI` (academic_task GET)

### `apis/edutrack_api/3914735_academic_task_GET.xs`

Estado atual — sem `auth`, sem filtro, retorna a lista crua de **todos os
usuários**:

```xanoscript
// Query all academic_task records
query academic_task verb=GET {
  api_group = "edutrackAPI"

  input {
  }

  stack {
    db.query academic_task {
      return = {type: "list"}
    } as $model
  }

  response = $model
}
```

**Implementado** — alinhado ao padrão já usado em `apis/tasks/tasks_GET.xs`
(autenticação obrigatória + filtro por `user_id` + resposta em `{items: ...}`,
incluindo o novo campo `priority`):

```xanoscript
// Query academic_task records do usuario autenticado
query academic_task verb=GET {
  api_group = "edutrackAPI"
  auth = "user"

  input {
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }

    db.query academic_task {
      where = $db.academic_task.user_id == $auth.id
      return = {type: "list"}
      output = [
        "id"
        "created_at"
        "user_id"
        "subject_id"
        "title"
        "description"
        "status"
        "data"
        "priority"
      ]
    } as $model
  }

  response = {items: $model}
}
```

Como o front-end já cobre essa necessidade via `apis/tasks/tasks_GET.xs`
(`Tasks` group), este endpoint permanece sem uso direto pelo app — mas deixa
de expor dados de outros usuários.

## Integration Points

1. **Dashboard** (`app.py`): métrica "Disciplinas Ativas" poderá filtrar por
   `subject.status == "ativo"` após a migração.
2. **Disciplinas** (`pages/1_📚_Disciplinas.py`): UI de "arquivar disciplina"
   e exibição de `semester` podem ser adicionadas após os campos existirem.
3. **Tarefas** (`pages/2_📝_Tarefas.py`): seletor/exibição de `priority` pode
   ser adicionado ao formulário de criação/edição após o campo existir.
4. **Relatórios** (`pages/4_📈_Relatorios.py`): filtro por prioridade pode ser
   adicionado como melhoria futura.
