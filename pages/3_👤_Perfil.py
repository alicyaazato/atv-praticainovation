import streamlit as st

from utils.api_client import (
    change_password,
    clear_token,
    edit_profile,
    get_profile,
    is_authenticated,
    login,
    magic_link_login,
    request_password_reset,
    set_token,
    signup,
)
from utils.ui import inject_global_styles

# ── Login via magic link (redefinição de senha) ────────────────────────────────

qp = st.query_params
if not is_authenticated() and "magic_token" in qp and "email" in qp:
    token, err = magic_link_login(qp["magic_token"], qp["email"])
    if err:
        st.error(f"Link de redefinição inválido ou expirado: {err}")
    else:
        set_token(token)
        st.session_state["force_password_tab"] = True
        st.query_params.clear()
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

    # ── Fluxo de magic link: definir nova senha imediatamente ─────────────────
    if st.session_state.pop("force_password_tab", False):
        st.info("Você acessou pelo link de redefinição de senha. Defina sua nova senha abaixo.")
        st.markdown("#### 🔒 Definir nova senha")

        with st.form("form_alterar_senha_magic"):
            nova_senha_m = st.text_input(
                "Nova senha", type="password",
                placeholder="Mínimo 8 caracteres", key="nova_senha_magic",
            )
            conf_senha_m = st.text_input(
                "Confirmar nova senha", type="password",
                placeholder="••••••••", key="conf_senha_magic",
            )
            alterar_m = st.form_submit_button("🔒 Alterar senha", use_container_width=True, type="primary")

        if alterar_m:
            if not nova_senha_m or not conf_senha_m:
                st.warning("Preencha os dois campos de senha.")
            elif len(nova_senha_m) < 8:
                st.error("A senha deve ter no mínimo 8 caracteres.")
            elif nova_senha_m != conf_senha_m:
                st.error("As senhas não coincidem.")
            else:
                _, err = change_password(nova_senha_m, conf_senha_m)
                if err:
                    st.error(err)
                else:
                    st.success("Senha alterada com sucesso!")

        st.divider()

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
            "Por segurança, a senha é redefinida exclusivamente via e-mail. "
            "Clique no botão abaixo para receber o link de redefinição no seu e-mail cadastrado."
        )
        st.write(f"**E-mail cadastrado:** {dados.get('email', '—')}")

        if st.button("📧 Enviar link de redefinição", type="primary", use_container_width=False):
            _, err = request_password_reset(dados.get("email", ""))
            if err:
                st.error(f"Erro ao enviar: {err}")
            else:
                st.success("Link de redefinição enviado! Verifique sua caixa de entrada.")

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
                with st.form("form_esqueci_senha"):
                    email_reset = st.text_input("E-mail cadastrado", placeholder="seu@email.com", key="email_reset")
                    enviar_reset = st.form_submit_button("Enviar link de redefinição", use_container_width=True)

                if enviar_reset:
                    if not email_reset:
                        st.warning("Informe seu e-mail.")
                    else:
                        _, err = request_password_reset(email_reset.strip())
                        if err:
                            st.error(err)
                        else:
                            st.success("Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.")

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
