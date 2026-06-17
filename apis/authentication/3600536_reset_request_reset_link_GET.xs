// Request a one-time magic link to reset password
query "reset/request-reset-link" verb=POST {
  api_group = "Authentication"

  input {
    // O e-mail do usuário que deseja resetar a senha
    email email?
  }

  stack {
    // Gera um token único e salva no registro do usuário
    function.run "Getting Started Template/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email
  
    // Verifica se o token foi gerado com sucesso
    precondition ($token_and_email != null) {
      error = "Não foi possível criar o link de reset. Tente novamente."
    }
  
    // URL base do aplicativo (EduTrack AI)
    var $app_base_url {
      value = $env.FRONTEND_URL
    }
  
    // Cria o link mágico para o reset
    var $magic_link {
      value = ($app_base_url) ~ "/?magic_token=" ~ ($token_and_email.token) ~ "&email=" ~ ($token_and_email.email)
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
            .button-container { 
              text-align: center; 
              margin: 30px 0; 
            }
            .button { 
              background-color: #09090b; 
              color: #ffffff; 
              padding: 12px 24px; 
              text-decoration: none; 
              border-radius: 6px; 
              font-weight: 500; 
              display: inline-block; 
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
                <span class="email-highlight">{{ $var.token_and_email.email|e('html') }}</span>
              </p>
              <p>Se você fez esta solicitação, clique no botão abaixo para criar uma nova senha e recuperar seu acesso:</p>
              <div class="button-container">
                <a href="{{ $var.magic_link|e('html_attr') }}" class="button">Redefinir Minha Senha</a>
              </div>
              <p>Se você não solicitou a redefinição de senha, pode ignorar este e-mail com segurança. Nenhuma alteração será feita na sua conta.</p>
            </div>
            <div class="footer">
              <p>Problemas com o botão? Copie e cole o link abaixo no seu navegador:</p>
              <p style="word-break: break-all; color: #52525b;">{{ $var.magic_link|e('html') }}</p>
            </div>
          </div>
        </body>
        </html>
        """
    } as $message
  
    // Envia o e-mail via Resend (plano gratuito: 3.000/mês, 100/dia).
    // Variáveis de ambiente necessárias no Xano:
    //   RESEND_API_KEY → chave gerada em resend.com/api-keys
    //   FRONTEND_URL   → https://atv-praticainovation-kdmdubdbe3nrdurbbasjiu.streamlit.app
    util.send_email {
      service_provider = "resend"
      api_key = $env.RESEND_API_KEY
      subject = "Recuperação de senha — EduTrack AI"
      message = $message
      to = $token_and_email.email
      from = "onboarding@resend.dev"
    } as $send_email
  }

  response = {
    success: true
    message: "E-mail de recuperação enviado com sucesso."
  }

  tags = ["xano:quick-start"]
}