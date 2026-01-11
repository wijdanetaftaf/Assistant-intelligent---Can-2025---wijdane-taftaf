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
        return f"Aucune donnée de match disponible pour **{team}**."

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
        return f"Aucun match trouvé pour **{team}**."

    result = f"⚽ Matchs de {team} :\n\n"
    for m in matchs:
        adversaire = m['eq2'] if m['eq1'] == team else m['eq1']
        result += f"**{team}** vs **{adversaire}**\n"
        if m['score'] != 'À venir':
            result += f"   Score : {m['score']}\n"
        if m['date']:
            result += f"   📆 {m['date']} à {m['heure']}\n"
        result += f"   🏆 {m['phase']}\n\n"

    return result.strip()


def score_match(query):
    """
    Trouve le score d'un match entre deux équipes
    Optimisé avec recherche vectorisée
    """
    query_norm = normalize_text(query)

    # Recherche dans les poules
    if not poules.empty:
        for idx, match in poules.iterrows():
            eq1 = normalize_text(match["equipe1"])
            eq2 = normalize_text(match["equipe2"])
            if (eq1 in query_norm and eq2 in query_norm):
                return f"⚽ {match['equipe1']} **{match['score']}** {match['equipe2']}"

    # Recherche dans les finales
    if not finales.empty:
        for idx, match in finales.iterrows():
            eq1 = normalize_text(match["equipe1"])
            eq2 = normalize_text(match["equipe2"])
            if (eq1 in query_norm and eq2 in query_norm):
                score = match.get('score', 'Match à venir')
                return f"⚽ {match['equipe1']} **{score}** {match['equipe2']}"

    return "Je n'ai pas trouvé ce match. Vérifie les noms d'équipes ! 😊"


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
        result += f"{emoji} **{r['equipe']}** — {r['pts']} pts (diff: {r['diff']:+d})\n"

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

    return f"📋 **{team}** est dans le **Groupe {groupe}**\n👥 Avec : {', '.join(autres)}"


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
        f"📊 Classement de **{team}**\n"
        f"{emoji} Position : **{r['rang']}ème** (Groupe {r['groupe']})\n"
        f"⭐ Points : **{r['pts']}**\n"
        f"⚖️ Différence : **{r['diff']:+d}**"
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

    result = f"👥 Effectif de **{team}** ({total} joueurs)\n\n"
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
        result += f"   ⚽ **{m['equipe1']}** vs **{m['equipe2']}**\n"
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
        result += f"📍 **{ville}**\n"
        for s in liste:
            result += f"   • {s['nom']} — {s['capacite']:,} places\n".replace(',', ' ')
        result += "\n"

    return result.strip()


def smart_intent(query):
    """
    Détecte l'intention de l'utilisateur
    Retourne (action, donnée)
    """
    q = normalize_text(query)
    team = find_team(query)
    groupe = find_groupe(query)

    # Matchs d'une équipe
    if team and any(w in q for w in [
        'tous les matchs', 'tous les match',
        'liste des matchs', 'donne moi les matchs',
        'matchs du', 'match du'
    ]):
        return ('matchs_equipe', team)

    if team and any(w in q for w in ['premier', 'leader']) and 'groupe' in q:
        return ('classement', team)

    if any(w in q for w in ['joue quand', 'quand joue', 'prochain match', 'calendrier',
                            'programme', 'qui affronte', 'contre qui', 'adversaire', 'rencontre']):
        if team:
            return ('matchs_equipe', team)

    # Score
    if any(w in q for w in ['score', 'resultat', 'vs', 'contre']) and not any(w in q for w in ['quand', 'prochain']):
        return ('score', None)

    # Équipes d'un groupe
    if groupe and any(w in q for w in ['equipes', 'qui', 'liste', 'quelles', 'composition']):
        return ('equipes_groupe', groupe)

    # Classement d'un groupe
    if groupe and any(w in q for w in ['classement', 'premier', 'leader', 'points', 'qui est']):
        return ('classement_groupe_complet', groupe)

    # Groupe d'une équipe
    if 'groupe' in q and team and not any(w in q for w in ['classement', 'premier']):
        return ('groupe', team)

    # Classement d'une équipe
    if any(w in q for w in ['classement', 'position', 'rang', 'points', 'difference', 'buts']) and team:
        return ('classement', team)

    # Joueurs
    if any(w in q for w in ['joueur', 'effectif', 'composition', 'selection', 'roster', 'equipe']) and team:
        if 'groupe' not in q:
            return ('joueurs', team)

    # Phases finales
    phases = {
        'quart': 'Quarts',
        'demi': 'Demi',
        'finale': 'Finale',
        'huitieme': 'Huitième',
        'huit': 'Huitième'
    }
    for kw, phase in phases.items():
        if kw in q:
            return ('phase', phase)

    # Stades
    if any(w in q for w in ['stade', 'stades', 'lieu', 'capacite']):
        return ('stades', None)

    return ('conversation', None)


def chatbot(query):
    """
    Point d'entrée principal du chatbot
    Avec gestion d'erreurs améliorée
    """
    if not query or not query.strip():
        return "💭 Pose-moi une question sur la CAN 2025 !"

    query = query.strip()
    q_norm = normalize_text(query)

    # Conversations générales
    conv_kw = ['bonjour', 'salut', 'hello', 'merci', 'qui es tu', 'aide', 'ca va', 'cava']
    if any(kw in q_norm for kw in conv_kw):
        return talk(query)

    try:
        intent, data = smart_intent(query)

        if intent == 'matchs_equipe':
            return matchs_equipe(data)
        elif intent == 'score':
            return score_match(query)
        elif intent == 'equipes_groupe':
            return equipes_du_groupe(data)
        elif intent == 'classement_groupe_complet':
            return classement_complet_groupe(data)
        elif intent == 'groupe':
            return group_of_team(data)
        elif intent == 'classement':
            return classement_groupe(data)
        elif intent == 'joueurs':
            return joueurs_equipe(data)
        elif intent == 'phase':
            return matchs_phase(data)
        elif intent == 'stades':
            return liste_stades()
        else:
            return talk(query)

    except Exception as e:
        logger.error(f"Erreur chatbot: {e}")
        return "Désolé, une erreur s'est produite. Peux-tu reformuler ta question ? 😊"


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
