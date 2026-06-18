// Verifica o código de redefinição de senha e troca por um auth token.
query "reset/verify-code" verb=POST {
  api_group = "Authentication"

  input {
    text code? filters=trim
    text email? filters=trim
  }

  stack {
    // Check to make sure the code exists
    precondition ($input.code != null) {
      error = "code is required but was not provided."
    }
  
    // Check to make sure the email exists
    precondition ($input.email != null) {
      error = "email is required but not provided"
    }
  
    // Get the user record with the email informado
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = [
        "id"
        "created_at"
        "name"
        "email"
        "account_id"
        "role"
        "password_reset.token"
        "password_reset.expiration"
        "password_reset.used"
      ]
    } as $user
  
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
  
    // Create an authentication token
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $auth_token
  
    // Update the user record that the password reset token has been used
    db.edit user {
      field_name = "id"
      field_value = $user.id
      enforce_hidden_fields = false
      data = {
        password_reset: {
        token     : $user.password_reset.token
        expiration: $user.password_reset.expiration
        used      : true
      }
      }
    } as $user1
  
    // Create an event log for password reset code verification
    function.run "Getting Started Template/create_event_log" {
      input = {
        user_id   : $user.id
        account_id: $user.account_id
        action    : "verify_password_reset_code"
        metadata  : $user1
      }
    } as $event_log
  }

  response = {authToken: $auth_token, user_id: $user1.id}
  tags = ["xano:quick-start"]
}