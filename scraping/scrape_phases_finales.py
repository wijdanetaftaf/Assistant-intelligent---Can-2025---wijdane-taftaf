import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import re

URL = "https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025"
HEADERS = {"User-Agent": "Mozilla/5.0"}

DATA_DIR = Path(r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data")
DATA_DIR.mkdir(exist_ok=True)

PHASES = {
    "Huitièmes de finale": "Huitièmes_de_finale",
    "Quarts de finale": "Quarts_de_finale",
    "Demi-finale": "Demi-finale",
    "Finale": "Finale"
}

soup = BeautifulSoup(requests.get(URL, headers=HEADERS).text, "html.parser")
matchs = []

for phase, phase_id in PHASES.items():

    h4 = soup.find("h4", id=phase_id)
    if not h4:
        print(f"Phase '{phase}' introuvable")
        continue

    tables = []
    for el in h4.parent.find_next_siblings():
        if el.find("h4"):
            break
        if el.name == "table" and el.get("width") == "100%":
            tables.append(el)

    for table in tables:
        rows = table.find_all("tr")

        for i, row in enumerate(rows):

            time_tag = row.find("time")
            if not time_tag:
                continue

            date = time_tag.get_text(strip=True)
            heure = ""
            for t in row.stripped_strings:
                if re.match(r"\d{1,2}h\d{2}", t):
                    heure = t
                    break

            equipe1 = equipe2 = ""
            stade = ""

            for prev in reversed(rows[:i]):
                teams = prev.find_all("span", class_="nowrap")
                if len(teams) >= 2:
                    equipe1 = teams[0].get_text(strip=True)
                    equipe2 = teams[1].get_text(strip=True)

                    tds = prev.find_all("td")
                    if tds:
                        links = tds[-1].find_all("a")
                        stade = ", ".join(a.get_text(strip=True) for a in links)

                    break

            if not equipe1 or not equipe2:
                continue

            matchs.append({
                "phase": phase,
                "date": date,
                "heure": heure,
                "equipe1": equipe1,
                "equipe2": equipe2,
                "score": "",
                "stade": stade
            })

df = pd.DataFrame(matchs)
df.to_csv(DATA_DIR / "phases_finales_matchs.csv", index=False, encoding="utf-8-sig")

print("phases_finales_matchs.csv généré correctement")
print(f"Matchs : {len(df)}")
