// Cadastra uma tarefa vinculada a uma disciplina do usuario autenticado
query tasks verb=POST {
  api_group = "Tasks"
  auth = "user"

  input {
    text title filters=trim
    text description?
    text due_date?
    int subject_id
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    // Garante que a disciplina existe e pertence ao usuario
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Disciplina nao encontrada"
    }
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Voce nao e o dono desta disciplina"
    }
  
    db.add "" {
      data = {
        created_at : "now"
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : "pendente"
        subject_id : $input.subject_id
        user_id    : $auth.id
      }
    } as $new_task
  }

  response = {data: $new_task}
}