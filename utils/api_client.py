"""Camada única de acesso à API Xano + helpers de sessão/UI compartilhados
entre as páginas do EduTrack AI (Streamlit).
"""

from datetime import date, datetime

import requests
import streamlit as st

# URLs base da API Xano (workspace edutrack-ai, branch v1)
AUTH_URL = "https://x8ki-letl-twmt.n7.xano.io/api:OwEMGCzd"
EDIT_URL = "https://x8ki-letl-twmt.n7.xano.io/api:PIgO5Chd"
SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:zwpAOwnh"
TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:FJtu6_X0"

# status interno (vindo da API) -> rótulo exibido
STATUS_LABELS = {
    "Pendente": "⏳ Pendente",
    "Em_progresso": "🔄 Em progresso",
    "Completa": "✅ Completa",
    "Atrasada": "⚠️ Atrasada",
}
STATUS_OPTIONS = list(STATUS_LABELS.keys())

# subject.status interno -> rótulo exibido
SUBJECT_STATUS_LABELS = {
    "rascunho": "Rascunho",
    "ativo": "Ativo",
    "arquivado": "Arquivado",
}
SUBJECT_STATUS_OPTIONS = list(SUBJECT_STATUS_LABELS.keys())

# academic_task.priority interno -> rótulo exibido
PRIORITY_LABELS = {
    "Baixa": "Baixa",
    "Media": "Média",
    "Alta": "Alta",
}
PRIORITY_OPTIONS = list(PRIORITY_LABELS.keys())

# ícone e peso (para exibição e ordenação) por prioridade
PRIORITY_ICONS = {"Baixa": "⬇️", "Media": "➡️", "Alta": "⬆️"}
PRIORITY_WEIGHT = {"Baixa": 0, "Media": 1, "Alta": 2}


# ── Sessão ───────────────────────────────────────────────────────────────────

def get_token():
    return st.session_state.get("auth_token")


def set_token(token):
    st.session_state["auth_token"] = token


def clear_token():
    st.session_state["auth_token"] = None


def is_authenticated():
    return bool(get_token())


def require_session(message=None):
    """Garante que o usuário está autenticado. Para o restante da página
    (st.stop) caso contrário, exibindo a mensagem apropriada."""
    if st.session_state.pop("session_expired", False):
        clear_token()
        st.warning("Sua sessão expirou. Faça login novamente.")
        st.info("Acesse a página **👤 Perfil** para entrar novamente.")
        st.stop()

    if not is_authenticated():
        st.warning(message or "Você precisa estar autenticado para acessar esta página.")
        st.info("Acesse a página **👤 Perfil** para fazer login ou criar uma conta.")
        st.stop()


# ── Requisições ──────────────────────────────────────────────────────────────

def _safe_json(resp):
    try:
        return resp.json()
    except ValueError:
        return {}


def request(method: str, url: str, auth: bool = True, **kwargs):
    """Wrapper genérico sobre requests. Retorna (data, error).

    - Em respostas 401, limpa a sessão e marca `session_expired` para a
      próxima página chamar `require_session()`.
    - Em respostas >= 400, retorna a mensagem de erro vinda da API (ou texto).
    """
    headers = kwargs.pop("headers", {})
    headers.setdefault("Content-Type", "application/json")

    if auth:
        token = get_token()
        if not token:
            return None, "Não autenticado"
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = requests.request(method, url, headers=headers, timeout=10, **kwargs)
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {e}"

    if auth and resp.status_code == 401:
        clear_token()
        st.session_state["session_expired"] = True
        return None, "Sessão expirada"

    if resp.status_code >= 400:
        data = _safe_json(resp)
        msg = data.get("message") if isinstance(data, dict) else None
        return None, msg or f"Erro {resp.status_code}: {resp.text}"

    if resp.status_code == 204 or not resp.content:
        return {}, None

    return _safe_json(resp), None


# ── Disciplinas (Subjects) ───────────────────────────────────────────────────

def fetch_subjects():
    data, err = request("GET", f"{SUBJECTS_URL}/subjects")
    if err:
        return None, err
    return data.get("items", []), None


def create_subject(payload: dict):
    return request("POST", f"{SUBJECTS_URL}/subjects", json=payload)


def update_subject(subject_id: int, payload: dict):
    return request("PATCH", f"{SUBJECTS_URL}/subjects/{subject_id}", json=payload)


def build_subject_payload(subject: dict, **changes) -> dict:
    """Monta o payload completo a partir da disciplina atual, sobrescrevendo só
    o que mudou. Garante que nenhum campo seja apagado quando a API não faz merge."""
    payload = {
        "name": subject.get("name"),
        "professor": subject.get("professor"),
        "carga_horaria": subject.get("CargaHoraria"),
        "status": subject.get("status", "ativo"),
        "semester": subject.get("semester", ""),
    }
    payload.update(changes)
    return payload


def delete_subject(subject_id: int):
    _, err = request("DELETE", f"{SUBJECTS_URL}/subjects/{subject_id}")
    return err is None, err


