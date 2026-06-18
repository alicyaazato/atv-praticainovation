// This function generates a 6-digit numeric reset code with a 15 minute expiration date.
function "Getting Started Template/generate_reset_code" {
  input {
    email email?
  }

  stack {
    // Checks that the email input is not empty
    precondition ($input.email != null) {
      error = "email is required but was not suppiled. "
    }

    // Gets the user record by email
    db.query user {
      where = $db.user.email == $input.email
      return = {type: "single"}
    } as $user

    // Verifies that the user record exists
    precondition ($user != null) {
      error_type = "notfound"
      error = "No user found for that email."
    }

    // Gera um código numérico de 6 dígitos (ex.: 384921)
    security.random_number {
      min = 100000
      max = 999999
    } as $random_code

    var $token {
      value = $random_code|to_text
    }

    // Builds the password reset object
    var $password_reset {
      value = {}
        |set:"token":$token
        |set:"expiration":(now
          |add_secs_to_timestamp:(900|to_int)
        )
        |set:"used":false
    }

    // Updates the user record with the password reset object
    db.edit user {
      field_name = "id"
      field_value = $user|get:"id":0
      enforce_hidden_fields = false
      data = {password_reset: $password_reset}
    } as $updated_password_reset
  }

  response = {}
    |set:"code":$token
    |set:"email":$updated_password_reset.email
  tags = ["xano:quick-start"]
}