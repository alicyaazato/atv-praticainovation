// Atualiza uma tarefa do usuario (titulo, descricao, prazo, status, disciplina)
// Tambem usado para marcar como concluida (status = "concluida")
query "tasks/{id}" verb=PATCH {
  api_group = "Tasks"
  auth = "user"

  input {
    int id
    text title?
    text description?
    text data?
    text status?
    int subject_id?
    text priority?
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.get academic_task {
      field_name = "id"
      field_value = $input.id
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
    } as $academic_task1
  
    precondition ($academic_task1 != null) {
      error_type = "notfound"
      error = "Tarefa nao encontrada"
    }
  
    precondition ($academic_task1.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: voce nao e o dono desta tarefa"
    }
  
    // Resolve cada campo: usa o valor enviado ou mantem o atual
    var $final_title {
      value = $academic_task1.title
    }
  
    conditional {
      if ($input.title != null) {
        var.update $final_title {
          value = $input.title
        }
      }
    }
  
    var $final_desc {
      value = $academic_task1.description
    }
  
    conditional {
      if ($input.description != null) {
        var.update $final_desc {
          value = $input.description
        }
      }
    }
  
    var $final_due {
      value = $academic_task1.data
    }
  
    conditional {
      if ($input.data != null) {
        var.update $final_due {
          value = $input.data
        }
      }
    }
  
    var $final_status {
      value = $academic_task1.status
    }
  
    conditional {
      if ($input.status != null) {
        var.update $final_status {
          value = $input.status
        }
      }
    }
  
    var $final_subject {
      value = $academic_task1.subject_id
    }
  
    conditional {
      if ($input.subject_id != null) {
        var.update $final_subject {
          value = $input.subject_id
        }
      }
    }
  
    var $final_priority {
      value = $academic_task1.priority
    }
  
    conditional {
      if ($input.priority != null) {
        var.update $final_priority {
          value = $input.priority
        }
      }
    }
  
    db.edit academic_task {
      field_name = "id"
      field_value = $input.id
      data = {
        user_id    : $auth.id
        subject_id : $final_subject
        title      : $final_title
        description: $final_desc
        status     : $final_status
        data       : $final_due
        priority   : $final_priority
      }
    } as $academic_task
  }

  response = {data: $academic_task}
}