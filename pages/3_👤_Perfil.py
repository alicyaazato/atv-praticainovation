import streamlit as st

from utils.api_client import (
    clear_token,
    confirm_password_reset,
    edit_profile,
    get_profile,
    is_authenticated,
    login,
    request_password_reset,
    set_token,
    signup,
)
from utils.ui import inject_global_styles


def render_password_reset_flow(key_prefix: str, known_email: str | None = None):
    """Fluxo de redefinição de senha em 2 passos: solicitar código por e-mail
    e depois confirmar o código junto com a nova senha."""
    step_key = f"{key_prefix}_reset_step"
    email_key = f"{key_prefix}_reset_email"
    step = st.session_state.get(step_key, "request")

    if step == "request":
        with st.form(f"form_{key_prefix}_reset_request"):
            email_input = st.text_input(
                "E-mail cadastrado",
                value=known_email or "",
                disabled=bool(known_email),
                placeholder="seu@email.com",
                key=f"{key_prefix}_reset_email_input",
            )
            enviar = st.form_submit_button(
                "📧 Enviar código", type="primary", use_container_width=True
            )

        if enviar:
            alvo = (known_email or email_input).strip()
            if not alvo:
                st.warning("Informe seu e-mail.")
            else:
                _, err = request_password_reset(alvo)
                if err:
                    st.error(err)
                else:
                    st.session_state[email_key] = alvo
                    st.session_state[step_key] = "verify"
                    st.rerun()
        return

    email_alvo = st.session_state.get(email_key, known_email or "")
    st.success(f"Código enviado para **{email_alvo}**. Verifique sua caixa de entrada.")

    with st.form(f"form_{key_prefix}_reset_verify"):
        codigo = st.text_input(
            "Código recebido", max_chars=6, placeholder="000000", key=f"{key_prefix}_codigo"
        )
        nova_senha = st.text_input(
            "Nova senha", type="password", placeholder="Mínimo 8 caracteres",
            key=f"{key_prefix}_nova_senha",
        )
        conf_senha = st.text_input(
            "Confirmar nova senha", type="password", placeholder="••••••••",
            key=f"{key_prefix}_conf_senha",
        )
        col_confirmar, col_reenviar = st.columns(2)
        with col_confirmar:
            confirmar = st.form_submit_button(
                "🔒 Confirmar e trocar senha", type="primary", use_container_width=True
            )
        with col_reenviar:
            reenviar = st.form_submit_button(
                "🔁 Reenviar código", use_container_width=True
            )

    if reenviar:
        _, err = request_password_reset(email_alvo)
        if err:
            st.error(err)
        else:
            st.success(f"Novo código enviado para {email_alvo}.")

    if confirmar:
        if not codigo or not nova_senha or not conf_senha:
            st.warning("Preencha todos os campos.")
        elif len(nova_senha) < 8:
            st.error("A senha deve ter no mínimo 8 caracteres.")
        elif nova_senha != conf_senha:
            st.error("As senhas não coincidem.")
        else:
            _, err = confirm_password_reset(email_alvo, codigo.strip(), nova_senha, conf_senha)
            if err:
                st.error(err)
            else:
                st.session_state.pop(step_key, None)
                st.session_state.pop(email_key, None)
                st.success("Senha alterada com sucesso!")
                st.rerun()


# ── Autenticado ───────────────────────────────────────────────────────────────

