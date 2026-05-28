import streamlit as st
import requests

st.set_page_config(page_title="Disciplinas", page_icon="📚")

XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:v1"

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
        resp = requests.get(f"{XANO_BASE_URL}/subjects/my", headers=headers, timeout=10)
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


# Task 4.3: calls GET /subjects/search with at least one filter
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
    st.stop()

tab_lista, tab_busca, tab_nova = st.tabs(["📋 Minhas Disciplinas", "🔍 Buscar", "➕ Nova Disciplina"])

# ── Tab: list ─────────────────────────────────────────────────────────────────

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
                    st.write(f"**Código:** {subj.get('code') or '—'}")
                    st.write(f"**Descrição:** {subj.get('description') or '—'}")
                    st.write(f"**Semestre:** {subj.get('semester') or '—'}  |  **Ano:** {subj.get('year') or '—'}")
                    st.write(f"**Créditos:** {subj.get('credits') or '—'}  |  **Status:** {subj.get('status') or '—'}")

                with col_actions:
                    # ── Edit form ──────────────────────────────────────────
                    with st.form(key=f"edit_{subj_id}"):
                        st.markdown("**Editar**")
                        new_name = st.text_input("Nome", value=subj.get("name", ""), key=f"name_{subj_id}")
                        new_code = st.text_input("Código", value=subj.get("code") or "", key=f"code_{subj_id}")
                        new_desc = st.text_area("Descrição", value=subj.get("description") or "", key=f"desc_{subj_id}", height=80)
                        new_credits = st.number_input("Créditos", min_value=0, max_value=20, value=int(subj.get("credits") or 0), key=f"credits_{subj_id}")
                        new_year = st.number_input("Ano", min_value=1900, max_value=2100, value=int(subj.get("year") or 2024), key=f"year_{subj_id}")
                        new_status = st.selectbox("Status", ["active", "archived", "draft"], index=["active", "archived", "draft"].index(subj.get("status") or "active"), key=f"status_{subj_id}")
                        save_btn = st.form_submit_button("💾 Salvar")

                    if save_btn:
                        patch_payload = {}
                        if new_name and new_name != subj.get("name"):
                            patch_payload["name"] = new_name
                        if new_code != (subj.get("code") or ""):
                            patch_payload["code"] = new_code
                        if new_desc != (subj.get("description") or ""):
                            patch_payload["description"] = new_desc
                        if new_credits != (subj.get("credits") or 0):
                            patch_payload["credits"] = new_credits
                        if new_year != (subj.get("year") or 2024):
                            patch_payload["year"] = new_year
                        if new_status != subj.get("status"):
                            patch_payload["status"] = new_status

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

                    # ── Delete button ──────────────────────────────────────
                    if st.button("🗑️ Excluir", key=f"del_{subj_id}", type="secondary"):
                        ok, err = delete_subject(subj_id)
                        if err:
                            st.error(f"Erro ao excluir: {err}")
                        else:
                            st.success(f"Disciplina '{subj.get('name')}' excluída.")
                            st.session_state.pop("subjects_cache", None)
                            st.rerun()

# ── Tab: search ───────────────────────────────────────────────────────────────

with tab_busca:
    st.subheader("Buscar Disciplinas")

    # Task 4.2: search controls
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
            # Task 4.5: informative message on empty results
            elif not resultados:
                st.info("Nenhuma disciplina encontrada com os filtros informados.")
            else:
                st.write(f"**{len(resultados)} disciplina(s) encontrada(s)**")
                # Task 4.4: cards with name, code and overdue indicator.
                # The indicator is only accurate when overdue was the sole filter —
                # in combined mode (q + atrasadas) we cannot tell which match came from which filter.
                only_overdue_filter = busca_atrasadas and not busca_nome
                for subj in resultados:
                    label = f"📘 {subj.get('name', '—')}"
                    if only_overdue_filter:
                        label += "  ⚠️ com tarefas atrasadas"
                    with st.expander(label, expanded=False):
                        st.write(f"**ID:** {subj.get('id')}")
                        st.write(f"**Código:** {subj.get('code') or '—'}")
                        st.write(f"**Descrição:** {subj.get('description') or '—'}")
                        st.write(
                            f"**Semestre:** {subj.get('semester') or '—'}  |  "
                            f"**Ano:** {subj.get('year') or '—'}  |  "
                            f"**Créditos:** {subj.get('credits') or '—'}"
                        )
                        st.write(f"**Status:** {subj.get('status') or '—'}")

# ── Tab: create ───────────────────────────────────────────────────────────────

with tab_nova:
    st.subheader("Cadastrar Nova Disciplina")
    with st.form("form_nova_disciplina"):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
        codigo = st.text_input("Código", placeholder="Ex: MAT101")
        descricao = st.text_area("Descrição", placeholder="Descrição opcional...", height=100)
        col1, col2, col3 = st.columns(3)
        with col1:
            creditos = st.number_input("Créditos", min_value=0, max_value=20, value=0)
        with col2:
            ano = st.number_input("Ano", min_value=1900, max_value=2100, value=2024)
        with col3:
            semestre = st.selectbox("Semestre", ["", "1", "2", "3", "4", "5", "6", "7", "8", "full-year"])
        status = st.selectbox("Status", ["active", "archived", "draft"])
        submitted = st.form_submit_button("✅ Cadastrar Disciplina")

    if submitted:
        if not nome or len(nome.strip()) < 3:
            st.error("O nome da disciplina é obrigatório (mínimo 3 caracteres).")
        else:
            payload = {"name": nome.strip(), "status": status}
            if codigo:
                payload["code"] = codigo.strip()
            if descricao:
                payload["description"] = descricao.strip()
            if creditos:
                payload["credits"] = creditos
            if ano:
                payload["year"] = ano
            if semestre:
                payload["semester"] = semestre

            _, err = create_subject(payload)
            if err:
                st.error(f"Erro ao cadastrar: {err}")
            else:
                st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
                st.session_state.pop("subjects_cache", None)
