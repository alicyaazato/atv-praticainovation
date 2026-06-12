import streamlit as st

from utils.api_client import (
    PRIORITY_ICONS,
    PRIORITY_LABELS,
    PRIORITY_OPTIONS,
    STATUS_LABELS,
    fetch_subjects,
    fetch_tasks,
    fmt_due,
    is_authenticated,
    is_overdue,
    parse_due_date,
)

st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")


def dashboard_page():
    st.title("🎓 EduTrack AI — Dashboard")
    st.caption("Bem-vindo ao seu assistente acadêmico!")

    subjects, subj_err = fetch_subjects()
    if subj_err:
        st.error(f"Erro ao carregar disciplinas: {subj_err}")
        subjects = []

    tasks, task_err = fetch_tasks()
    if task_err:
        st.error(f"Erro ao carregar tarefas: {task_err}")
        tasks = []

    # ── Tela de boas-vindas para quem ainda não tem dados ───────────────────
    if not subjects:
        st.info("👋 Você ainda não tem nenhuma disciplina cadastrada.")
        st.markdown(
            "Comece cadastrando sua primeira disciplina para acompanhar suas "
            "tarefas e seu progresso acadêmico."
        )
        st.page_link("pages/1_📚_Disciplinas.py", label="➕ Cadastrar minha primeira disciplina", icon="📚")
        return

    subject_map = {s["id"]: s.get("name", "—") for s in subjects}
    subjects_ativas = [s for s in subjects if s.get("status", "ativo") == "ativo"]

    pendentes = [t for t in tasks if t.get("status") != "Completa"]
    atrasadas = [t for t in tasks if is_overdue(t)]

    # Progresso geral: média da taxa de conclusão por disciplina ativa (peso igual)
    progress_by_subject = {}
    for s in subjects_ativas:
        subj_tasks = [t for t in tasks if t.get("subject_id") == s["id"]]
        if subj_tasks:
            completed = sum(1 for t in subj_tasks if t.get("status") == "Completa")
            progress_by_subject[s["id"]] = completed / len(subj_tasks)
        else:
            progress_by_subject[s["id"]] = 0.0

    progresso_geral = sum(progress_by_subject.values()) / len(subjects_ativas) if subjects_ativas else 0.0

    # ── Métricas ─────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Disciplinas Ativas", len(subjects_ativas))
    col2.metric("📝 Tarefas Pendentes", len(pendentes))
    col3.metric("⚠️ Tarefas Atrasadas", len(atrasadas))
    col4.metric("📈 Progresso Geral", f"{progresso_geral * 100:.0f}%")

    st.divider()

    col_status, col_progress = st.columns(2)

    with col_status:
        st.subheader("Tarefas por Status")
        if not tasks:
            st.caption("Nenhuma tarefa cadastrada ainda.")
        else:
            for status_key, label in STATUS_LABELS.items():
                count = sum(1 for t in tasks if t.get("status") == status_key)
                st.write(f"**{label}:** {count}")

    with col_progress:
        st.subheader("Progresso por Disciplina")
        if not subjects_ativas:
            st.caption("Nenhuma disciplina ativa.")
        else:
            for s in subjects_ativas:
                st.write(s.get("name", "—"))
                st.progress(progress_by_subject[s["id"]])

    col_priority, _ = st.columns(2)

    with col_priority:
        st.subheader("Tarefas por Prioridade")
        if not tasks:
            st.caption("Nenhuma tarefa cadastrada ainda.")
        else:
            for p in PRIORITY_OPTIONS:
                count = sum(1 for t in tasks if t.get("priority", "Media") == p)
                st.write(f"{PRIORITY_ICONS[p]} **{PRIORITY_LABELS[p]}:** {count}")

    st.divider()

    st.subheader("Próximas Tarefas")
    proximas = sorted(
        (t for t in pendentes if parse_due_date(t.get("data")) is not None),
        key=lambda t: parse_due_date(t.get("data")),
    )[:5]

    if not proximas:
        st.caption("Nenhuma tarefa pendente com prazo definido.")
    else:
        for t in proximas:
            marcador = "🔴 " if is_overdue(t) else "• "
            disciplina = subject_map.get(t.get("subject_id"), "—")
            st.write(f"{marcador}**{t.get('title', '—')}** — {disciplina} — prazo: {fmt_due(t.get('data'))}")


if is_authenticated():
    pages = [
        st.Page(dashboard_page, title="Dashboard", icon="📊", default=True),
        st.Page("pages/1_📚_Disciplinas.py", title="Disciplinas", icon="📚"),
        st.Page("pages/2_📝_Tarefas.py", title="Tarefas", icon="📝"),
        st.Page("pages/4_📈_Relatorios.py", title="Relatórios", icon="📈"),
        st.Page("pages/3_👤_Perfil.py", title="Perfil", icon="👤"),
    ]
else:
    pages = [
        st.Page("pages/3_👤_Perfil.py", title="Entrar / Cadastrar", icon="🔑", default=True),
    ]

nav = st.navigation(pages)
nav.run()
