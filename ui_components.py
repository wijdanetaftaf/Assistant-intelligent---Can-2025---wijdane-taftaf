"""
Composants UI réutilisables pour l'application Streamlit CAN 2025
"""

import streamlit as st

# Couleurs du thème
PRIMARY = "#1A472A"
SECONDARY = "#2D6A3E"
ACCENT = "#F4A261"
RED_ACCENT = "#C1272D"
LIGHT_BG = "#F8F9FA"
WHITE = "#FFFFFF"
TEXT_DARK = "#212529"
TEXT_LIGHT = "#6C757D"


def display_metric_card(icon, label, value, is_accent=False):
    """
    Affiche une carte métrique stylisée

    Args:
        icon: Emoji ou icône à afficher
        label: Titre de la métrique
        value: Valeur à afficher
        is_accent: Si True, utilise la couleur rouge accent
    """
    value_class = 'red-accent' if is_accent else ''

    st.markdown(
        f"""<div class='metric-card'>
            <div class='metric-card-icon'>{icon}</div>
            <h3>{label}</h3>
            <h2 class='{value_class}'>{value}</h2>
        </div>""",
        unsafe_allow_html=True
    )


def display_info_box(title, content, icon="ℹ️", box_type="info"):
    """
    Affiche une boîte d'information stylisée

    Args:
        title: Titre de la boîte (optionnel)
        content: Contenu à afficher
        icon: Icône à afficher
        box_type: "info" (vert) ou "highlight" (rouge)
    """
    box_class = 'info-box' if box_type == 'info' else 'highlight-box'
    color = PRIMARY if box_type == 'info' else RED_ACCENT

    title_html = f"<h3 style='margin: 0 0 0.5rem 0; color: {color};'>{icon} {title}</h3>" if title else ""

    st.markdown(
        f"""<div class='{box_class}'>
            {title_html}
            <p style='margin: 0; color: {TEXT_DARK}; font-weight: 600;'>
                {content}
            </p>
        </div>""",
        unsafe_allow_html=True
    )


def display_section_title(title, icon=""):
    """
    Affiche un titre de section stylisé

    Args:
        title: Titre à afficher
        icon: Emoji optionnel
    """
    st.markdown(
        f"""<div class='section-title'>
            <h3>{icon} {title}</h3>
        </div>""",
        unsafe_allow_html=True
    )


def display_page_header(title, subtitle=""):
    """
    Affiche l'en-tête de page stylisé

    Args:
        title: Titre principal de la page
        subtitle: Sous-titre optionnel
    """
    subtitle_html = f"<p style='color: {TEXT_LIGHT}; margin-top: 0.5rem;'>{subtitle}</p>" if subtitle else ""

    st.markdown(
        f"""<div class='page-header'>
            <h1>{title}</h1>
            {subtitle_html}
        </div>""",
        unsafe_allow_html=True
    )


def display_stadium_card(name, city, capacity, card_type="biggest"):
    """
    Affiche une carte de stade stylisée

    Args:
        name: Nom du stade
        city: Ville
        capacity: Capacité (nombre)
        card_type: "biggest" (vert) ou "smallest" (rouge)
    """
    if card_type == "biggest":
        box_class = 'info-box'
        title_color = PRIMARY
        name_color = RED_ACCENT
        icon = "🏆"
        title = "Plus Grand Stade"
    else:
        box_class = 'highlight-box'
        title_color = RED_ACCENT
        name_color = PRIMARY
        icon = "📍"
        title = "Plus Petit Stade"

    st.markdown(
        f"""<div class='{box_class}'>
            <h3 style='margin: 0 0 0.5rem 0; color: {title_color};'>{icon} {title}</h3>
            <p style='margin: 0; font-weight: 700; font-size: 1.2rem; color: {name_color};'>
                {name} — {city}
            </p>
            <p style='margin: 0.25rem 0 0 0; color: {TEXT_LIGHT};'>
                Capacité : {capacity:,} places
            </p>
        </div>""",
        unsafe_allow_html=True
    )


def display_chat_message(sender, message, is_user=True):
    """
    Affiche un message de chat stylisé

    Args:
        sender: Nom de l'expéditeur
        message: Contenu du message
        is_user: True si c'est un message utilisateur, False pour le bot
    """
    chat_class = 'chat-user' if is_user else 'chat-bot'

    st.markdown(
        f"""<div class='{chat_class}'>
            <b>{sender}</b><br>{message}
        </div>""",
        unsafe_allow_html=True
    )


