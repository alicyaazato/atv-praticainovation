// Exclui uma tarefa do usuario autenticado
query "tasks/{id}" verb=DELETE {
  api_group = "Tasks"
  auth = "user"

  input {
    int id
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.get academic_task {
      field_name = "id"
      field_value = $input.id
    } as $academic_task1
  
    precondition ($academic_task1 != null) {
      error_type = "notfound"
      error = "Tarefa nao encontrada"
    }
  
    precondition ($academic_task1.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: voce nao e o dono desta tarefa"
    }
  
    db.del academic_task {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {message: "Tarefa excluida com sucesso", data: ``}
}