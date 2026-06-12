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