def search_subjects(q: str, has_overdue_tasks: bool):
    params = {}
    if q:
        params["q"] = q
    if has_overdue_tasks:
        params["has_overdue_tasks"] = "true"
    data, err = request("GET", f"{SUBJECTS_URL}/subjects/search", params=params)
    if err:
        return None, err
    return data.get("items", []), None


# ── Tarefas (Tasks) ──────────────────────────────────────────────────────────

def fetch_tasks():
    data, err = request("GET", f"{TASKS_URL}/tasks")
    if err:
        return [], err
    return data.get("items", []), None


def create_task(payload: dict):
    return request("POST", f"{TASKS_URL}/tasks", json=payload)


def update_task(task_id: int, payload: dict):
    return request("PATCH", f"{TASKS_URL}/tasks/{task_id}", json=payload)


def delete_task(task_id: int):
    _, err = request("DELETE", f"{TASKS_URL}/tasks/{task_id}")
    return err is None, err


# ── Datas de tarefas ─────────────────────────────────────────────────────────

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


def is_overdue(task: dict) -> bool:
    """Prazo vencido: data < hoje e tarefa não concluída."""
    if task.get("status") == "Completa":
        return False
    d = parse_due_date(task.get("data"))
    return d is not None and d < date.today()


def fmt_due(due) -> str:
    d = parse_due_date(due)
    return d.strftime("%d/%m/%Y") if d else "—"


def build_task_payload(task: dict, **changes) -> dict:
    """Monta o payload completo a partir da tarefa atual, sobrescrevendo só o
    que mudou. Garante que nenhum campo seja apagado quando a API não faz merge."""
    payload = {
        "title": task.get("title"),
        "description": task.get("description"),
        "data": task.get("data"),
        "status": task.get("status"),
        "subject_id": task.get("subject_id"),
        "priority": task.get("priority", "Media"),
    }
    payload.update(changes)
    return payload


# ── Autenticação e Perfil ────────────────────────────────────────────────────

def signup(name: str, email: str, password: str):
    try:
        resp = requests.post(
            f"{AUTH_URL}/auth/signup",
            json={"name": name, "email": email, "password": password},
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {e}"
    data = _safe_json(resp)
    if resp.status_code != 200:
        return None, data.get("message", "Erro no cadastro")
    return data.get("authToken"), None


def login(email: str, password: str):
    try:
        resp = requests.post(
            f"{AUTH_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {e}"
    data = _safe_json(resp)
    if resp.status_code != 200:
        return None, data.get("message", "E-mail ou senha incorretos")
    return data.get("authToken"), None


def get_profile():
    return request("GET", f"{AUTH_URL}/auth/me")


def edit_profile(name: str, email: str):
    return request("PATCH", f"{EDIT_URL}/user/edit_profile", json={"name": name, "email": email})


def change_password(new_password: str, confirm_password: str):
    return request(
        "POST",
        f"{AUTH_URL}/reset/update_password",
        json={"password": new_password, "confirm_password": confirm_password},
    )


def request_password_reset(email: str):
    """Solicita o e-mail com o magic link de redefinição de senha (sem autenticação)."""
    return request("POST", f"{AUTH_URL}/reset/request-reset-link", auth=False, json={"email": email})


def confirm_password_reset(email: str, code: str, password: str, confirm_password: str):
    """Confirma o código de redefinição recebido por e-mail e já grava a nova senha.
    Não exige autenticação: o código enviado por e-mail é a prova de identidade."""
    return request(
        "POST",
        f"{AUTH_URL}/reset/confirm-code",
        auth=False,
        json={
            "email": email,
            "code": code,
            "password": password,
            "confirm_password": confirm_password,
        },
    )


# ── UI: confirmação de exclusão ──────────────────────────────────────────────

def confirm_delete_button(item_id, label: str, on_confirm, key_prefix: str) -> bool:
    """Renderiza um botão de excluir com confirmação em dois passos via
    st.session_state. Retorna True se o item foi excluído com sucesso nesta
    execução (o chamador deve invalidar o cache e chamar st.rerun())."""
    confirm_key = f"{key_prefix}_confirm_delete_{item_id}"

    if not st.session_state.get(confirm_key):
        if st.button("🗑️ Excluir", key=f"{key_prefix}_del_{item_id}", type="secondary"):
            st.session_state[confirm_key] = True
            st.rerun()
        return False

    st.warning(f"Confirma a exclusão de **{label}**? Essa ação não pode ser desfeita.")
    col_sim, col_nao = st.columns(2)
    with col_sim:
        if st.button("✅ Sim, excluir", key=f"{key_prefix}_yes_{item_id}", type="primary"):
            ok, err = on_confirm()
            st.session_state.pop(confirm_key, None)
            if err:
                st.error(f"Erro ao excluir: {err}")
                return False
            return True
    with col_nao:
        if st.button("↩️ Cancelar", key=f"{key_prefix}_no_{item_id}"):
            st.session_state.pop(confirm_key, None)
            st.rerun()
    return False
