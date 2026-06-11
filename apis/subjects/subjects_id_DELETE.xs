// Exclui uma disciplina do usuario autenticado
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
  }

  stack {
<<<<<<<
    precondition ($auth.id) {
=======
    precondition ($auth.id != null) {
>>>>>>>
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
  
    db.del subject {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    message: "Disciplina excluida com sucesso"
    data   : {id: $input.id}
  }
}