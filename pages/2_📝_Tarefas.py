import os
from datetime import date, datetime

import streamlit as st
import requests

st.set_page_config(page_title="Tarefas", page_icon="📝")


def load_dotenv(dotenv_path=".env"):
    if not os.path.exists(dotenv_path):
        return
    with open(dotenv_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv()

TASKS_URL = os.getenv("XANO_API_TASKS")
SUBJECTS_URL = os.getenv("XANO_API_SUBJECTS")

# status interno -> rótulo exibido
STATUS_LABELS = {
    "Pendente": "Pendente",
    "Em_progresso": "Em progresso",
    "Completa": "Completa",
    "Atrasada": "Atrasada"
}
STATUS_OPTIONS = list(STATUS_LABELS.keys())


def _auth_headers():
    token = st.session_state.get("auth_token")
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def fetch_subjects():
    headers = _auth_headers()
    if not headers:
        return [], "Não autenticado"
    try:
        resp = requests.get(f"{SUBJECTS_URL}/subjects", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("items", []), None
        return [], f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return [], str(e)


def fetch_tasks():
    headers = _auth_headers()
    if not headers:
        return [], "Não autenticado"
    try:
        resp = requests.get(f"{TASKS_URL}/tasks", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("items", []), None
        return [], f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return [], str(e)


def create_task(payload: dict):
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    try:
        resp = requests.post(f"{TASKS_URL}/tasks", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


def update_task(task_id: int, payload: dict):
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    try:
        resp = requests.patch(f"{TASKS_URL}/tasks/{task_id}", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


def delete_task(task_id: int):
    headers = _auth_headers()
    if not headers:
        return False, "Não autenticado"
    try:
        resp = requests.delete(f"{TASKS_URL}/tasks/{task_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            return True, None
        return False, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)


def to_xano_due(d: date) -> str:
    """Converte uma date para o formato brasileiro 'dd/mm/yyyy' (campo texto no Xano)."""
    return d.strftime("%d/%m/%Y")


def parse_due_date(due):
    """Interpreta o due_date vindo do Xano (dd/mm/yyyy ou ISO) e devolve uma date."""
    if due is None or due == "":
        return None
    texto = str(due).strip()
    # formato brasileiro dd/mm/yyyy
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        pass
    # fallback: ISO 'YYYY-MM-DD' (dados antigos)
    try:
        return date.fromisoformat(texto[:10])
    except ValueError:
        return None


def is_overdue(task):
    """Prazo vencido: data < hoje e tarefa não concluída."""
    if task.get("status") == "Completa":
        return False
    d = parse_due_date(task.get("data"))
    return d is not None and d < date.today()


def fmt_due(due):
    d = parse_due_date(due)
    return d.strftime("%d/%m/%Y") if d else "—"


def build_task_payload(task: dict, **changes) -> dict:
    """Monta o payload completo a partir da tarefa atual, sobrescrevendo só o que mudou.
    Garante que nenhum campo seja apagado quando a API não faz merge."""
    payload = {
        "title": task.get("title"),
        "description": task.get("description"),
        "data": task.get("data"),
        "status": task.get("status"),
        "subject_id": task.get("subject_id"),
    }
    payload.update(changes)
    return payload


# ── Página ────────────────────────────────────────────────────────────────────

st.title("📝 Minhas Tarefas")

if not st.session_state.get("auth_token"):
    st.warning("Você precisa estar autenticado para acessar esta página.")
    st.info("Acesse a página **👤 Perfil** para fazer login ou criar uma conta.")
    st.stop()

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
                }
                _, err = create_task(payload)
                if err:
                    st.error(f"Erro ao cadastrar: {err}")
                else:
                    st.success(f"Tarefa **{titulo}** cadastrada com sucesso!")
                    st.session_state.pop("tasks_cache", None)

# ── Tab: lista ────────────────────────────────────────────────────────────────

with tab_lista:
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        if st.button("🔄 Atualizar", key="refresh_tasks"):
            st.session_state.pop("tasks_cache", None)
    with col_b:
        agrupar_por = st.selectbox("Agrupar por", ["Disciplina", "Prazo"])
    with col_c:
        filtro_status = st.selectbox("Status", ["Todas"] + list(STATUS_LABELS.values()))

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

    if not tasks:
        st.info("Nenhuma tarefa encontrada.")
    else:
        # monta grupos
        grupos = {}
        if agrupar_por == "Disciplina":
            for t in tasks:
                chave = subject_map.get(t.get("subject_id"), "Sem disciplina")
                grupos.setdefault(chave, []).append(t)
        else:  # Prazo
            for t in tasks:
                chave = fmt_due(t.get("data"))
                grupos.setdefault(chave, []).append(t)

        for grupo, itens in grupos.items():
            st.markdown(f"### {grupo}")
            for t in itens:
                tid = t.get("id")
                venc = is_overdue(t)
                status_lbl = STATUS_LABELS.get(t.get("status"), t.get("status"))
                titulo_exib = f"{'🔴 ' if venc else ''}{t.get('title', '—')} · {status_lbl}"

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
                        salvar = st.form_submit_button("💾 Salvar")

                    if salvar:
                        payload = build_task_payload(
                            t,
                            title=novo_titulo.strip(),
                            description=nova_desc.strip(),
                            data=to_xano_due(novo_prazo),
                            status=novo_status,
                        )
                        _, err = update_task(tid, payload)
                        if err:
                            st.error(f"Erro ao atualizar: {err}")
                        else:
                            st.success("Tarefa atualizada!")
                            st.session_state.pop("tasks_cache", None)
                            st.rerun()

                    # excluir
                    if st.button("🗑️ Excluir", key=f"del_task_{tid}", type="secondary"):
                        ok, err = delete_task(tid)
                        if err:
                            st.error(f"Erro ao excluir: {err}")
                        else:
                            st.success("Tarefa excluída.")
                            st.session_state.pop("tasks_cache", None)
                            st.rerun()
