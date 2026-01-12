import pandas as pd
import re
from datetime import datetime
import random
import logging
from functools import lru_cache
from data_manager import (
    load_poules, load_finales, load_joueurs,
    load_classement, load_groupes, load_stades, load_equipes
)
from llama_router import llama_intent_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement des données avec cache (via data_manager)
poules = load_poules()
finales = load_finales()
joueurs = load_joueurs()
classement = load_classement()
groupes = load_groupes()
stades = load_stades()
equipes = load_equipes()


def talk(user_message):
    """Gère les conversations générales (salutations, aide, etc.)"""
    msg_lower = user_message.lower().strip()

    greetings = {
        'bonjour': ['Bonjour ! 😊', 'Salut ! 👋', 'Hello !'],
        'salut': ['Salut ! 👋', 'Hey ! 😊'],
        'hello': ['Hello ! 👋', 'Hi ! 😊'],
        'bonsoir': ['Bonsoir ! 🌙'],
        'coucou': ['Coucou ! 👋😊'],
    }

    for key, responses in greetings.items():
        if msg_lower.startswith(key):
            return random.choice(responses) + " Que veux-tu savoir sur la CAN 2025 ?"

    if any(p in msg_lower for p in ['ca va', 'cava', 'comment vas', 'tu vas bien']):
        return random.choice([
            "Je vais très bien, merci ! Et toi ?",
            "Super bien ! Des questions sur la CAN ?",
            "Ça roule ! Comment puis-je t'aider ?"
        ])

    if any(w in msg_lower for w in ['merci', 'thanks', 'cool', 'top', 'génial']):
        return random.choice([
            "Avec grand plaisir !",
            "De rien ! N'hésite pas pour d'autres questions !",
            "Content d'avoir pu t'aider !"
        ])

    if any(p in msg_lower for p in ['qui es tu', 'ton rôle', 'tu fais quoi']):
        return "Je suis un assistant IA spécialisé dans la CAN 2025 !\nJe peux t'aider avec les matchs, équipes, joueurs, et plus encore ! 😊"

    if 'aide' in msg_lower or 'aider' in msg_lower:
        return (
            "Bien sûr ! Je suis là pour t'aider !\n\n"
            "Je peux te renseigner sur :\n"
            "• Calendrier des matchs d'une équipe\n"
            "• Scores et résultats\n"
            "• Groupes et équipes\n"
            "• Classements\n"
            "• Joueurs et effectifs\n"
            "• Phases finales\n"
            "• Stades\n\n"
            "Pose-moi une question naturellement ! 😊"
        )

    return random.choice([
        "Hmm, je ne suis pas sûr de comprendre. Pose-moi une question sur la CAN 2025 !",
        "Intéressant ! Que veux-tu savoir sur la CAN 2025 ?",
        "Je peux t'aider avec la CAN 2025 ! Pose ta question !"
    ])


@lru_cache(maxsize=128)
def find_team(text):
    """
    Détecte une équipe dans le texte
    Optimisé avec cache et recherche directe
    """
    text_lower = text.lower()

    team_aliases = {
        "maroc": "Maroc", "morocco": "Maroc",
        "mali": "Mali",
        "sénégal": "Sénégal", "senegal": "Sénégal",
        "algérie": "Algérie", "algerie": "Algérie", "algeria": "Algérie",
        "egypte": "Égypte", "égypte": "Égypte", "egypt": "Égypte",
        "cameroun": "Cameroun", "cameroon": "Cameroun",
        "côte d'ivoire": "Côte D'Ivoire", "cote d'ivoire": "Côte D'Ivoire", "ivoire": "Côte D'Ivoire",
        "nigeria": "Nigeria",
        "afrique du sud": "Afrique Du Sud", "south africa": "Afrique Du Sud",
        "rd congo": "Rd Congo", "rdc": "Rd Congo", "congo": "Rd Congo",
        "benin": "Bénin", "bénin": "Bénin",
        "tunisie": "Tunisie", "tunisia": "Tunisie",
        "burkina faso": "Burkina Faso", "burkina": "Burkina Faso",
        "zambie": "Zambie", "zambia": "Zambie",
        "zimbabwe": "Zimbabwe",
        "tanzanie": "Tanzanie", "tanzania": "Tanzanie",
        "comores": "Comores", "comoros": "Comores",
        "guinée équatoriale": "Guinée Équatoriale", "guinee equatoriale": "Guinée Équatoriale",
        "soudan": "Soudan", "sudan": "Soudan",
        "mozambique": "Mozambique",
        "gabon": "Gabon",
        "ouganda": "Ouganda", "uganda": "Ouganda",
        "ghana": "Ghana",
        "angola": "Angola",
        "botswana": "Botswana"
    }

    # Recherche dans les aliases
    for alias, real_name in team_aliases.items():
        if alias in text_lower:
            return real_name

    # Recherche directe dans la liste des équipes
    for equipe in equipes:
        if equipe.lower() in text_lower:
            return equipe

    return None


