import streamlit as st

from utils.api_client import (
    confirm_delete_button,
    create_subject,
    delete_subject,
    fetch_subjects,
    require_session,
    search_subjects,
    update_subject,
)

# ── Page ─────────────────────────────────────────────────────────────────────

st.title("Gestão de Disciplinas")

require_session()

tab_lista, tab_busca, tab_nova = st.tabs(["📋 Minhas Disciplinas", "🔍 Buscar", "➕ Nova Disciplina"])

# ── Tab: listar ───────────────────────────────────────────────────────────────

with tab_lista:
    if st.button("🔄 Atualizar", key="refresh_list"):
        st.session_state.pop("subjects_cache", None)

    if "subjects_cache" not in st.session_state:
        subjects, err = fetch_subjects()
        if err:
            st.error(f"Erro ao carregar disciplinas: {err}")
            subjects = []
        st.session_state["subjects_cache"] = subjects or []

    subjects = st.session_state["subjects_cache"]

    if not subjects:
        st.info("Nenhuma disciplina cadastrada ainda. Use a aba **Nova Disciplina** para criar.")
    else:
        st.write(f"**{len(subjects)} disciplina(s) encontrada(s)**")

        for subj in subjects:
            subj_id = subj.get("id")
            with st.expander(f"📘 {subj.get('name', '—')} (ID: {subj_id})", expanded=False):
                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.write(f"**Professor:** {subj.get('professor') or '—'}")
                    st.write(f"**Carga Horária:** {subj.get('CargaHoraria') or '—'} h")

                with col_actions:
                    with st.form(key=f"edit_{subj_id}"):
                        st.markdown("**Editar**")
                        new_name = st.text_input("Nome", value=subj.get("name", ""), key=f"name_{subj_id}")
                        new_prof = st.text_input("Professor", value=subj.get("professor") or "", key=f"prof_{subj_id}")
                        new_ch = st.number_input(
                            "Carga Horária (h)",
                            min_value=0.0,
                            step=0.5,
                            value=float(subj.get("CargaHoraria") or 0),
                            key=f"ch_{subj_id}",
                        )
                        save_btn = st.form_submit_button("💾 Salvar")

                    if save_btn:
                        patch_payload = {}
                        if new_name and new_name != subj.get("name"):
                            patch_payload["name"] = new_name
                        if new_prof != (subj.get("professor") or ""):
                            patch_payload["professor"] = new_prof
                        if new_ch != float(subj.get("CargaHoraria") or 0):
                            patch_payload["carga_horaria"] = new_ch

                        if patch_payload:
                            _, err = update_subject(subj_id, patch_payload)
                            if err:
                                st.error(f"Erro ao atualizar: {err}")
                            else:
                                st.success("Disciplina atualizada!")
                                st.session_state.pop("subjects_cache", None)
                                st.rerun()
                        else:
                            st.info("Nenhuma alteração detectada.")

                    excluido = confirm_delete_button(
                        subj_id,
                        subj.get("name", "—"),
                        on_confirm=lambda sid=subj_id: delete_subject(sid),
                        key_prefix="subj",
                    )
                    if excluido:
                        st.success(f"Disciplina '{subj.get('name')}' excluída.")
                        st.session_state.pop("subjects_cache", None)
                        st.rerun()

# ── Tab: buscar ───────────────────────────────────────────────────────────────

with tab_busca:
    st.subheader("Buscar Disciplinas")

    with st.form("form_busca"):
        busca_nome = st.text_input("Buscar por nome", placeholder="Ex: Cálculo")
        busca_atrasadas = st.checkbox("Mostrar disciplinas com tarefas atrasadas")
        buscar_btn = st.form_submit_button("🔍 Buscar")

    if buscar_btn:
        if not busca_nome and not busca_atrasadas:
            st.warning("Informe um nome ou marque 'tarefas atrasadas' para buscar.")
        else:
            resultados, err = search_subjects(busca_nome.strip(), busca_atrasadas)
            if err:
                st.error(f"Erro na busca: {err}")
            elif not resultados:
                st.info("Nenhuma disciplina encontrada com os filtros informados.")
            else:
                st.write(f"**{len(resultados)} disciplina(s) encontrada(s)**")
                only_overdue = busca_atrasadas and not busca_nome
                for subj in resultados:
                    label = f"📘 {subj.get('name', '—')}"
                    if only_overdue:
                        label += "  ⚠️ com tarefas atrasadas"
                    with st.expander(label, expanded=False):
                        st.write(f"**ID:** {subj.get('id')}")
                        st.write(f"**Professor:** {subj.get('professor') or '—'}")
                        st.write(f"**Carga Horária:** {subj.get('CargaHoraria') or '—'} h")

# ── Tab: nova disciplina ──────────────────────────────────────────────────────

with tab_nova:
    st.subheader("Cadastrar Nova Disciplina")
    with st.form("form_nova_disciplina"):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
        professor = st.text_input("Professor *", placeholder="Ex: Prof. João Silva")
        carga_horaria = st.number_input("Carga Horária (h) *", min_value=0.0, step=0.5, value=0.0)
        submitted = st.form_submit_button("✅ Cadastrar Disciplina")

    if submitted:
        if not nome or len(nome.strip()) < 3:
            st.error("O nome da disciplina é obrigatório (mínimo 3 caracteres).")
        elif not professor or len(professor.strip()) < 3:
            st.error("O nome do professor é obrigatório (mínimo 3 caracteres).")
        elif carga_horaria <= 0:
            st.error("A carga horária deve ser maior que zero.")
        else:
            payload = {
                "name": nome.strip(),
                "professor": professor.strip(),
                "carga_horaria": carga_horaria,
            }
            _, err = create_subject(payload)
            if err:
                st.error(f"Erro ao cadastrar: {err}")
            else:
                st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
                st.session_state.pop("subjects_cache", None)
