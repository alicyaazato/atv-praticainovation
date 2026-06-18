// Confirma o código de redefinição de senha e atualiza a senha em uma única
// chamada. Não requer autenticação nem emite token: o código enviado por
// e-mail já é a prova de identidade.
query "reset/confirm-code" verb=POST {
  api_group = "Authentication"

  input {
    text email? filters=trim
    text code? filters=trim
    text password? filters=trim|min:8
    text confirm_password? filters=trim
  }

  stack {
    // Check to make sure the email exists
    precondition ($input.email != null) {
      error = "email is required but not provided"
    }

    // Check to make sure the code exists
    precondition ($input.code != null) {
      error = "code is required but was not provided."
    }

    // Check that the password inputs are matching
    precondition ($input.password == $input.confirm_password) {
      error = "As senhas não coincidem."
    }

    // Get the user record with the email informado
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = [
        "id"
        "account_id"
        "password_reset.token"
        "password_reset.expiration"
        "password_reset.used"
      ]
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "Usuário não encontrado."
    }

    // Valida se o código fornecido coincide com o salvo no banco (comparação direta de texto)
    var $verify_token {
      value = $input.code == $user.password_reset.token
    }

    // Verifica se a validação do código é verdadeira
    precondition ($verify_token) {
      error_type = "unauthorized"
      error = "O código informado está incorreto."
    }

    // Check that the password reset code has not expired
    precondition ($user.password_reset.expiration > now) {
      error = "Este código expirou. Solicite um novo."
    }

    // Check to make sure the password reset code has not been used
    precondition ($user.password_reset.used == false) {
      error = "Este código já foi utilizado. Solicite um novo."
    }

    // Atualiza a senha e marca o código como usado, em uma única gravação
    db.edit user {
      field_name = "id"
      field_value = $user.id
      enforce_hidden_fields = false
      data = {
        password: $input.password
        password_reset: {
          token     : $user.password_reset.token
          expiration: $user.password_reset.expiration
          used      : true
        }
      }
    } as $user1

    // Create an event log for password reset via code
    function.run "Getting Started Template/create_event_log" {
      input = {
        user_id   : $user.id
        account_id: $user.account_id
        action    : "reset_password_via_code"
        metadata  : $user1
      }
    } as $event_log
  }

  response = {}
    |set:"success":true
    |set:"message":"Senha atualizada com sucesso."
  tags = ["xano:quick-start"]
}
