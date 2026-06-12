// Cadastra uma tarefa vinculada a uma disciplina do usuario autenticado
query tasks verb=POST {
  api_group = "Tasks"
  auth = "user"

  input {
    text title filters=trim
    text description?
    int subject_id
    enum status?=Pendente {
      values = ["Pendente", "Em_progresso", "Completa", "Atrasada"]
    }
  
    text data filters=trim
    enum priority?=Media {
      values = ["Baixa", "Media", "Alta"]
    }
  }

  stack {
    precondition ($auth.id != null) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    // Garante que a disciplina existe e pertence ao usuario
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    !precondition ()
    db.add academic_task {
      data = {
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        status     : $input.status
        data       : $input.data
        priority   : $input.priority
      }
    
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
    } as $adcionar_tarefa
  }

  response = {item: $adcionar_tarefa}
}