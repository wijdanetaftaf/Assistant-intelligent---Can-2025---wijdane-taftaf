import pandas as pd
import re
from datetime import datetime
import random


poules = pd.read_csv("data/poules_matchs.csv")
finales = pd.read_csv("data/phases_finales_matchs.csv")
joueurs = pd.read_csv("data/joueurs_brut.csv")
classement = pd.read_csv("data/classement_groupes.csv")
groupes = pd.read_csv("data/groupes.csv")
stades = pd.read_csv("data/stades.csv")
equipes = pd.read_csv("data/equipes.csv")["equipe"].tolist()


conversation_history = []
last_team_mentioned = None


def talk(user_message):
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
            "Super bien !  Des questions sur la CAN ?",
            "Ça roule !  Comment puis-je t'aider ?"
        ])
    
    if any(w in msg_lower for w in ['merci', 'thanks', 'cool', 'top', 'génial']):
        return random.choice([
            "Avec grand plaisir ! ",
            "De rien ! N'hésite pas pour d'autres questions ! ",
            "Content d'avoir pu t'aider ! "
        ])
    
    if any(p in msg_lower for p in ['qui es tu', 'ton rôle', 'tu fais quoi']):
        return "Je suis un assistant IA spécialisé dans la CAN 2025 ! \nJe peux t'aider avec les matchs, équipes, joueurs, et plus encore ! 😊"
    
    if 'aide' in msg_lower or 'aider' in msg_lower:
        return (
            "Bien sûr ! Je suis là pour t'aider ! \n\n"
            "Je peux te renseigner sur :\n"
            "Calendrier des matchs d'une équipe\n"
            "Scores et résultats\n"
            "Groupes et équipes\n"
            "Classements\n"
            "Joueurs et effectifs\n"
            "Phases finales\n"
            "Stades\n\n"
            "Pose-moi une question naturellement ! 😊"
        )
    
    return random.choice([
        "Hmm, je ne suis pas sûr de comprendre. Pose-moi une question sur la CAN 2025 ! ",
        "Intéressant ! Que veux-tu savoir sur la CAN 2025 ? ",
        "Je peux t'aider avec la CAN 2025 ! Pose ta question ! "
    ])

def find_team(text):
    text_lower = text.lower()
    
    team_aliases = {
        "maroc": "Maroc", "morocco": "Maroc",
        "mali": "Mali",
        "sénégal": "Sénégal", "senegal": "Sénégal",
        "algérie": "Algérie", "algerie": "Algérie", "algeria": "Algérie",
        "egypte": "Égypte", "égypte": "Égypte", "egypt": "Égypte",
        "cameroun": "Cameroun", "cameroon": "Cameroun",
        "côte d'ivoire": "Côte d'Ivoire", "cote d'ivoire": "Côte d'Ivoire", "ivoire": "Côte d'Ivoire",
        "nigeria": "Nigeria",
        "afrique du sud": "Afrique du Sud", "south africa": "Afrique du Sud",
        "rd congo": "RD Congo", "rdc": "RD Congo", "congo": "RD Congo",
        "benin": "Bénin", "bénin": "Bénin",
        "tunisie": "Tunisie", "tunisia": "Tunisie",
        "burkina faso": "Burkina Faso", "burkina": "Burkina Faso",
        "zambie": "Zambie", "zambia": "Zambie",
        "zimbabwe": "Zimbabwe",
        "tanzanie": "Tanzanie", "tanzania": "Tanzanie",
        "comores": "Comores", "comoros": "Comores",
        "guinée équatoriale": "Guinée équatoriale", "guinee equatoriale": "Guinée équatoriale",
        "soudan": "Soudan", "sudan": "Soudan",
        "mozambique": "Mozambique",
        "gabon": "Gabon",
        "ouganda": "Ouganda", "uganda": "Ouganda",
        "ghana": "Ghana",
        "angola": "Angola",
        "botswana": "Botswana"
    }
    
    for alias, real_name in team_aliases.items():
        if alias in text_lower:
            return real_name
    
    for equipe in equipes:
        if equipe.lower() in text_lower:
            return equipe
    
    return None


