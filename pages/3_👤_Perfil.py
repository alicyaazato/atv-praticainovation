import os

import streamlit as st
import requests


def load_dotenv(dotenv_path=".env"):
    if os.path.exists(dotenv_path):
        with open(dotenv_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value

load_dotenv()

xano_url_login_singup = os.getenv("XANO_API_AUTH")
xano_url_edit = os.getenv("XANO_API_EDIT")

TOKEN_SESSAO = None



def _headers():
    return {
        "Authorization": f"Bearer {TOKEN_SESSAO}",
        "Content-Type": "application/json",
    }


def cadastrar_usuario(nome, email, senha):
    global TOKEN_SESSAO
    try:
        response = requests.post(f"{xano_url_login_singup}/auth/signup",
                                 json={"name": nome, "email": email, "password": senha})
        data = response.json()
        if response.status_code != 200:
            return {"numErro": 1, "mensagem": data.get("message", "Erro no cadastro")}
        TOKEN_SESSAO = data.get("authToken")
        return {"numErro": 0, "mensagem": "Usuário cadastrado com sucesso!"}
    except requests.exceptions.RequestException as e:
        return {"numErro": 1, "mensagem": f"Erro de conexão: {str(e)}"}


def login_usuario(email, senha):
    global TOKEN_SESSAO
    try:
        response = requests.post(f"{xano_url_login_singup}/auth/login",
                                 json={"email": email, "password": senha})
        data = response.json()
        if response.status_code != 200:
            return {"numErro": 1, "mensagem": data.get("message", "E-mail ou senha incorretos")}
        TOKEN_SESSAO = data.get("authToken")
        return {"numErro": 0, "mensagem": "Login realizado com sucesso!"}
    except requests.exceptions.RequestException as e:
        return {"numErro": 1, "mensagem": f"Erro de conexão: {str(e)}"}


def obter_perfil_objeto():
    if not TOKEN_SESSAO:
        return {"numErro": 1, "mensagem": "Usuário não autenticado."}
    try:
        response = requests.get(f"{xano_url_login_singup}/auth/me", headers=_headers())
        data = response.json()
        if response.status_code != 200:
            return {"numErro": 1, "mensagem": "Erro ao carregar dados do perfil"}
        return {"numErro": 0, "dados": data}
    except requests.exceptions.RequestException as e:
        return {"numErro": 1, "mensagem": f"Erro de conexão: {str(e)}"}


def editar_perfil(nome, email):
    """PATCH /user/edit_profile — atualiza nome e/ou e-mail do usuário autenticado."""
    try:
        response = requests.patch(
            f"{xano_url_edit}/user/edit_profile",
            json={"name": nome, "email": email},
            headers=_headers(),
            timeout=10,
        )
        data = response.json()
        if response.status_code != 200:
            return {"numErro": 1, "mensagem": data.get("message", f"Erro {response.status_code}")}
        return {"numErro": 0, "mensagem": "Perfil atualizado com sucesso!"}
    except requests.exceptions.RequestException as e:
        return {"numErro": 1, "mensagem": f"Erro de conexão: {str(e)}"}


def alterar_senha(nova_senha, confirmar_senha):
    """POST /reset/update_password — troca senha do usuário já autenticado."""
    try:
        response = requests.post(
            f"{xano_url_login_singup}/reset/update_password",
            json={"password": nova_senha, "confirm_password": confirmar_senha},
            headers=_headers(),
            timeout=10,
        )
        data = response.json()
        if response.status_code != 200:
            return {"numErro": 1, "mensagem": data.get("message", f"Erro {response.status_code}")}
        return {"numErro": 0, "mensagem": "Senha alterada com sucesso!"}
    except requests.exceptions.RequestException as e:
        return {"numErro": 1, "mensagem": f"Erro de conexão: {str(e)}"}


# ── Page ──────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Perfil", page_icon="👤")
st.title("👤 Perfil")

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

TOKEN_SESSAO = st.session_state["auth_token"]

# ── Autenticado ───────────────────────────────────────────────────────────────

if TOKEN_SESSAO:
    resultado = obter_perfil_objeto()

    if resultado["numErro"] != 0:
        st.error(resultado["mensagem"])
        st.session_state["auth_token"] = None
        st.rerun()

    dados = resultado["dados"]
    st.success(f"Bem-vindo, **{dados.get('name', '')}**!")
    st.divider()

    tab_perfil, tab_senha = st.tabs(["✏️ Meu Perfil", "🔒 Alterar Senha"])

    # ── Tab: visualizar / editar perfil ───────────────────────────────────────
    with tab_perfil:
        st.subheader("Dados da conta")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {dados.get('id', '—')}")
            st.write(f"**Função:** {dados.get('role', '—')}")

        st.divider()
        st.subheader("Editar informações")

        with st.form("form_editar_perfil"):
            novo_nome = st.text_input("Nome", value=dados.get("name", ""))
            novo_email = st.text_input("E-mail", value=dados.get("email", ""))
            salvar = st.form_submit_button("💾 Salvar alterações", use_container_width=True)

        if salvar:
            if not novo_nome or not novo_email:
                st.warning("Nome e e-mail são obrigatórios.")
            else:
                res = editar_perfil(novo_nome.strip(), novo_email.strip())
                if res["numErro"] == 0:
                    st.success(res["mensagem"])
                    st.rerun()
                else:
                    st.error(res["mensagem"])

    # ── Tab: alterar senha ────────────────────────────────────────────────────
    with tab_senha:
        st.subheader("Redefinir senha")
        st.caption("Você já está autenticado — basta informar a nova senha.")

        with st.form("form_alterar_senha"):
            nova_senha = st.text_input("Nova senha", type="password", placeholder="Mínimo 8 caracteres")
            conf_senha = st.text_input("Confirmar nova senha", type="password", placeholder="••••••••")
            alterar = st.form_submit_button("🔒 Alterar senha", use_container_width=True)

        if alterar:
            if not nova_senha or not conf_senha:
                st.warning("Preencha os dois campos de senha.")
            elif len(nova_senha) < 8:
                st.error("A senha deve ter no mínimo 8 caracteres.")
            elif nova_senha != conf_senha:
                st.error("As senhas não coincidem.")
            else:
                res = alterar_senha(nova_senha, conf_senha)
                if res["numErro"] == 0:
                    st.success(res["mensagem"])
                else:
                    st.error(res["mensagem"])

    st.divider()
    if st.button("Sair", type="secondary"):
        st.session_state["auth_token"] = None
        st.rerun()

# ── Não autenticado: login / registro ─────────────────────────────────────────

else:
    tab_login, tab_registro = st.tabs(["🔑 Login", "📝 Criar conta"])

    with tab_login:
        st.subheader("Entrar na sua conta")

        with st.form("form_login"):
            email_login = st.text_input("E-mail", placeholder="seu@email.com")
            senha_login = st.text_input("Senha", type="password", placeholder="••••••••")
            entrar = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            if not email_login or not senha_login:
                st.warning("Preencha e-mail e senha.")
            else:
                resultado = login_usuario(email_login, senha_login)
                if resultado["numErro"] == 0:
                    st.session_state["auth_token"] = TOKEN_SESSAO
                    st.success(resultado["mensagem"])
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

    with tab_registro:
        st.subheader("Criar nova conta")

        with st.form("form_registro"):
            nome_reg = st.text_input("Nome completo", placeholder="João Silva")
            email_reg = st.text_input("E-mail", placeholder="seu@email.com")
            senha_reg = st.text_input("Senha", type="password", placeholder="••••••••")
            senha_conf = st.text_input("Confirmar senha", type="password", placeholder="••••••••")
            cadastrar = st.form_submit_button("Criar conta", use_container_width=True)

        if cadastrar:
            if not nome_reg or not email_reg or not senha_reg:
                st.warning("Preencha todos os campos obrigatórios.")
            elif senha_reg != senha_conf:
                st.error("As senhas não coincidem.")
            else:
                resultado = cadastrar_usuario(nome_reg, email_reg, senha_reg)
                if resultado["numErro"] == 0:
                    st.session_state["auth_token"] = TOKEN_SESSAO
                    st.success(resultado["mensagem"])
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])
