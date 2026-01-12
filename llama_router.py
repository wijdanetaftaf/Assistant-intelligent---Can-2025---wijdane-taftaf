import subprocess
import json
import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

MODEL_NAME = "llama3"
TIMEOUT = 20

SYSTEM_PROMPT = """
Tu es un classificateur d’intention pour un chatbot sur la CAN 2025.

RÈGLES STRICTES :
- Réponds UNIQUEMENT par un JSON valide
- Aucun texte avant ou après
- Pas de commentaires
- Pas de markdown

FORMAT STRICT :
{
  "intent": "matchs_equipe | score | joueurs | classement | groupe | stades | phase | conversation",
  "team": "Nom de l’équipe ou null",
  "groupe": "Lettre A-F ou null",
  "phase": "Huitième | Quart | Demi | Finale | null"
}

EXEMPLES :

Question: donne moi l'effectif du mali
{"intent":"joueurs","team":"Mali","groupe":null,"phase":null}

Question: où se joue la demi finale
{"intent":"phase","team":null,"groupe":null,"phase":"Demi"}

Question: bonjour
{"intent":"conversation","team":null,"groupe":null,"phase":null}

Question utilisateur :
"""


VALID_INTENTS = {
    "matchs_equipe",
    "score",
    "joueurs",
    "classement",
    "groupe",
    "stades",
    "phase",
    "conversation"
}

VALID_PHASES = {"Huitième", "Quart", "Demi", "Finale"}


def _safe_json_extract(text: str) -> Dict:
    """
    Extrait un JSON valide depuis la sortie LLaMA
    """
    match = re.search(r"\{[\s\S]*?\}", text)
    if not match:
        raise ValueError("Aucun JSON détecté dans la réponse LLaMA")

    return json.loads(match.group())


def llama_intent_router(question: str) -> Dict[str, Optional[str]]:
    """
    Analyse la question utilisateur via LLaMA 3 (local)
    Retourne toujours un dictionnaire sûr
    """
    if not question or not question.strip():
        return _fallback()

    try:
        proc = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=SYSTEM_PROMPT + question.strip(),
            text=True,
            capture_output=True,
            timeout=TIMEOUT
        )

        if proc.returncode != 0:
            logger.error(f"Ollama error: {proc.stderr}")
            return _fallback()

        raw_output = proc.stdout.strip()

        data = _safe_json_extract(raw_output)

        intent = data.get("intent", "inconnu")
        team = data.get("team")
        groupe = data.get("groupe")
        phase = data.get("phase")

        # 🔒 Sécurisation des valeurs
        if intent not in VALID_INTENTS:
            intent = "inconnu"

        if phase not in VALID_PHASES:
            phase = None

        if groupe:
            groupe = groupe.upper()
            if groupe not in {"A", "B", "C", "D", "E", "F"}:
                groupe = None

        return {
            "intent": intent,
            "team": team,
            "groupe": groupe,
            "phase": phase
        }

    except subprocess.TimeoutExpired:
        logger.error("LLaMA timeout")
        return _fallback()

    except Exception as e:
        logger.error(f"LLaMA parsing error: {e}")
        return _fallback()


def _fallback() -> Dict[str, Optional[str]]:
    """
    Réponse de secours garantie
    """
    return {
        "intent": "inconnu",
        "team": None,
        "groupe": None,
        "phase": None
    }