def find_groupe(text):
    match = re.search(r'\bgroupe\s*([a-f])\b', text.lower())
    if match:
        return match.group(1).upper()
    return None


def normalize_text(text):
    text = text.lower()
    replacements = {
        'à': 'a', 'á': 'a', 'â': 'a', 'è': 'e', 'é': 'e', 'ê': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ò': 'o', 'ó': 'o', 'ô': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ç': 'c'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r'\s+', ' ', text).strip()


def clean_number(value):
    if pd.isna(value):
        return 0
    value_str = str(value).replace('\xa0', '').replace(' ', '').replace(',', '')
    try:
        return int(float(value_str))
    except:
        return 0

def matchs_equipe(team):
    matchs = []
    
    for _, match in poules.iterrows():
        if team in [match["equipe1"], match["equipe2"]]:
            matchs.append({
                'eq1': match['equipe1'],
                'eq2': match['equipe2'],
                'score': match.get('score', 'À venir'),
                'date': match.get('date', ''),
                'heure': match.get('heure', ''),
                'phase': 'Phase de poules'
            })
    
    for _, match in finales.iterrows():
        if team in [match["equipe1"], match["equipe2"]]:
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
    
    result = f"Matchs de {team} :\n\n"
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
    query_norm = normalize_text(query)
    
    for _, match in poules.iterrows():
        eq1 = normalize_text(match["equipe1"])
        eq2 = normalize_text(match["equipe2"])
        if (eq1 in query_norm and eq2 in query_norm):
            return f"{match['equipe1']} {match['score']} {match['equipe2']}"
    
    for _, match in finales.iterrows():
        eq1 = normalize_text(match["equipe1"])
        eq2 = normalize_text(match["equipe2"])
        if (eq1 in query_norm and eq2 in query_norm):
            score = match.get('score', 'Match à venir')
            return f"⚽ {match['equipe1']} {score} {match['equipe2']}"
    
    return "Je n'ai pas trouvé ce match. Vérifie les noms ! 😊"


def equipes_du_groupe(groupe_lettre):
    equipes_groupe = groupes[groupes["groupe"] == groupe_lettre]["equipe"].tolist()
    
    if not equipes_groupe:
        return f"Groupe {groupe_lettre} non trouvé."
    
    return f"Groupe {groupe_lettre} :\n   • " + "\n   • ".join(equipes_groupe)


def classement_complet_groupe(groupe_lettre):
    rows = classement[classement["groupe"] == groupe_lettre].sort_values('rang')
    
    if rows.empty:
        return f"Classement du groupe {groupe_lettre} non disponible."
    
    result = f"Classement Groupe {groupe_lettre} :\n\n"
    for _, r in rows.iterrows():
        emoji = ["🥇", "🥈", "🥉", "4️⃣"][min(r['rang']-1, 3)]
        result += f"{emoji} {r['equipe']} — {r['pts']} pts (diff: {r['diff']:+d})\n"

    return result


def group_of_team(team):
    global last_team_mentioned
    last_team_mentioned = team
    
    groupe_info = groupes[groupes["equipe"] == team]
    if groupe_info.empty:
        return f"Groupe de {team} non trouvé."
    
    groupe = groupe_info.iloc[0]['groupe']
    autres = groupes[groupes["groupe"] == groupe]["equipe"].tolist()
    autres.remove(team)
    
    return f"{team} est dans le Groupe {groupe}\n📋 Avec : {', '.join(autres)}"


def classement_groupe(team):
    global last_team_mentioned
    last_team_mentioned = team
    
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
    global last_team_mentioned
    last_team_mentioned = team
    
    j = joueurs[joueurs["equipe"].str.lower() == team.lower()]
    
    if j.empty:
        j = joueurs[joueurs["equipe"].str.lower().str.contains(team.lower(), na=False)]
    
    if j.empty:
        return f"Joueurs de {team} non trouvés."
    
    total = len(j)
    liste = j["joueur"].head(15).tolist()

    result = f"👥 Effectif de {team} ({total} joueurs)\n\n"
    result += "\n".join([f"   • {joueur}" for joueur in liste])
    
    if total > 15:
        result += f"\n\n   ... et {total - 15} autres"
    
    return result