def display_metrics_row(metrics):
    """
    Affiche une ligne de métriques (2 à 4 cartes)

    Args:
        metrics: Liste de dictionnaires avec keys: 'icon', 'label', 'value', 'is_accent' (optionnel)
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            display_metric_card(
                icon=metric['icon'],
                label=metric['label'],
                value=metric['value'],
                is_accent=metric.get('is_accent', False)
            )


def get_css_styles():
    """
    Retourne le CSS complet de l'application
    """
    return f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {LIGHT_BG};
    color: {TEXT_DARK};
}}

/* Headers */
h1 {{
    color: {PRIMARY};
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

h2 {{
    color: {SECONDARY};
    font-weight: 600;
    font-size: 1.8rem;
}}

h3 {{
    color: {TEXT_DARK};
    font-weight: 600;
    font-size: 1.2rem;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PRIMARY} 0%, {SECONDARY} 100%);
    padding-top: 2rem;
}}

section[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}

section[data-testid="stSidebar"] .stRadio > label {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {WHITE} !important;
}}

section[data-testid="stSidebar"] [role="radiogroup"] label {{
    padding: 0.75rem 1rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    background-color: transparent;
}}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

section[data-testid="stSidebar"] [role="radiogroup"] label[data-baseweb="radio"] {{
    display: flex;
    align-items: center;
}}

section[data-testid="stSidebar"] [role="radiogroup"] label div[role="radio"] {{
    display: none !important;
}}

/* Chat Messages */
.chat-user {{
    background: linear-gradient(135deg, {WHITE} 0%, #F8F9FA 100%);
    padding: 1rem 1.25rem;
    border-radius: 16px;
    margin: 1rem 0;
    max-width: 75%;
    margin-left: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #E9ECEF;
}}

.chat-bot {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    color: {WHITE};
    padding: 1rem 1.25rem;
    border-radius: 16px;
    margin: 1rem 0;
    max-width: 75%;
    margin-right: auto;
    box-shadow: 0 4px 12px rgba(26, 71, 42, 0.15);
}}

.chat-user b, .chat-bot b {{
    font-size: 0.85rem;
    opacity: 0.9;
    display: block;
    margin-bottom: 0.5rem;
}}

/* Input Fields */
.stTextInput input {{
    background-color: {WHITE} !important;
    border-radius: 12px !important;
    border: 2px solid #E9ECEF !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}}

.stTextInput input:focus {{
    border-color: {PRIMARY} !important;
    box-shadow: 0 0 0 3px rgba(26, 71, 42, 0.1) !important;
}}

/* Buttons */
.stButton button {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%) !important;
    color: {WHITE} !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(26, 71, 42, 0.2) !important;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(26, 71, 42, 0.3) !important;
}}

/* Red Accent Elements */
.red-accent {{
    color: {RED_ACCENT};
    font-weight: 700;
}}

.red-badge {{
    background: linear-gradient(135deg, {RED_ACCENT} 0%, #A01F24 100%);
    color: {WHITE};
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    box-shadow: 0 2px 8px rgba(193, 39, 45, 0.3);
}}

.info-box {{
    background: linear-gradient(135deg, #E8F5E9 0%, #F1F8F4 100%);
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    border-left: 4px solid {PRIMARY};
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}

.highlight-box {{
    background: linear-gradient(135deg, #FFE5E5 0%, #FFF5F5 100%);
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    border-left: 4px solid {RED_ACCENT};
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(193, 39, 45, 0.1);
}}

/* Metric Cards */
.metric-card {{
    background: {WHITE};
    padding: 1.75rem;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid #E9ECEF;
    text-align: center;
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}}

.metric-card h3 {{
    color: {TEXT_LIGHT};
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.metric-card h2 {{
    color: {PRIMARY};
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}}

.metric-card-icon {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background-color: {WHITE} !important;
    border-radius: 12px !important;
    border: 2px solid #E9ECEF !important;
    transition: all 0.3s ease !important;
}}

.stSelectbox > div > div:hover {{
    border-color: {PRIMARY} !important;
    box-shadow: 0 0 0 3px rgba(26, 71, 42, 0.1) !important;
}}

.stSelectbox label {{
    font-weight: 600 !important;
    color: {TEXT_DARK} !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
}}

/* Dataframe */
.stDataFrame {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}}

.stDataFrame [data-testid="stDataFrameResizable"] {{
    border-radius: 12px;
}}

/* Table Styling */
table {{
    border-collapse: separate !important;
    border-spacing: 0 !important;
}}

thead tr th {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%) !important;
    color: {WHITE} !important;
    font-weight: 600 !important;
    padding: 1rem !important;
    border: none !important;
}}

tbody tr {{
    transition: all 0.2s ease;
}}

tbody tr:hover {{
    background-color: rgba(26, 71, 42, 0.05) !important;
    transform: scale(1.01);
}}

tbody tr td {{
    padding: 0.75rem 1rem !important;
    border-bottom: 1px solid #E9ECEF !important;
}}

/* Info Box */
.stAlert {{
    background-color: {WHITE} !important;
    border-left: 4px solid {ACCENT} !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
}}

/* Caption */
.caption {{
    color: {TEXT_LIGHT};
    font-size: 0.9rem;
    margin-top: 0.5rem;
}}

/* Page Title Container */
.page-header {{
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 3px solid {PRIMARY};
    position: relative;
}}

.page-header::after {{
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 100px;
    height: 3px;
    background: {RED_ACCENT};
}}

.section-title {{
    background: linear-gradient(135deg, {WHITE} 0%, #F8F9FA 100%);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    border-left: 4px solid {PRIMARY};
    margin: 1.5rem 0 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}

.section-title h3 {{
    margin: 0;
    color: {PRIMARY};
    font-weight: 700;
}}

/* Spinner */
.stSpinner > div {{
    border-top-color: {PRIMARY} !important;
}}
</style>
"""
