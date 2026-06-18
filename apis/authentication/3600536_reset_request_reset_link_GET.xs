// Request a one-time magic link to reset password
query "reset/request-reset-link" verb=POST {
  api_group = "Authentication"

  input {
    // O e-mail do usuário que deseja resetar a senha
    email email?
  }

  stack {
    // Gera um código de 6 dígitos e salva no registro do usuário
    function.run "Getting Started Template/generate_reset_code" {
      input = {email: $input.email}
    } as $code_and_email

    // Verifica se o código foi gerado com sucesso
    precondition ($code_and_email != null) {
      error = "Não foi possível gerar o código de redefinição. Tente novamente."
    }

    // Cria o corpo do e-mail em HTML
    util.template_engine {
      value = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Redefinição de Senha</title>
          <style>
            body { 
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
              background-color: #f4f4f5; 
              margin: 0; 
              padding: 0; 
              color: #18181b; 
            }
            .container { 
              max-width: 600px; 
              margin: 40px auto; 
              background: #ffffff; 
              border-radius: 8px; 
              padding: 40px; 
              box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); 
            }
            .header { 
              text-align: center; 
              margin-bottom: 30px; 
            }
            .title { 
              font-size: 24px; 
              font-weight: 600; 
              color: #09090b; 
              margin: 0; 
            }
            .content { 
              font-size: 16px; 
              line-height: 1.6; 
              color: #3f3f46; 
            }
            .email-highlight {
              display: inline-block;
              background: #f4f4f5;
              padding: 6px 12px;
              border-radius: 6px;
              font-weight: 600;
              color: #09090b;
              border: 1px solid #e4e4e7;
              letter-spacing: 0.5px;
            }
            .code-container {
              text-align: center;
              margin: 30px 0;
            }
            .code {
              display: inline-block;
              background-color: #09090b;
              color: #ffffff;
              padding: 16px 32px;
              border-radius: 8px;
              font-weight: 700;
              font-size: 32px;
              letter-spacing: 8px;
            }
            .footer {
              font-size: 14px; 
              color: #71717a; 
              text-align: center; 
              margin-top: 30px; 
              border-top: 1px solid #e4e4e7; 
              padding-top: 20px; 
            }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1 class="title">Redefinição de Senha</h1>
            </div>
            <div class="content">
              <p>Olá,</p>
              <p>Recebemos uma solicitação para redefinir a senha da conta associada ao e-mail abaixo:</p>
              <p style="text-align: center; margin: 24px 0;">
                <span class="email-highlight">{{ $var.code_and_email.email|e('html') }}</span>
              </p>
              <p>Use o código abaixo no app EduTrack AI para confirmar a redefinição e criar uma nova senha:</p>
              <div class="code-container">
                <span class="code">{{ $var.code_and_email.code|e('html') }}</span>
              </div>
              <p>Este código expira em 15 minutos. Se você não solicitou a redefinição de senha, pode ignorar este e-mail com segurança. Nenhuma alteração será feita na sua conta.</p>
            </div>
            <div class="footer">
              <p>Por segurança, nunca compartilhe este código com outras pessoas.</p>
            </div>
          </div>
        </body>
        </html>
        """
    } as $message
  
    // Envia o e-mail via Resend (plano gratuito: 3.000/mês, 100/dia).
    // Variável de ambiente necessária no Xano:
    //   RESEND_API_KEY → chave gerada em resend.com/api-keys
    util.send_email {
      api_key = $env.RESEND_API_KEY
      service_provider = "resend"
      subject = "Seu código de redefinição de senha — EduTrack AI"
      message = $message
      to = $code_and_email.email
      from = "onboarding@resend.dev"
    } as $send_email
  }

  response = {
    success: true
    message: "Código de redefinição enviado com sucesso."
  }

  tags = ["xano:quick-start"]
}