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

classement = []

for lettre in ["A", "B", "C", "D", "E", "F"]:
    h4 = soup.find("h4", id=f"Groupe_{lettre}")
    if not h4:
        print(f"Groupe {lettre} introuvable")
        continue

    table = h4.find_next("table", class_="wikitable")
    if not table:
        print(f"⚠ Table classement introuvable pour groupe {lettre}")
        continue

    rows = table.find_all("tr", class_="notheme")

    for row in rows:
        cells = row.find_all(["th", "td"])
        if len(cells) != 10:
            continue

        equipe = cells[1].get_text(strip=True)
        equipe = re.sub(r"H$", "", equipe)  

        classement.append({
            "groupe": lettre,
            "rang": cells[0].get_text(strip=True),
            "equipe": equipe,
            "pts": cells[2].get_text(strip=True),
            "joues": cells[3].get_text(strip=True),
            "gagnes": cells[4].get_text(strip=True),
            "nuls": cells[5].get_text(strip=True),
            "perdus": cells[6].get_text(strip=True),
            "bp": cells[7].get_text(strip=True),
            "bc": cells[8].get_text(strip=True),
            "diff": cells[9].get_text(strip=True)
        })

df_classement = pd.DataFrame(classement)

df_classement.to_csv(
    r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\classement_groupes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("classement_groupes.csv généré correctement")
print(f"Lignes : {len(df_classement)}")