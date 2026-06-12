import csv
import io
from datetime import date, timedelta

import streamlit as st

from utils.api_client import (
    PRIORITY_LABELS,
    STATUS_LABELS,
    fetch_subjects,
    fetch_tasks,
    fmt_due,
    is_overdue,
    parse_due_date,
    require_session,
)

st.title("📈 Relatórios e Progresso")

require_session()

subjects, subj_err = fetch_subjects()
if subj_err:
    st.error(f"Erro ao carregar disciplinas: {subj_err}")
    subjects = []

tasks, task_err = fetch_tasks()
if task_err:
    st.error(f"Erro ao carregar tarefas: {task_err}")
    tasks = []

if not subjects:
    st.info("Nenhuma disciplina cadastrada ainda. Cadastre disciplinas e tarefas para ver relatórios aqui.")
    st.stop()

subject_map = {s["id"]: s.get("name", "—") for s in subjects}

# ── Progresso por Disciplina (não filtrado por período) ─────────────────────

st.subheader("Progresso por Disciplina")

incluir_arquivadas = st.checkbox("Incluir disciplinas arquivadas")

subjects_progresso = subjects if incluir_arquivadas else [s for s in subjects if s.get("status", "ativo") == "ativo"]

if not subjects_progresso:
    st.caption("Nenhuma disciplina ativa.")
else:
    for s in subjects_progresso:
        subj_tasks = [t for t in tasks if t.get("subject_id") == s["id"]]
        if subj_tasks:
            completed = sum(1 for t in subj_tasks if t.get("status") == "Completa")
            rate = completed / len(subj_tasks)
            st.write(f"**{s.get('name', '—')}** — {completed}/{len(subj_tasks)} tarefas concluídas")
        else:
            rate = 0.0
            st.write(f"**{s.get('name', '—')}** — sem tarefas")
        st.progress(rate)

st.divider()

# ── Histórico de Tarefas ──────────────────────────────────────────────────────

st.subheader("Histórico de Tarefas")

col1, col2, col3 = st.columns(3)
with col1:
    data_inicio = st.date_input("De", value=date.today() - timedelta(days=30))
with col2:
    data_fim = st.date_input("Até", value=date.today())
with col3:
    opcoes_disciplina = ["Todas"] + [s["id"] for s in subjects]
    disciplina_sel = st.selectbox(
        "Disciplina",
        options=opcoes_disciplina,
        format_func=lambda i: "Todas" if i == "Todas" else subject_map.get(i, f"ID {i}"),
    )

if data_inicio > data_fim:
    st.warning("A data inicial não pode ser depois da data final.")
    filtradas = []
else:
    filtradas = []
    for t in tasks:
        prazo = parse_due_date(t.get("data"))
        if prazo is None or not (data_inicio <= prazo <= data_fim):
            continue
        if disciplina_sel != "Todas" and t.get("subject_id") != disciplina_sel:
            continue
        filtradas.append(t)
    filtradas.sort(key=lambda t: parse_due_date(t.get("data")))

if not filtradas:
    st.info("Nenhuma tarefa encontrada para os filtros selecionados.")
else:
    linhas = [
        {
            "Título": t.get("title", "—"),
            "Disciplina": subject_map.get(t.get("subject_id"), "—"),
            "Status": STATUS_LABELS.get(t.get("status"), t.get("status")),
            "Prioridade": PRIORITY_LABELS.get(t.get("priority", "Media"), t.get("priority")),
            "Prazo": fmt_due(t.get("data")),
            "Atrasada": "Sim" if is_overdue(t) else "Não",
        }
        for t in filtradas
    ]

    st.dataframe(linhas, use_container_width=True)

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=linhas[0].keys())
    writer.writeheader()
    writer.writerows(linhas)

    st.download_button(
        "⬇️ Exportar CSV",
        data=buffer.getvalue().encode("utf-8-sig"),
        file_name="historico_tarefas.csv",
        mime="text/csv",
    )
