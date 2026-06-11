import os

import streamlit as st
import requests

st.set_page_config(page_title="Disciplinas", page_icon="📚")

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

XANO_BASE_URL = os.getenv("XANO_API_SUBJECTS")


def _auth_headers():
    token = st.session_state.get("auth_token")
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def fetch_subjects():
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    try:
        resp = requests.get(f"{XANO_BASE_URL}/subjects", headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("items", []), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


def create_subject(payload: dict):
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    try:
        resp = requests.post(f"{XANO_BASE_URL}/subjects", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


def update_subject(subject_id: int, payload: dict):
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    try:
        resp = requests.patch(
            f"{XANO_BASE_URL}/subjects/{subject_id}", json=payload, headers=headers, timeout=10
        )
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


def delete_subject(subject_id: int):
    headers = _auth_headers()
    if not headers:
        return False, "Não autenticado"
    try:
        resp = requests.delete(
            f"{XANO_BASE_URL}/subjects/{subject_id}", headers=headers, timeout=10
        )
        if resp.status_code == 200:
            return True, None
        return False, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)


def search_subjects(q: str, has_overdue_tasks: bool):
    headers = _auth_headers()
    if not headers:
        return None, "Não autenticado"
    params = {}
    if q:
        params["q"] = q
    if has_overdue_tasks:
        params["has_overdue_tasks"] = "true"
    try:
        resp = requests.get(
            f"{XANO_BASE_URL}/subjects/search",
            headers=headers,
            params=params,
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("items", []), None
        return None, f"Erro {resp.status_code}: {resp.text}"
    except Exception as e:
        return None, str(e)


# ── Page ─────────────────────────────────────────────────────────────────────

st.title("Gestão de Disciplinas")

if not st.session_state.get("auth_token"):
    st.warning("Você precisa estar autenticado para acessar esta página.")
    st.info("Acesse a página **👤 Perfil** para fazer login ou criar uma conta.")
    st.stop()

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

                    if st.button("🗑️ Excluir", key=f"del_{subj_id}", type="secondary"):
                        ok, err = delete_subject(subj_id)
                        if err:
                            st.error(f"Erro ao excluir: {err}")
                        else:
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
