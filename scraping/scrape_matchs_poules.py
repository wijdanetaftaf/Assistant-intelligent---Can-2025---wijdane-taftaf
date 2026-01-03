import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import re

URL = "https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
if response.status_code != 200:
    print("Impossible d'accéder à la page Wikipedia")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

matchs = []

score_regex = re.compile(
    r"([A-Za-zÉéèêôûîïç'\- ]+)\s+(\d+)\s*[–-]\s*(\d+)\s+([A-Za-zÉéèêôûîïç'\- ]+)"
)

for lettre in ["A", "B", "C", "D", "E", "F"]:
    h4 = soup.find("h4", id=f"Groupe_{lettre}")
    if not h4:
        continue

    node = h4

    while True:
        node = node.find_next()
        if node is None:
            break
        if node.name == "h4" and node.get("id", "").startswith("Groupe_"):
            break

        if node.name == "table" and node.get("width") == "100%":
            for tr in node.find_all("tr"):
                text = tr.get_text(" ", strip=True)

                text = re.split(r"\b(Stade|Complexe)\b", text)[0].strip()

                match = score_regex.search(text)
                if not match:
                    continue

                matchs.append({
                    "groupe": lettre,
                    "equipe1": match.group(1).strip(),
                    "equipe2": match.group(4).strip(),
                    "score": f"{match.group(2)}-{match.group(3)}"
                })

df_matchs = pd.DataFrame(matchs).drop_duplicates()

df_matchs.to_csv(
    r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\poules_matchs.csv",
    index=False,
    encoding="utf-8-sig"
)

print("poules_matchs.csv généré correctement")
print(f"Matchs : {len(df_matchs)}")
