// Request a one-time magic link to reset password
query "reset/request-reset-link" verb=GET {
  api_group = "Authentication"

  input {
    email email?
  }

  stack {
    // Generate a one-time magic link
    function.run "Getting Started Template/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email
  
    // Check that the link exists
    precondition ($token_and_email != null) {
      error = "Magic link could not be created. Try again."
    }
  
    // URL pública do app Streamlit (EduTrack AI). Atualize aqui se o app
    // mudar de endereço (ex: deploy no Streamlit Community Cloud).
    var $app_base_url {
      value = "http://179.110.58.64:8765"
    }
  
    // Create magic link (abre direto na página de Perfil, que lê
    // magic_token/email da query string para logar e trocar a senha)
    var $magic_link {
      value = $app_base_url ~ "/?magic_token=" ~ $token_and_email.token ~ "&email=" ~ $token_and_email.email
    }
  
    // Create HTML message to include magic reset password link
    util.template_engine {
      value = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2>Password Reset Request</h2>
            <p>Hello,</p>
            <p>We received a request to reset your password. To proceed, please click the link below:</p>
            <p style="text-align: center; margin: 30px 0;">
              <a href="{{ $var.magic_link }}" style="display: inline-block; padding: 12px 25px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 4px; font-size: 16px;">
                Reset Your Password
              </a>
            </p>
            <p>If you did not request a password reset, please ignore this email.</p>
            <p>Thank you.</p>
          </div>
        </body>
        </html>
        """
    } as $message
  
    // Send Email Function will ONLY send to the instance owner email with the free credits. Provide your own Resend API key and account for additional capability.
  
    // Send email with password reset link
    util.send_email {
      service_provider = "xano"
      subject = "Your password reset request"
      message = $message
    } as $send_email
  }

  response = {
    message: {}|set:"success":true|set:"message":"magic link sent"
  }

  tags = ["xano:quick-start"]
}