def find_groupe(text):
    """Détecte un groupe (A-F) dans le texte"""
    match = re.search(r'\bgroupe\s*([a-f])\b', text.lower())
    if match:
        return match.group(1).upper()
    return None


# Regex compilée pour normalisation (3-5x plus rapide)
ACCENT_PATTERN = re.compile(r'[àáâ]')
ACCENT_E_PATTERN = re.compile(r'[èéê]')
ACCENT_I_PATTERN = re.compile(r'[ìíî]')
ACCENT_O_PATTERN = re.compile(r'[òóô]')
ACCENT_U_PATTERN = re.compile(r'[ùúû]')
WHITESPACE_PATTERN = re.compile(r'\s+')


def normalize_text(text):
    """Normalise le texte (supprime accents et espaces multiples) - Optimisé"""
    text = text.lower()
    text = ACCENT_PATTERN.sub('a', text)
    text = ACCENT_E_PATTERN.sub('e', text)
    text = ACCENT_I_PATTERN.sub('i', text)
    text = ACCENT_O_PATTERN.sub('o', text)
    text = ACCENT_U_PATTERN.sub('u', text)
    text = text.replace('ç', 'c')
    text = WHITESPACE_PATTERN.sub(' ', text)
    return text.strip()


def matchs_equipe(team):
    """
    Retourne tous les matchs d'une équipe
    Optimisé : utilise .isin() au lieu de .iterrows()
    """
    if poules.empty and finales.empty:
        return f"Aucune donnée de match disponible pour {team}."

    matchs = []

    # Recherche optimisée avec isin() au lieu de iterrows()
    if not poules.empty:
        mask = poules['equipe1'].eq(team) | poules['equipe2'].eq(team)
        matches_poules = poules[mask]

        for idx, match in matches_poules.iterrows():
            matchs.append({
                'eq1': match['equipe1'],
                'eq2': match['equipe2'],
                'score': match.get('score', 'À venir'),
                'date': match.get('date', ''),
                'heure': match.get('heure', ''),
                'phase': 'Phase de poules'
            })

    if not finales.empty:
        mask = finales['equipe1'].eq(team) | finales['equipe2'].eq(team)
        matches_finales = finales[mask]

        for idx, match in matches_finales.iterrows():
            matchs.append({
                'eq1': match['equipe1'],
                'eq2': match['equipe2'],
                'score': match.get('score', 'À venir'),
                'date': match.get('date', ''),
                'heure': match.get('heure', ''),
                'phase': match.get('phase', 'Phase finale')
            })

    if not matchs:
        return f"Aucun match trouvé pour {team}."

    result = f"⚽ Matchs de {team} :\n\n"
    for m in matchs:
        adversaire = m['eq2'] if m['eq1'] == team else m['eq1']
        result += f"{team} vs {adversaire}\n"
        if m['score'] != 'À venir':
            result += f"   Score : {m['score']}\n"
        if m['date']:
            result += f"   📆 {m['date']} à {m['heure']}\n"
        result += f"   🏆 {m['phase']}\n\n"

    return result.strip()


