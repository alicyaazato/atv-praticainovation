from datetime import date

import streamlit as st

from utils.api_client import (
    PRIORITY_ICONS,
    PRIORITY_LABELS,
    PRIORITY_OPTIONS,
    PRIORITY_WEIGHT,
    STATUS_LABELS,
    STATUS_OPTIONS,
    build_task_payload,
    confirm_delete_button,
    create_task,
    delete_task,
    fetch_subjects,
    fetch_tasks,
    fmt_due,
    is_overdue,
    parse_due_date,
    require_session,
    to_xano_due,
    update_task,
)

# ── Página ────────────────────────────────────────────────────────────────────

st.title("📝 Minhas Tarefas")

require_session()

# carrega disciplinas (para o dropdown e para mapear subject_id -> nome)
subjects, subj_err = fetch_subjects()
if subj_err:
    st.error(f"Erro ao carregar disciplinas: {subj_err}")
subject_map = {s["id"]: s.get("name", "—") for s in subjects}

tab_lista, tab_nova = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

# ── Tab: nova tarefa ──────────────────────────────────────────────────────────

with tab_nova:
    st.subheader("Cadastrar Nova Tarefa")

    if not subjects:
        st.warning("Você precisa cadastrar uma disciplina antes de criar tarefas.")
    else:
        with st.form("form_nova_tarefa"):
            titulo = st.text_input("Título *", placeholder="Ex: Entregar relatório")
            descricao = st.text_area("Descrição", placeholder="Detalhes da tarefa")
            prazo = st.date_input("Prazo *", value=date.today())
            disciplina_id = st.selectbox(
                "Disciplina *",
                options=[s["id"] for s in subjects],
                format_func=lambda i: subject_map.get(i, f"ID {i}"),
            )
            prioridade = st.selectbox(
                "Prioridade",
                options=PRIORITY_OPTIONS,
                index=PRIORITY_OPTIONS.index("Media"),
                format_func=lambda p: PRIORITY_LABELS[p],
            )
            submitted = st.form_submit_button("✅ Cadastrar Tarefa")

        if submitted:
            if not titulo or len(titulo.strip()) < 3:
                st.error("O título é obrigatório (mínimo 3 caracteres).")
            else:
                payload = {
                    "title": titulo.strip(),
                    "description": descricao.strip(),
                    "data": to_xano_due(prazo),
                    "subject_id": disciplina_id,
                    "priority": prioridade,
                }
                _, err = create_task(payload)
                if err:
                    st.error(f"Erro ao cadastrar: {err}")
                else:
                    st.success(f"Tarefa **{titulo}** cadastrada com sucesso!")
                    st.session_state.pop("tasks_cache", None)

# ── Tab: lista ────────────────────────────────────────────────────────────────

