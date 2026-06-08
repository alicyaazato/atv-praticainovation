// Busca disciplinas por nome (q), case-insensitive.
// has_overdue_tasks fica reservado para quando houver modulo de tarefas.
query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text q?
    bool has_overdue_tasks?
  }

  stack {
<<<<<<<
    precondition ($auth.id) {
=======
    precondition ($auth.id != null) {
>>>>>>>
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    precondition ($input.q != null) {
      error_type = "inputerror"
      error = "Informe o parametro 'q' para buscar por nome"
    }
  
    db.query subject {
<<<<<<<
      where = $db.subject.user_id == $auth.id && $db.subject.name includes $input.q
=======
      where = $auth.id == $db.subject.user_id && $db.subject.name includes $input.q
>>>>>>>
      return = {type: "list", paging: {page: 1, per_page: 100}}
      output = [
        "itemsReceived"
        "curPage"
        "nextPage"
        "prevPage"
        "offset"
        "perPage"
        "items.id"
        "items.name"
        "items.professor"
        "items.CargaHoraria"
        "items.user_id"
      ]
    } as $results
  }

  response = {items: $results.items}
}