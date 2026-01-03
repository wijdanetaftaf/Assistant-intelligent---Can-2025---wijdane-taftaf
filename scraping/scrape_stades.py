import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

h2_tags = soup.find_all("h2")

target_h2 = None
for h2 in h2_tags:
    if "Villes et stades" in h2.get_text():
        target_h2 = h2
        break

if not target_h2:
    print("h2 'Villes et stades' introuvable")
    exit()

table = target_h2.find_next("table", class_="wikitable")

if not table:
    print("Table 'Villes et stades' introuvable")
    exit()

stades = []
current_ville = None

rows = table.find_all("tr")[1:]

for row in rows:
    cells = row.find_all(["th", "td"])

    if len(cells) == 3:
        current_ville = cells[0].get_text(strip=True)
        stade = cells[1].get_text(strip=True)
        capacite = cells[2].get_text(strip=True)

    elif len(cells) == 2 and current_ville:
        stade = cells[0].get_text(strip=True)
        capacite = cells[1].get_text(strip=True)

    else:
        continue

    stades.append({
        "ville": current_ville,
        "stade": stade,
        "capacite": capacite
    })

df = pd.DataFrame(stades)

df.to_csv(
    r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\stades.csv",
    index=False,
    encoding="utf-8-sig"
)

print("stades.csv généré avec succès")
