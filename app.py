"""
Application Streamlit pour l'Assistant Intelligent CAN 2025
Version optimisée avec composants modulaires
"""

import streamlit as st
import pandas as pd
import re
from chatbot_can import ask_bot
from data_manager import load_classement, load_joueurs, load_stades
from ui_components import (
    display_metric_card, display_page_header, display_section_title,
    display_info_box, display_chat_message, display_stadium_card,
    display_metrics_row, get_css_styles
)

# Configuration de la page
st.set_page_config(
    page_title="CAN 2025 Assistant",
    page_icon="⚽",
    layout="wide"
)

# Application des styles CSS
st.markdown(get_css_styles(), unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Charge les données avec cache Streamlit"""
    with st.spinner("Chargement des données..."):
        return (
            load_classement(),
            load_joueurs(),
            load_stades()
        )


# Chargement des données
classement, joueurs, stades = load_data()

# Sidebar
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='font-size: 2.5rem; margin: 0; line-height: 1.2;'>🏆</h1>
    <h2 style='font-size: 1.5rem; margin: 0.5rem 0 0 0; font-weight: 700;'>CAN 2025</h2>
    <p style='font-size: 0.85rem; margin: 0.25rem 0 0 0; opacity: 0.9;'>Coupe d'Afrique des Nations</p>
    <div style='margin-top: 0.5rem;'>
        <span class='red-badge'>LIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["🤖 Chatbot", "📊 Classements", "👥 Joueurs", "🏟️ Stades"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align: center; font-size: 0.85rem; opacity: 0.8;'>"
    "Assistant intelligent basé sur les données officielles CAN 2025"
    "</p>",
    unsafe_allow_html=True
)

# Initialisation de l'historique
if "history" not in st.session_state:
    st.session_state.history = []


# ==================== PAGE CHATBOT ====================
if page == "🤖 Chatbot":
    display_page_header("🤖 Assistant CAN 2025")

    if not st.session_state.history:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FFE5E5 0%, #FFF5F5 100%);
                    padding: 1.5rem; border-radius: 16px; border-left: 4px solid #C1272D;
                    margin: 1rem 0; box-shadow: 0 4px 12px rgba(193, 39, 45, 0.1);'>
            <p style='margin: 0 0 1rem 0; color: #C1272D; font-weight: 700; font-size: 1.1rem;'>
                💬 Exemples de questions
            </p>
            <p style='margin: 0; color: #6C757D; line-height: 1.8;'>
                • Quand joue le Maroc ?<br>
                • Score Sénégal Mali<br>
                • Groupe du Cameroun
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Affichage de l'historique
    for q, r in st.session_state.history:
        display_chat_message("Vous", q, is_user=True)
        display_chat_message("Assistant", r, is_user=False)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Posez votre question...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col2:
        send = st.button("Envoyer", use_container_width=True)

    if send and user_input.strip():
        with st.spinner("Analyse en cours..."):
            response = ask_bot(user_input)
            st.session_state.history.append((user_input, response))
        st.rerun()


# ==================== PAGE CLASSEMENTS ====================
elif page == "📊 Classements":
    display_page_header(
        "📊 Classements des Groupes",
        "Suivez les performances de chaque équipe"
    )

    if classement.empty:
        st.error("Données de classement non disponibles")
    else:
        groupe = st.selectbox(
            "🎯 Choisir un groupe",
            sorted(classement["groupe"].unique()),
            key="groupe_select"
        )

        df = classement[classement["groupe"] == groupe].reset_index(drop=True)

        if not df.empty:
            st.markdown("<br>", unsafe_allow_html=True)

            # Métriques avec le nouveau système
            metrics = [
                {
                    'icon': '🥇',
                    'label': 'Leader',
                    'value': df.iloc[0]['equipe'],
                    'is_accent': True
                },
                {
                    'icon': '⭐',
                    'label': 'Points Leader',
                    'value': df.iloc[0]['pts']
                },
                {
                    'icon': '⚽',
                    'label': 'Total Points',
                    'value': df['pts'].sum()
                },
                {
                    'icon': '👥',
                    'label': 'Équipes',
                    'value': len(df)
                }
            ]
            display_metrics_row(metrics)

        # Section tableau
        display_section_title("Tableau du classement", "🏆")
        st.dataframe(df, use_container_width=True, height=400, hide_index=True)

        # Info box
        display_info_box(
            title="",
            content="ℹ️ Les deux premières équipes se qualifient pour la phase suivante",
            box_type="info"
        )


# ==================== PAGE JOUEURS ====================
elif page == "👥 Joueurs":
    display_page_header(
        "👥 Effectifs par Équipe",
        "Découvrez les joueurs de chaque sélection"
    )

    if joueurs.empty:
        st.error("Données de joueurs non disponibles")
    else:
        equipes_list = sorted(joueurs["equipe"].unique())
        equipe = st.selectbox(
            "🏴 Choisir une équipe",
            equipes_list,
            key="equipe_select"
        )

        # Extraction de l'âge
        def extract_age(text):
            if pd.isna(text):
                return None
            match = re.search(r'aged\s*(\d+)', str(text))
            return int(match.group(1)) if match else None

        df = joueurs[joueurs["equipe"] == equipe].copy()
        df["age"] = df["date_naissance"].apply(extract_age)

        # Métriques
        st.markdown("<br>", unsafe_allow_html=True)

        positions = df["poste"].nunique() if "poste" in df.columns else 0
        avg_age = round(df["age"].mean()) if df["age"].notna().any() else None

        metrics = [
            {
                'icon': '⚽',
                'label': 'Équipe',
                'value': equipe,
                'is_accent': True
            },
            {
                'icon': '👤',
                'label': 'Joueurs',
                'value': len(df)
            },
            {
                'icon': '🎯',
                'label': 'Postes',
                'value': positions if positions > 0 else 'N/A'
            },
            {
                'icon': '📅',
                'label': 'Âge Moyen',
                'value': avg_age if avg_age else 'N/A'
            }
        ]
        display_metrics_row(metrics)

        # Table des joueurs
        display_section_title("Liste des joueurs", "📋")
        st.dataframe(df[["joueur"]], use_container_width=True, height=500, hide_index=True)

        display_info_box(
            title="",
            content="💡 Effectif complet de la sélection nationale",
            box_type="highlight"
        )


# ==================== PAGE STADES ====================
elif page == "🏟️ Stades":
    display_page_header(
        "🏟️ Stades de la CAN 2025",
        "Infrastructure et capacités d'accueil"
    )

    if stades.empty:
        st.error("Données de stades non disponibles")
    else:
        # Métriques globales
        total_capacity = stades["capacite"].sum()
        avg_capacity = int(stades["capacite"].mean())

        metrics = [
            {
                'icon': '🏟️',
                'label': 'Nombre de Stades',
                'value': len(stades),
                'is_accent': True
            },
            {
                'icon': '👥',
                'label': 'Capacité Totale',
                'value': f"{total_capacity:,}".replace(',', ' ')
            },
            {
                'icon': '📊',
                'label': 'Capacité Moyenne',
                'value': f"{avg_capacity:,}".replace(',', ' ')
            }
        ]
        display_metrics_row(metrics)

        st.markdown("<br>", unsafe_allow_html=True)

        # Plus grand et plus petit stade
        if len(stades) > 0:
            col_biggest, col_smallest = st.columns(2)

            biggest_stadium = stades.loc[stades['capacite'].idxmax()]
            smallest_stadium = stades.loc[stades['capacite'].idxmin()]

            with col_biggest:
                display_stadium_card(
                    name=biggest_stadium['stade'],
                    city=biggest_stadium['ville'],
                    capacity=int(biggest_stadium['capacite']),
                    card_type="biggest"
                )

            with col_smallest:
                display_stadium_card(
                    name=smallest_stadium['stade'],
                    city=smallest_stadium['ville'],
                    capacity=int(smallest_stadium['capacite']),
                    card_type="smallest"
                )

        # Liste complète
        display_section_title("Liste complète des stades", "🗺️")
        st.dataframe(stades, use_container_width=True, height=400, hide_index=True)

        display_info_box(
            title="",
            content="ℹ️ Tous les stades répondent aux normes internationales de la CAF",
            box_type="info"
        )