def score_match(query):
    q = normalize_text(query)

    team1 = find_team(query)
    if not team1:
        return "Je n'ai pas reconnu les équipes du match."

    # Cherche une 2e équipe différente
    team2 = None
    for eq in equipes:
        if eq != team1 and normalize_text(eq) in q:
            team2 = eq
            break

    if not team2:
        return "Je n'ai pas reconnu les deux équipes du match."

    # Recherche dans poules
    if not poules.empty:
        m = poules[
            ((poules['equipe1'] == team1) & (poules['equipe2'] == team2)) |
            ((poules['equipe1'] == team2) & (poules['equipe2'] == team1))
        ]
        if not m.empty:
            r = m.iloc[0]
            return f"⚽ {r['equipe1']} {r['score']} {r['equipe2']}"

    # Recherche dans finales
    if not finales.empty:
        m = finales[
            ((finales['equipe1'] == team1) & (finales['equipe2'] == team2)) |
            ((finales['equipe1'] == team2) & (finales['equipe2'] == team1))
        ]
        if not m.empty:
            r = m.iloc[0]
            score = r['score'] if r['score'] else "Match à venir"
            return f"⚽ {r['equipe1']} {score} {r['equipe2']}"

    return f"Aucun match trouvé entre {team1} et {team2}."



def equipes_du_groupe(groupe_lettre):
    """Liste les équipes d'un groupe"""
    if groupes.empty:
        return f"Données de groupes non disponibles."

    equipes_groupe = groupes[groupes["groupe"] == groupe_lettre]["equipe"].tolist()

    if not equipes_groupe:
        return f"Groupe {groupe_lettre} non trouvé."

    return f"📋 Groupe {groupe_lettre} :\n   • " + "\n   • ".join(equipes_groupe)


def classement_complet_groupe(groupe_lettre):
    """Affiche le classement complet d'un groupe"""
    if classement.empty:
        return f"Classement du groupe {groupe_lettre} non disponible."

    rows = classement[classement["groupe"] == groupe_lettre].sort_values('rang')

    if rows.empty:
        return f"Classement du groupe {groupe_lettre} non disponible."

    result = f"🏆 Classement Groupe {groupe_lettre} :\n\n"
    for idx, r in rows.iterrows():
        emoji = ["🥇", "🥈", "🥉", "4️⃣"][min(r['rang']-1, 3)]
        result += f"{emoji} {r['equipe']} — {r['pts']} pts (diff: {r['diff']:+d})\n"

    return result


def group_of_team(team):
    """Trouve le groupe d'une équipe"""
    if groupes.empty:
        return f"Données de groupes non disponibles."

    groupe_info = groupes[groupes["equipe"] == team]

    if groupe_info.empty:
        return f"Groupe de {team} non trouvé."

    groupe = groupe_info.iloc[0]['groupe']
    autres = groupes[groupes["groupe"] == groupe]["equipe"].tolist()

    if team in autres:
        autres.remove(team)

    return f"📋 {team} est dans le Groupe {groupe}\n👥 Avec : {', '.join(autres)}"


def classement_groupe(team):
    """Affiche le classement d'une équipe dans son groupe"""
    if classement.empty:
        return f"Classement de {team} non disponible."

    row = classement[classement["equipe"] == team]

    if row.empty:
        return f"Classement de {team} non disponible."

    r = row.iloc[0]
    emoji = ["🥇", "🥈", "🥉", "4️⃣"][min(r['rang']-1, 3)]

    return (
        f"📊 Classement de {team}\n"
        f"{emoji} Position : {r['rang']}ème (Groupe {r['groupe']})\n"
        f"⭐ Points : {r['pts']}\n"
        f"⚖️ Différence : {r['diff']:+d}"
    )


def joueurs_equipe(team):
    """Liste les joueurs d'une équipe - Affiche TOUS les joueurs"""
    if joueurs.empty:
        return f"Données de joueurs non disponibles."

    j = joueurs[joueurs["equipe"].str.lower() == team.lower()]

    if j.empty:
        j = joueurs[joueurs["equipe"].str.lower().str.contains(team.lower(), na=False)]

    if j.empty:
        return f"Joueurs de {team} non trouvés."

    total = len(j)
    liste = j["joueur"].tolist()  # TOUS les joueurs maintenant

    result = f"👥 Effectif de {team} ({total} joueurs)\n\n"
    result += "\n".join([f"   • {joueur}" for joueur in liste])

    return result


def matchs_phase(phase):
    """Liste les matchs d'une phase finale"""
    if finales.empty:
        return f"Aucun match de phase finale disponible."

    matchs = finales[finales["phase"].str.contains(phase, case=False, na=False)]

    if matchs.empty:
        return f"Aucun match trouvé pour {phase}."

    result = f"🏆 {phase.title()} :\n\n"
    for idx, m in matchs.iterrows():
        result += f"   ⚽ {m['equipe1']} vs {m['equipe2']}\n"
        result += f"   📅 {m['date']} à {m['heure']}\n\n"

    return result.strip()


