// Atualiza os dados de uma disciplina do usuario autenticado
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
    text name?
    text professor?
    decimal carga_horaria?
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Disciplina nao encontrada"
    }
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: voce nao e o dono desta disciplina"
    }
  
    // Resolve cada campo: usa o valor enviado ou mantem o atual
    var $final_name {
      value = $subject.name
    }
  
    conditional {
      if ($input.name != null) {
        var.update $final_name {
          value = $input.name
        }
      }
    }
  
    var $final_professor {
      value = $subject.professor
    }
  
    conditional {
      if ($input.professor != null) {
        var.update $final_professor {
          value = $input.professor
        }
      }
    }
  
    var $final_ch {
      value = $subject.CargaHoraria
    }
  
    conditional {
      if ($input.carga_horaria != null) {
        var.update $final_ch {
          value = $input.carga_horaria
        }
      }
    }
  
    db.edit subject {
      field_name = "id"
      field_value = $input.id
      data = {
        name        : $final_name
        professor   : $final_professor
        CargaHoraria: $final_ch
      }
    } as $updated
  }

  response = {data: $updated}
}