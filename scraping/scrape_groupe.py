import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
if response.status_code != 200:
    print("Impossible d'accéder à la page Wikipedia")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

groupes = []

for lettre in ["A", "B", "C", "D", "E", "F"]:
    h4 = soup.find("h4", id=f"Groupe_{lettre}")
    if not h4:
        print(f"Groupe {lettre} introuvable")
        continue

    table = h4.find_next("table", class_="wikitable")
    if not table:
        print(f"Table du groupe {lettre} introuvable")
        continue

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        equipe = cols[1].get_text(strip=True).replace("H", "")


        groupes.append({
            "groupe": lettre,
            "equipe": equipe
        })

df_groupes = pd.DataFrame(groupes)

df_groupes.to_csv(
    r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\groupes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("groupes.csv généré correctement")
print(f"Lignes : {len(df_groupes)}")