import streamlit as st

from utils.api_client import (
    SUBJECT_STATUS_LABELS,
    SUBJECT_STATUS_OPTIONS,
    build_subject_payload,
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
    col_refresh, col_filtro = st.columns([1, 2])
    with col_refresh:
        if st.button("🔄 Atualizar", key="refresh_list"):
            st.session_state.pop("subjects_cache", None)
    with col_filtro:
        filtro_status = st.selectbox(
            "Mostrar",
            ["Ativas", "Arquivadas", "Rascunhos", "Todas"],
            index=0,
            key="subjects_filtro_status",
        )

    if "subjects_cache" not in st.session_state:
        subjects, err = fetch_subjects()
        if err:
            st.error(f"Erro ao carregar disciplinas: {err}")
            subjects = []
        st.session_state["subjects_cache"] = subjects or []

    subjects = st.session_state["subjects_cache"]

    if filtro_status == "Ativas":
        subjects_exibidas = [s for s in subjects if s.get("status", "ativo") == "ativo"]
    elif filtro_status == "Arquivadas":
        subjects_exibidas = [s for s in subjects if s.get("status") == "arquivado"]
    elif filtro_status == "Rascunhos":
        subjects_exibidas = [s for s in subjects if s.get("status") == "rascunho"]
    else:
        subjects_exibidas = subjects

    if not subjects:
        st.info("Nenhuma disciplina cadastrada ainda. Use a aba **Nova Disciplina** para criar.")
    elif not subjects_exibidas:
        st.info("Nenhuma disciplina encontrada para o filtro selecionado.")
    else:
        st.write(f"**{len(subjects_exibidas)} disciplina(s) encontrada(s)**")

        for subj in subjects_exibidas:
            subj_id = subj.get("id")
            status_atual = subj.get("status", "ativo")
            semestre_atual = subj.get("semester", "")

            titulo = f"📘 {subj.get('name', '—')}"
            if semestre_atual:
                titulo += f" · {semestre_atual}"
            if status_atual == "arquivado":
                titulo += " 📦"
            titulo += f" (ID: {subj_id})"

            with st.expander(titulo, expanded=False):
                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.write(f"**Professor:** {subj.get('professor') or '—'}")
                    st.write(f"**Carga Horária:** {subj.get('CargaHoraria') or '—'} h")
                    st.write(f"**Status:** {SUBJECT_STATUS_LABELS.get(status_atual, status_atual)}")
                    st.write(f"**Semestre:** {semestre_atual or '—'}")

                with col_actions:
                    with st.form(key=f"edit_{subj_id}"):
                        st.markdown("**Editar**")
                        new_name = st.text_input("Nome", value=subj.get("name", ""), key=f"name_{subj_id}")
                        new_prof = st.text_input("Professor", value=subj.get("professor") or "", key=f"prof_{subj_id}")
                        new_ch = st.number_input(
                            "Carga Horária (h)",
                            min_value=0,
                            step=1,
                            value=int(subj.get("CargaHoraria") or 0),
                            key=f"ch_{subj_id}",
                        )
                        new_status = st.selectbox(
                            "Status",
                            options=SUBJECT_STATUS_OPTIONS,
                            index=SUBJECT_STATUS_OPTIONS.index(status_atual)
                            if status_atual in SUBJECT_STATUS_OPTIONS
                            else SUBJECT_STATUS_OPTIONS.index("ativo"),
                            format_func=lambda s: SUBJECT_STATUS_LABELS[s],
                            key=f"status_{subj_id}",
                        )
                        new_semester = st.text_input(
                            "Semestre/Período",
                            value=semestre_atual,
                            placeholder="Ex: 2026/1",
                            key=f"sem_{subj_id}",
                        )
                        save_btn = st.form_submit_button("💾 Salvar")

                    if save_btn:
                        patch_payload = {}
                        if new_name and new_name != subj.get("name"):
                            patch_payload["name"] = new_name
                        if new_prof != (subj.get("professor") or ""):
                            patch_payload["professor"] = new_prof
                        if new_ch != int(subj.get("CargaHoraria") or 0):
                            patch_payload["carga_horaria"] = new_ch
                        if new_status != status_atual:
                            patch_payload["status"] = new_status
                        if new_semester.strip() != semestre_atual:
                            patch_payload["semester"] = new_semester.strip()

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

                    if status_atual != "arquivado":
                        if st.button("📦 Arquivar", key=f"archive_{subj_id}"):
                            _, err = update_subject(subj_id, build_subject_payload(subj, status="arquivado"))
                            if err:
                                st.error(f"Erro ao arquivar: {err}")
                            else:
                                st.success("Disciplina arquivada.")
                                st.session_state.pop("subjects_cache", None)
                                st.rerun()
                    else:
                        if st.button("♻️ Reativar", key=f"unarchive_{subj_id}"):
                            _, err = update_subject(subj_id, build_subject_payload(subj, status="ativo"))
                            if err:
                                st.error(f"Erro ao reativar: {err}")
                            else:
                                st.success("Disciplina reativada.")
                                st.session_state.pop("subjects_cache", None)
                                st.rerun()

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
                        status_busca = subj.get("status", "ativo")
                        st.write(f"**Status:** {SUBJECT_STATUS_LABELS.get(status_busca, status_busca)}")
                        if subj.get("semester"):
                            st.write(f"**Semestre:** {subj.get('semester')}")

# ── Tab: nova disciplina ──────────────────────────────────────────────────────

with tab_nova:
    st.subheader("Cadastrar Nova Disciplina")
    with st.form("form_nova_disciplina"):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
        professor = st.text_input("Professor *", placeholder="Ex: Prof. João Silva")
        carga_horaria = st.number_input("Carga Horária (h) *", min_value=0, step=1, value=0)
        col_status, col_sem = st.columns(2)
        with col_status:
            status_novo = st.selectbox(
                "Status",
                options=SUBJECT_STATUS_OPTIONS,
                index=SUBJECT_STATUS_OPTIONS.index("ativo"),
                format_func=lambda s: SUBJECT_STATUS_LABELS[s],
            )
        with col_sem:
            semestre_novo = st.text_input("Semestre/Período", placeholder="Ex: 2026/1")
        submitted = st.form_submit_button("✅ Cadastrar Disciplina")

    if submitted:
        if not nome or len(nome.strip()) < 3:
            st.error("O nome da disciplina é obrigatório (mínimo 3 caracteres).")
        elif not professor or len(professor.strip()) < 3:
            st.error("O nome do professor é obrigatório (mínimo 3 caracteres).")
        elif carga_horaria <= 0:
            st.error("A carga horária deve ser maior que zero.")
        else:
            existing = st.session_state.get("subjects_cache", [])
            nome_n = nome.strip().lower()
            prof_n = professor.strip().lower()
            duplicata = any(
                s.get("name", "").strip().lower() == nome_n
                and s.get("professor", "").strip().lower() == prof_n
                for s in existing
            )
            if duplicata:
                st.warning(
                    f"Já existe uma disciplina **{nome.strip()}** com o professor **{professor.strip()}**. "
                    "Verifique sua lista de disciplinas."
                )
            else:
                payload = {
                    "name": nome.strip(),
                    "professor": professor.strip(),
                    "carga_horaria": carga_horaria,
                    "status": status_novo,
                    "semester": semestre_novo.strip(),
                }
                _, err = create_subject(payload)
                if err:
                    st.error(f"Erro ao cadastrar: {err}")
                else:
                    st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
                    st.session_state.pop("subjects_cache", None)
