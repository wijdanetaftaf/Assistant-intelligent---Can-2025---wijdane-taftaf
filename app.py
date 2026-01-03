import streamlit as st
import pandas as pd
from chatbot_can import ask_bot
import re

st.set_page_config(
    page_title="CAN 2025 Assistant",
    page_icon="⚽",
    layout="wide"
)

PRIMARY = "#1A472A"      
SECONDARY = "#2D6A3E"    
ACCENT = "#F4A261"       
RED_ACCENT = "#C1272D"   
LIGHT_BG = "#F8F9FA"     
WHITE = "#FFFFFF"
TEXT_DARK = "#212529"
TEXT_LIGHT = "#6C757D"

#css styles
st.markdown(f"""
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
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return (
        pd.read_csv("data/classement_groupes.csv"),
        pd.read_csv("data/joueurs_brut.csv"),
        pd.read_csv("data/stades.csv")
    )

classement, joueurs, stades = load_data()

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


if "history" not in st.session_state:
    st.session_state.history = []


if page == "🤖 Chatbot":

    st.markdown("<div class='page-header'><h1>🤖 Assistant CAN 2025</h1></div>", unsafe_allow_html=True)

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

    # Historique du chat
    for q, r in st.session_state.history:
        st.markdown(f"<div class='chat-user'><b>Vous</b><br>{q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bot'><b>Assistant</b><br>{r}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Posez votre question...",
            label_visibility="collapsed"
        )

    with col2:
        send = st.button("Envoyer", use_container_width=True)

    if send and user_input.strip():
        with st.spinner("Analyse en cours..."):
            response = ask_bot(user_input)
            st.session_state.history.append((user_input, response))

        st.rerun()





elif page == "📊 Classements":
    
    st.markdown("<div class='page-header'><h1>📊 Classements des Groupes</h1><p style='color: #6C757D; margin-top: 0.5rem;'>Suivez les performances de chaque équipe</p></div>", unsafe_allow_html=True)
    
    col_select, col_badge = st.columns([3, 1])
    
    with col_select:
        groupe = st.selectbox("🎯 Choisir un groupe", sorted(classement["groupe"].unique()), key="groupe_select")
    
    
    df = classement[classement["groupe"] == groupe].reset_index(drop=True)
    
    if not df.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""<div class='metric-card'>
                    <div class='metric-card-icon'>🥇</div>
                    <h3>Leader</h3>
                    <h2 class='red-accent'>{df.iloc[0]['equipe']}</h2>
                </div>""",
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""<div class='metric-card'>
                    <div class='metric-card-icon'>⭐</div>
                    <h3>Points Leader</h3>
                    <h2>{df.iloc[0]['pts']}</h2>
                </div>""",
                unsafe_allow_html=True
            )
        
        with col3:
            total_buts = df['pts'].sum() if 'pts' in df.columns else 0
            st.markdown(
                f"""<div class='metric-card'>
                    <div class='metric-card-icon'>⚽</div>
                    <h3>Total Buts</h3>
                    <h2>{total_buts}</h2>
                </div>""",
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""<div class='metric-card'>
                    <div class='metric-card-icon'>👥</div>
                    <h3>Équipes</h3>
                    <h2>{len(df)}</h2>
                </div>""",
                unsafe_allow_html=True
            )
    
    # Table Section
    st.markdown("""
        <div class='section-title'>
            <h3>🏆 Tableau du classement</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True, height=400, hide_index=True)
    
    # Info de plus
    if not df.empty:
        st.markdown("""
            <div class='info-box'>
                <p style='margin: 0; color: #1A472A; font-weight: 600;'>
                    ℹ️ Les deux premières équipes se qualifient pour la phase suivante
                </p>
            </div>
        """, unsafe_allow_html=True)


elif page == "👥 Joueurs":
    
    st.markdown("<div class='page-header'><h1>👥 Effectifs par Équipe</h1><p style='color: #6C757D; margin-top: 0.5rem;'>Découvrez les joueurs de chaque sélection</p></div>", unsafe_allow_html=True)
    
    # selector
    equipes_list = sorted(joueurs["equipe"].unique())
    
    col_select, col_search = st.columns([2, 1])
    
    with col_select:
        equipe = st.selectbox("🏴 Choisir une équipe", equipes_list, key="equipe_select")
    
    
    def extract_age(text):
        if pd.isna(text):
            return None
        match = re.search(r'aged\s*(\d+)', str(text))
        return int(match.group(1)) if match else None
    
    df = joueurs[joueurs["equipe"] == equipe]
    df = df.copy()
    df["age"] = df["date_naissance"].apply(extract_age)

    
    # Stats 
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-card-icon'>⚽</div>
                <h3>Équipe</h3>
                <h2 class='red-accent' style='font-size: 1.5rem;'>{equipe}</h2>
            </div>""",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-card-icon'>👤</div>
                <h3>Joueurs</h3>
                <h2>{len(df)}</h2>
            </div>""",
            unsafe_allow_html=True
        )

    
    with col3:
     positions = df["poste"].nunique() if "poste" in df.columns else 0
     st.markdown(
        f"""<div class='metric-card'>
            <div class='metric-card-icon'>🎯</div>
            <h3>Postes</h3>
            <h2>{positions if positions > 0 else 'N/A'}</h2>
        </div>""",
        unsafe_allow_html=True
    )

    with col4:
     avg_age = round(df["age"].mean()) if df["age"].notna().any() else None
     st.markdown(
        f"""<div class='metric-card'>
            <div class='metric-card-icon'>📅</div>
            <h3>Âge Moyen</h3>
            <h2>{avg_age if avg_age else 'N/A'}</h2>
        </div>""",
        unsafe_allow_html=True
    )

    
    # table players
    st.markdown("""
        <div class='section-title'>
            <h3>📋 Liste des joueurs</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df[["joueur"]], use_container_width=True, height=500, hide_index=True)
    
    st.markdown("""
        <div class='highlight-box'>
            <p style='margin: 0; color: #C1272D; font-weight: 600;'>
                💡 Effectif complet de la sélection nationale
            </p>
        </div>
    """, unsafe_allow_html=True)

