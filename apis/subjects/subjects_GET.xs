// Lista todas as disciplinas do usuario autenticado
query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.query subject {
      where = $db.subject.user_id == $auth.id
      sort = {created_at: "desc"}
      return = {type: "list", paging: {page: 1, per_page: 100}}
    } as $subjects
  }

  response = {items: $subjects.items}
}