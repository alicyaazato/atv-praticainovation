// Lista todas as tarefas do usuario autenticado
query tasks verb=GET {
  api_group = "Tasks"
  auth = "user"

  input {
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.query "" {
      where = $db.task.user_id == $auth.id
      sort = {due_date: "asc"}
      return = {type: "list", paging: {page: 1, per_page: 200}}
    } as $tasks
  }

  response = {items: $tasks.items}
}