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
    } as $lista_de_tarefas
  }

  response = {items: $lista_de_tarefas}
}