def matchs_phase(phase):
    matchs = finales[finales["phase"].str.contains(phase, case=False, na=False)]
    
    if matchs.empty:
        return f"Aucun match trouvé pour {phase}."

    result = f"🏆 {phase.title()} :\n\n"
    for _, m in matchs.iterrows():
        result += f"   ⚽ {m['equipe1']} vs {m['equipe2']}\n"
        result += f"   📅 {m['date']} à {m['heure']}\n\n"
    
    return result.strip()


def liste_stades():
    stades_ville = {}
    
    for _, row in stades.iterrows():
        ville = row['ville']
        if ville not in stades_ville:
            stades_ville[ville] = []
        
        cap = clean_number(row['capacite'])
        stades_ville[ville].append({'nom': row['stade'], 'capacite': cap})
    
    result = "🏟️ Stades de la CAN 2025 :\n\n"
    for ville, liste in stades_ville.items():
        result += f"📍 {ville}\n"
        for s in liste:
            result += f"   • {s['nom']} — {s['capacite']:,} places\n".replace(',', ' ')
        result += "\n"
    
    return result.strip()


def smart_intent(query):
    q = normalize_text(query)
    team = find_team(query)
    groupe = find_groupe(query)
    
    if team and any(w in q for w in [
             'tous les matchs', 'tous les match',
            'liste des matchs', 'donne moi les matchs',
           'matchs du', 'match du'
       ]):
        return ('matchs_equipe', team)
    
    if team and any(w in q for w in ['premier', 'leader']) and 'groupe' in q:
           return ('classement', team)

    if any(w in q for w in ['joue quand','quand joue', 'prochain match', 'calendrier', 'programme', 'qui affronte', 'contre qui', 'adversaire', 'rencontre']):
        if team:
            return ('matchs_equipe', team)
    
    if any(w in q for w in ['score', 'resultat', 'vs', 'contre']) and not any(w in q for w in ['quand', 'prochain']):
        return ('score', None)
    
    if groupe and any(w in q for w in ['equipes', 'qui', 'liste', 'quelles', 'composition']):
        return ('equipes_groupe', groupe)
    
    if groupe and any(w in q for w in ['classement', 'premier', 'leader', 'points', 'qui est']):
        return ('classement_groupe_complet', groupe)
    
    if 'groupe' in q and team and not any(w in q for w in ['classement', 'premier']):
        return ('groupe', team)
    
    if any(w in q for w in ['classement', 'position', 'rang', 'points', 'difference', 'buts']) and team:
        return ('classement', team)
    
    if any(w in q for w in ['joueur', 'effectif', 'composition', 'selection', 'roster', 'equipe']) and team:
        # Vérifier que ce n'est pas une question sur le groupe
        if 'groupe' not in q:
            return ('joueurs', team)
    
    phases = {'quart': 'Quarts', 'demi': 'Demi', 'finale': 'Finale', 'huitieme': 'Huitième', 'huit': 'Huitième'}
    for kw, phase in phases.items():
        if kw in q:
            return ('phase', phase)
    
    if any(w in q for w in ['stade', 'stades', 'lieu', 'capacite']):
        return ('stades', None)
    
    return ('conversation', None)



def chatbot(query):
    if not query or not query.strip():
        return "💭 Pose-moi une question sur la CAN 2025 !"
    
    query = query.strip()
    q_norm = normalize_text(query)
    
    conv_kw = ['bonjour', 'salut', 'hello', 'merci', 'qui es tu', 'aide', 'ca va', 'cava']
    if any(kw in q_norm for kw in conv_kw):
        return talk(query)
    
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



if __name__ == "__main__":
    print("🤖 CHATBOT CAN 2025 - Assistant Intelligent")
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
            print(f"\n Erreur : {e}\n")
def ask_bot(question):
    return chatbot(question)
