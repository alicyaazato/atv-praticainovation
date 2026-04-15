import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# ========== MAPEAMENTO DE PÁGINAS ==========
PAGES = {
    "Dashboard": {"icon": "📊", "path": None},
    "Disciplinas": {"icon": "📚", "path": "pages/1_📚_Disciplinas.py"},
    "Tarefas": {"icon": "📝", "path": "pages/2_📝_Tarefas.py"},
    "Perfil": {"icon": "👤", "path": "pages/3_👤_Perfil.py"},
}
# ==========================================

# Título Principal
st.title("🎓 EduTrack AI")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")

# Criar opções dinamicamente a partir do mapeamento
menu_option = st.sidebar.radio(
    "Navegar", 
    [f"{PAGES[page]['icon']} {page}" for page in PAGES.keys()]
)

# Extrair a opção selecionada
selected_page = menu_option.split(" ", 1)[1]  # Remove o ícone e fica com o nome

# Navegação
if selected_page == "Dashboard":
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("Conecte ao Xano para ver seus dados reais.")
    # Exemplo de Métrica Visual
    col1, col2 = st.columns(2)
    col1.metric("Disciplinas Ativas", "0")
    col2.metric("Tarefas Pendentes", "0")
    
    # Exibir páginas disponíveis
    st.markdown("---")
    st.subheader("📍 Páginas Disponíveis")
    for page_name, page_info in PAGES.items():
        if page_name != "Dashboard" and page_info["path"]:
            st.markdown(f"- **{page_info['icon']} {page_name}**: `{page_info['path']}`")
            
elif PAGES[selected_page]["path"]:
    # Tentar navegar usando st.switch_page() se disponível, caso contrário mostrar instrução
    try:
        st.switch_page(PAGES[selected_page]["path"])
    except AttributeError:
        st.info(f"📄 Página: **{PAGES[selected_page]['icon']} {selected_page}**\nCaminho: `{PAGES[selected_page]['path']}`")