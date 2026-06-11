// Atualiza uma tarefa do usuario (titulo, descricao, prazo, status, disciplina)
// Tambem usado para marcar como concluida (status = "concluida")
query "tasks/{id}" verb=PATCH {
  api_group = "Tasks"
  auth = "user"

  input {
    int id
    text title?
    text description?
    text due_date?
    text status?
    int subject_id?
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.get "" {
      field_name = "id"
      field_value = $input.id
    } as $task
  
    precondition ($task != null) {
      error_type = "notfound"
      error = "Tarefa nao encontrada"
    }
  
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: voce nao e o dono desta tarefa"
    }
  
    // Resolve cada campo: usa o valor enviado ou mantem o atual
    var $final_title {
      value = $task.title
    }
  
    conditional {
      if ($input.title != null) {
        var.update $final_title {
          value = $input.title
        }
      }
    }
  
    var $final_desc {
      value = $task.description
    }
  
    conditional {
      if ($input.description != null) {
        var.update $final_desc {
          value = $input.description
        }
      }
    }
  
    var $final_due {
      value = $task.due_date
    }
  
    conditional {
      if ($input.due_date != null) {
        var.update $final_due {
          value = $input.due_date
        }
      }
    }
  
    var $final_status {
      value = $task.status
    }
  
    conditional {
      if ($input.status != null) {
        var.update $final_status {
          value = $input.status
        }
      }
    }
  
    var $final_subject {
      value = $task.subject_id
    }
  
    conditional {
      if ($input.subject_id != null) {
        var.update $final_subject {
          value = $input.subject_id
        }
      }
    }
  
    db.edit "" {
      field_name = "id"
      field_value = $input.id
      data = {
        title      : $final_title
        description: $final_desc
        due_date   : $final_due
        status     : $final_status
        subject_id : $final_subject
      }
    } as $updated
  }

  response = {data: $updated}
}