def liste_stades():
    """Liste tous les stades de la CAN 2025"""
    if stades.empty:
        return "Données de stades non disponibles."

    stades_ville = {}

    for idx, row in stades.iterrows():
        ville = row['ville']
        if ville not in stades_ville:
            stades_ville[ville] = []

        stades_ville[ville].append({
            'nom': row['stade'],
            'capacite': row['capacite']
        })

    result = "🏟️ Stades de la CAN 2025 :\n\n"
    for ville, liste in stades_ville.items():
        result += f"📍 {ville}\n"
        for s in liste:
            result += f"   • {s['nom']} — {s['capacite']:,} places\n".replace(',', ' ')
        result += "\n"

    return result.strip()


INTENT_HANDLERS = {
    "matchs_equipe": matchs_equipe,
    "score": score_match,
    "joueurs": joueurs_equipe,
    "classement": classement_groupe,
    "equipes_groupe": equipes_du_groupe,
    "groupe": group_of_team,
    "stades": lambda _: liste_stades(),
    "phase": matchs_phase
}

def chatbot(query: str) -> str:
    if not query.strip():
        return "💭 Pose-moi une question sur la CAN 2025 !"

    q_norm = normalize_text(query)

    # ======================
    # 1️⃣ SALUTATIONS
    # ======================
    if any(w in q_norm for w in ["bonjour", "salut", "hello", "merci", "aide"]):
        return talk(query)

    # ======================
    # 2️⃣ RÈGLES DIRECTES (FIABLES)
    # ======================
    team = find_team(query)
    groupe = find_groupe(query)

    joueurs_kw = ["joueur", "joueurs", "effectif", "selection", "sélection", "liste"]
    if team and any(k in q_norm for k in joueurs_kw):
        return joueurs_equipe(team)

    if team and any(k in q_norm for k in ["match", "joue", "quand"]):
        return matchs_equipe(team)

    if "score" in q_norm or "resultat" in q_norm:
        return score_match(query)

    if "classement" in q_norm and team:
        return classement_groupe(team)

    if groupe and "classement" in q_norm:
        return classement_complet_groupe(groupe)

    if "stade" in q_norm:
        return liste_stades()

    if "demi" in q_norm:
        return matchs_phase("Demi")
    if "quart" in q_norm:
        return matchs_phase("Quart")
    if "finale" in q_norm:
        return matchs_phase("Finale")

    # ======================
    # 3️⃣ LLaMA (AMBIGU)
    # ======================
    parsed = llama_intent_router(query)

    intent = parsed.get("intent")
    team_llm = parsed.get("team")
    groupe_llm = parsed.get("groupe")
    phase_llm = parsed.get("phase")

    if intent == "conversation":
        return talk(query)

    if intent == "joueurs" and team_llm:
        return joueurs_equipe(team_llm)

    if intent == "matchs_equipe" and team_llm:
        return matchs_equipe(team_llm)

    if intent == "score":
        return score_match(query)

    if intent == "classement" and team_llm:
        return classement_groupe(team_llm)

    if intent == "equipes_groupe" and groupe_llm:
        return equipes_du_groupe(groupe_llm)

    if intent == "phase" and phase_llm:
        return matchs_phase(phase_llm)

    if intent == "stades":
        return liste_stades()

    # ======================
    # 4️⃣ FALLBACK FINAL
    # ======================
    if team:
        return f"🤔 Que veux-tu savoir exactement sur {team} ?"

    return "🤔 Je n’ai pas compris. Peux-tu reformuler ?"



def ask_bot(question):
    """Interface publique pour l'application Streamlit"""
    return chatbot(question)


if __name__ == "__main__":
    print("🤖 CHATBOT CAN 2025 - Assistant Intelligent (Version Optimisée)")
    print("💬 Pose-moi des questions naturellement sur la CAN 2025 !")
    print("👉 Tape 'exit' pour quitter\n")

    while True:
        try:
            user_input = input("Toi : ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "quitter", "bye"]:
                print("\n👋 À bientôt ! Bonne CAN 2025 ! ⚽✨")
                break

            response = chatbot(user_input)
            print(f"\n🤖 Bot : {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 À bientôt !")
            break
        except Exception as e:
            logger.error(f"Erreur: {e}")
            print(f"\n❌ Erreur : {e}\n")
