// Cadastra uma nova disciplina para o usuario autenticado
// Impede duplicatas: mesmo name + professor para o mesmo usuario
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text professor filters=trim
    decimal carga_horaria
  }

  stack {
    precondition ($auth.id) {
      error_type = "accessdenied"
      error = "Autenticacao necessaria"
    }
  
    precondition ($input.carga_horaria > 0) {
      error_type = "inputerror"
      error = "Carga horaria deve ser maior que zero"
    }
  
    // Verifica duplicata: mesmo nome + professor para este usuario
    db.query subject {
      where = $db.subject.user_id == $auth.id && $db.subject.name == $input.name && $db.subject.professor == $input.professor
      return = {type: "count"}
    } as $dup_count
  
    precondition ($dup_count == 0) {
      error_type = "inputerror"
      error = "Ja existe uma disciplina com esse nome e professor"
    }
  
    db.add subject {
      data = {
        created_at  : "now"
        name        : $input.name
        professor   : $input.professor
        CargaHoraria: $input.carga_horaria
        user_id     : $auth.id
      }
    } as $new_subject
  }

  response = {data: $new_subject}
}