with tab_lista:
    col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 1])
    with col_a:
        if st.button("🔄 Atualizar", key="refresh_tasks"):
            st.session_state.pop("tasks_cache", None)
    with col_b:
        agrupar_por = st.selectbox("Agrupar por", ["Disciplina", "Prazo", "Prioridade"])
    with col_c:
        filtro_status = st.selectbox("Status", ["Todas"] + list(STATUS_LABELS.values()))
    with col_d:
        filtro_prioridade = st.selectbox("Prioridade", ["Todas"] + list(PRIORITY_LABELS.values()))

    if "tasks_cache" not in st.session_state:
        tasks, err = fetch_tasks()
        if err:
            st.error(f"Erro ao carregar tarefas: {err}")
            tasks = []
        st.session_state["tasks_cache"] = tasks
    tasks = st.session_state["tasks_cache"]

    # filtro por status
    if filtro_status != "Todas":
        tasks = [t for t in tasks if STATUS_LABELS.get(t.get("status")) == filtro_status]

    # filtro por prioridade
    if filtro_prioridade != "Todas":
        tasks = [t for t in tasks if PRIORITY_LABELS.get(t.get("priority", "Media")) == filtro_prioridade]

    if not tasks:
        st.info("Nenhuma tarefa encontrada.")
    else:
        # monta grupos
        grupos = {}
        if agrupar_por == "Disciplina":
            for t in tasks:
                chave = subject_map.get(t.get("subject_id"), "Sem disciplina")
                grupos.setdefault(chave, []).append(t)
        elif agrupar_por == "Prazo":
            for t in tasks:
                chave = fmt_due(t.get("data"))
                grupos.setdefault(chave, []).append(t)
        else:  # Prioridade
            for p in sorted(PRIORITY_OPTIONS, key=lambda x: -PRIORITY_WEIGHT[x]):
                label = PRIORITY_LABELS[p]
                itens_p = [t for t in tasks if t.get("priority", "Media") == p]
                if itens_p:
                    grupos[label] = itens_p

        for grupo, itens in grupos.items():
            st.markdown(f"### {grupo}")
            for t in itens:
                tid = t.get("id")
                venc = is_overdue(t)
                status_lbl = STATUS_LABELS.get(t.get("status"), t.get("status"))
                icone_prioridade = PRIORITY_ICONS.get(t.get("priority", "Media"), "")
                titulo_exib = f"{icone_prioridade} {'❗ ' if venc else ''}{t.get('title', '—')} · {status_lbl}"

                with st.expander(titulo_exib):
                    if venc:
                        st.error("⚠️ Prazo vencido!")
                    st.write(f"**Descrição:** {t.get('description') or '—'}")
                    st.write(f"**Prazo:** {fmt_due(t.get('data'))}")
                    st.write(f"**Disciplina:** {subject_map.get(t.get('subject_id'), '—')}")

                    # marcar como concluída
                    if t.get("status") != "Completa":
                        if st.button("✅ Marcar como concluída", key=f"done_{tid}"):
                            _, err = update_task(tid, build_task_payload(t, status="Completa"))
                            if err:
                                st.error(f"Erro: {err}")
                            else:
                                st.session_state.pop("tasks_cache", None)
                                st.rerun()

                    # editar
                    with st.form(key=f"edit_task_{tid}"):
                        st.markdown("**Editar**")
                        novo_titulo = st.text_input("Título", value=t.get("title", ""), key=f"t_{tid}")
                        nova_desc = st.text_area("Descrição", value=t.get("description") or "", key=f"d_{tid}")
                        valor_prazo = parse_due_date(t.get("data")) or date.today()
                        novo_prazo = st.date_input("Prazo", value=valor_prazo, key=f"p_{tid}")
                        novo_status = st.selectbox(
                            "Status",
                            options=STATUS_OPTIONS,
                            index=STATUS_OPTIONS.index(t.get("status")) if t.get("status") in STATUS_OPTIONS else 0,
                            format_func=lambda s: STATUS_LABELS[s],
                            key=f"s_{tid}",
                        )
                        prioridade_atual = t.get("priority", "Media")
                        nova_prioridade = st.selectbox(
                            "Prioridade",
                            options=PRIORITY_OPTIONS,
                            index=PRIORITY_OPTIONS.index(prioridade_atual)
                            if prioridade_atual in PRIORITY_OPTIONS
                            else PRIORITY_OPTIONS.index("Media"),
                            format_func=lambda p: PRIORITY_LABELS[p],
                            key=f"prio_{tid}",
                        )
                        salvar = st.form_submit_button("💾 Salvar")

                    if salvar:
                        payload = build_task_payload(
                            t,
                            title=novo_titulo.strip(),
                            description=nova_desc.strip(),
                            data=to_xano_due(novo_prazo),
                            status=novo_status,
                            priority=nova_prioridade,
                        )
                        _, err = update_task(tid, payload)
                        if err:
                            st.error(f"Erro ao atualizar: {err}")
                        else:
                            st.success("Tarefa atualizada!")
                            st.session_state.pop("tasks_cache", None)
                            st.rerun()

                    # excluir
                    excluido = confirm_delete_button(
                        tid,
                        t.get("title", "—"),
                        on_confirm=lambda t_id=tid: delete_task(t_id),
                        key_prefix="task",
                    )
                    if excluido:
                        st.success("Tarefa excluída.")
                        st.session_state.pop("tasks_cache", None)
                        st.rerun()