if is_authenticated():
    inject_global_styles()

    dados, err = get_profile()
    if err:
        st.error(err)
        clear_token()
        st.rerun()

    # ── Card do usuário ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="
        background:#F9FAFB;
        border:1px solid #E5E7EB;
        border-radius:12px;
        padding:1.25rem 1.5rem;
        margin-bottom:1rem;
        display:flex;
        align-items:center;
        gap:1.25rem;
    ">
        <div style="font-size:3rem;line-height:1;">👤</div>
        <div>
            <div style="font-size:1.2rem;font-weight:700;color:#1F2937;">{dados.get('name', '—')}</div>
            <div style="color:#6B7280;font-size:.9rem;">{dados.get('email', '—')}</div>
            <div style="color:#9CA3AF;font-size:.78rem;margin-top:.2rem;">
                ID {dados.get('id', '—')} · {dados.get('role', '—')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs: editar perfil / segurança ───────────────────────────────────────
    tab_perfil, tab_seguranca = st.tabs(["✏️ Editar Perfil", "🔒 Segurança"])

    with tab_perfil:
        st.markdown("#### Informações da conta")

        with st.form("form_editar_perfil"):
            novo_nome = st.text_input("Nome completo", value=dados.get("name", ""))
            novo_email = st.text_input("E-mail", value=dados.get("email", ""))
            salvar = st.form_submit_button("💾 Salvar alterações", use_container_width=True, type="primary")

        if salvar:
            if not novo_nome or not novo_email:
                st.warning("Nome e e-mail são obrigatórios.")
            else:
                _, err = edit_profile(novo_nome.strip(), novo_email.strip())
                if err:
                    st.error(err)
                else:
                    st.success("Perfil atualizado com sucesso!")
                    st.rerun()

    with tab_seguranca:
        st.markdown("#### Redefinição de senha")
        st.info(
            "Por segurança, a senha é redefinida com um código enviado para o "
            "seu e-mail cadastrado. Informe o código recebido para confirmar a troca."
        )
        render_password_reset_flow("seg", known_email=dados.get("email"))

    # ── Sair ──────────────────────────────────────────────────────────────────
    st.divider()
    col_sair, _ = st.columns([1, 5])
    with col_sair:
        if st.button("Sair →", type="secondary", use_container_width=True):
            clear_token()
            st.rerun()

# ── Não autenticado: login / registro ─────────────────────────────────────────

else:
    st.markdown("""
    <style>
    .edu-hero { text-align: center; padding: 2.5rem 0 1.5rem; }
    .edu-hero h1 { color: #4F46E5; font-size: 2rem; font-weight: 700; margin: 0.4rem 0 0.2rem; }
    .edu-hero p  { color: #6B7280; font-size: .9rem; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])

    with mid:
        st.markdown("""
        <div class="edu-hero">
            <div style="font-size:3.5rem;line-height:1.2">🎓</div>
            <h1>EduTrack AI</h1>
            <p>Organize seus estudos com inteligência</p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_registro = st.tabs(["🔑 Entrar", "📝 Criar conta"])

        with tab_login:
            st.markdown("#### Bem-vindo de volta!")
            with st.form("form_login"):
                email_login = st.text_input("E-mail", placeholder="seu@email.com")
                senha_login = st.text_input("Senha", type="password", placeholder="••••••••")
                entrar = st.form_submit_button("Entrar →", use_container_width=True, type="primary")

            if entrar:
                if not email_login or not senha_login:
                    st.warning("Preencha e-mail e senha.")
                else:
                    token, err = login(email_login, senha_login)
                    if err:
                        st.error(err)
                    else:
                        set_token(token)
                        st.success("Login realizado com sucesso!")
                        st.rerun()

            with st.expander("Esqueci minha senha"):
                render_password_reset_flow("esq")

        with tab_registro:
            st.markdown("#### Crie sua conta gratuita")
            with st.form("form_registro"):
                nome_reg = st.text_input("Nome completo", placeholder="João Silva")
                email_reg = st.text_input("E-mail", placeholder="seu@email.com")
                senha_reg = st.text_input("Senha", type="password", placeholder="••••••••")
                senha_conf = st.text_input("Confirmar senha", type="password", placeholder="••••••••")
                cadastrar = st.form_submit_button("Criar conta →", use_container_width=True, type="primary")

            if cadastrar:
                if not nome_reg or not email_reg or not senha_reg:
                    st.warning("Preencha todos os campos obrigatórios.")
                elif senha_reg != senha_conf:
                    st.error("As senhas não coincidem.")
                else:
                    token, err = signup(nome_reg, email_reg, senha_reg)
                    if err:
                        st.error(err)
                    else:
                        set_token(token)
                        st.success("Usuário cadastrado com sucesso!")
                        st.rerun()