elif page == "🏟️ Stades":
    
    st.markdown("<div class='page-header'><h1>🏟️ Stades de la CAN 2025</h1><p style='color: #6C757D; margin-top: 0.5rem;'>Infrastructure et capacités d'accueil</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    if "capacite" in stades.columns:
     stades["capacite"] = (
        stades["capacite"]
        .astype(str)
        .str.replace("\xa0", "", regex=False)  
        .str.replace(" ", "", regex=False)     
        .str.replace(",", "", regex=False)     
        .astype(int)
    )

    
    total_capacity = stades["capacite"].sum()
    avg_capacity = int(stades["capacite"].mean())

    with col1:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-card-icon'>🏟️</div>
                <h3>Nombre de Stades</h3>
                <h2 class='red-accent'>{len(stades)}</h2>
            </div>""",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-card-icon'>👥</div>
                <h3>Capacité Totale</h3>
                <h2>{total_capacity:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-card-icon'>📊</div>
                <h3>Capacité Moyenne</h3>
                <h2>{avg_capacity:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "capacite" in stades.columns and len(stades) > 0:
        col_biggest, col_smallest = st.columns(2)
        
        biggest_stadium = stades.loc[stades['capacite'].idxmax()]
        smallest_stadium = stades.loc[stades['capacite'].idxmin()]
        
        with col_biggest:
          st.markdown(f"""
        <div class='info-box'>
            <h3 style='margin: 0 0 0.5rem 0; color: #1A472A;'>🏆 Plus Grand Stade</h3>
            <p style='margin: 0; font-weight: 700; font-size: 1.2rem; color: #C1272D;'>
                {biggest_stadium['stade']} — {biggest_stadium['ville']}
            </p>
            <p style='margin: 0.25rem 0 0 0; color: #6C757D;'>
                Capacité : {int(biggest_stadium['capacite']):,} places
            </p>
        </div>
    """, unsafe_allow_html=True)

        
        with col_smallest:
          st.markdown(f"""
        <div class='highlight-box'>
            <h3 style='margin: 0 0 0.5rem 0; color: #C1272D;'>📍 Plus Petit Stade</h3>
            <p style='margin: 0; font-weight: 700; font-size: 1.2rem; color: #1A472A;'>
                {smallest_stadium['stade']} — {smallest_stadium['ville']}
            </p>
            <p style='margin: 0.25rem 0 0 0; color: #6C757D;'>
                Capacité : {int(smallest_stadium['capacite']):,} places
            </p>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("""
        <div class='section-title'>
            <h3>🗺️ Liste complète des stades</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(stades, use_container_width=True, height=400, hide_index=True)
    
    st.markdown("""
        <div class='info-box'>
            <p style='margin: 0; color: #1A472A; font-weight: 600;'>
                ℹ️ Tous les stades répondent aux normes internationales de la CAF
            </p>
        </div>
    """, unsafe_allow_html=True)