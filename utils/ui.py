"""Helpers de UI compartilhados entre todas as páginas do EduTrack AI."""

import streamlit as st

# Paleta de cores da marca
BRAND_PRIMARY = "#4F46E5"
BRAND_TEXT = "#1F2937"
BRAND_MUTED = "#6B7280"
BRAND_BG_CARD = "#F9FAFB"
BRAND_BORDER = "#E5E7EB"

GLOBAL_CSS = f"""
<style>
/* ── EduTrack AI · Global Styles ─────────────────────────────────── */

/* Metric cards */
[data-testid="stMetric"] {{
    background: {BRAND_BG_CARD};
    border: 1px solid {BRAND_BORDER};
    border-radius: 10px;
    padding: 1rem 1.25rem;
}}
[data-testid="stMetricValue"] {{
    color: {BRAND_PRIMARY};
    font-weight: 700;
}}

/* Expander: cabeçalho em negrito */
[data-testid="stExpander"] summary p {{
    font-weight: 600;
    color: {BRAND_TEXT};
}}

/* Progress bar na cor primária */
[data-testid="stProgressBar"] > div > div {{
    background-color: {BRAND_PRIMARY} !important;
}}

/* Tabs: borda inferior mais visível na aba ativa */
[data-testid="stTabs"] [aria-selected="true"] {{
    border-bottom: 3px solid {BRAND_PRIMARY} !important;
    color: {BRAND_PRIMARY} !important;
    font-weight: 600;
}}

/* Rodapé do Streamlit: ocultar */
footer {{ visibility: hidden; }}
</style>
"""


def inject_global_styles():
    """Injeta o CSS global da identidade visual em qualquer página."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
