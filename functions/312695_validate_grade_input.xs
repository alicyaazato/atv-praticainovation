// Função reutilizável para validar os inputs de criação/atualização de uma nota de atividade.
function validate_grade_input {
  input {
    // We receive all potential inputs and check for presence and validity.
    // Making them nullable to handle missing field checks.
    // A nota a ser validada.
    decimal? grade
  
    // ID do professor que está lançando a nota.
    int? professor_id
  
    // ID do aluno que está recebendo a nota.
    int? student_id
  
    // ID da conta.
    int? account_id
  
    // ID da atividade.
    int? activity_id
  }

  stack {
    // Initialize the response structure
    var $validation_result {
      value = {is_valid: true, errors: []}
    }
  
    // 1. Check for required fields for creation
    conditional {
      if ($input.account_id == null || $input.activity_id == null || $input.student_id == null || $input.professor_id == null || $input.grade == null) {
        var.update $validation_result.is_valid {
          value = false
        }
      
        array.push $validation_result.errors {
          value = {
            code   : "REQUIRED_FIELDS_MISSING"
            message: "Campos obrigatórios (account_id, activity_id, student_id, professor_id, grade) estão faltando."
          }
        }
      }
    }
  
    // 2. Validate grade range (only if grade is not null to avoid cascading errors)
    conditional {
      if ($input.grade != null && ($input.grade < 0 || $input.grade > 10)) {
        var.update $validation_result.is_valid {
          value = false
        }
      
        array.push $validation_result.errors {
          value = {
            code   : "INVALID_GRADE_VALUE"
            message: "A nota deve estar entre 0.0 e 10.0."
          }
        }
      }
    }
  
    // 3. Validate professor_id is not the same as student_id
    conditional {
      if ($input.professor_id != null && $input.student_id != null && $input.professor_id == $input.student_id) {
        var.update $validation_result.is_valid {
          value = false
        }
      
        array.push $validation_result.errors {
          value = {
            code   : "INVALID_SELF_GRADE"
            message: "O professor não pode lançar uma nota para si mesmo."
          }
        }
      }
    }
  }

  response = $validation_result
}