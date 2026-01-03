import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRAPING_DIR = BASE_DIR / "scraping"

def run(script_name, description=""):
    print(f"\nExécution : {script_name}")
    if description:
        print(f"   ℹ {description}")

    script_path = SCRAPING_DIR / script_name

    if not script_path.exists():
        print(f"Fichier introuvable : {script_path}")
        return

    exit_code = os.system(f'python "{script_path}"')

    if exit_code != 0:
        print(f"{script_name} exécuté sans données ou non disponible (normal)")
    else:
        print(f"{script_name} exécuté avec succès")

run(
    "scrape_matchs_poules.py",
    "Matchs & résultats de la phase de poules"
)

run(
    "scrape_phases_finales.py",
    "Huitièmes, Quarts, Demi-finales, Finale (si disponibles)"
)

run(
    "scrape_joueurs.py",
    "Listes des joueurs par équipe"
)
