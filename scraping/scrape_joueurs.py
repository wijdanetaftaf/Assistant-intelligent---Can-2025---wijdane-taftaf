import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations_squads"
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

joueurs = []

def is_player_table(df):
    required = {"No.", "Pos.", "Player"}
    return required.issubset(set(df.columns))

h3_tags = soup.find_all("h3")

for i, h3 in enumerate(h3_tags):
    equipe = h3.get_text(strip=True)

    next_h3 = h3_tags[i + 1] if i + 1 < len(h3_tags) else None
    node = h3

    while True:
        node = node.find_next()
        if node is None or node == next_h3:
            break

        if node.name == "table" and "wikitable" in node.get("class", []):
            dfs = pd.read_html(str(node))
            if not dfs:
                continue

            df = dfs[0]

            if not is_player_table(df):
                continue

            # Nettoyage joueur
            df = df.dropna(subset=["Player"])
            df["Player"] = (
                df["Player"]
                .astype(str)
                .str.replace(r"\(.*?\)", "", regex=True)
                .str.strip()
            )

            for _, row in df.iterrows():
                joueurs.append({
                    "joueur": row.get("Player", ""),
                    "equipe": equipe,
                    "poste": row.get("Pos.", ""),
                    "date_naissance": row.get("Date of birth (age)", ""),
                    "club": row.get("Club", ""),
                    "goals": int(row["Goals"]) if "Goals" in df.columns and pd.notna(row["Goals"]) else 0
                })

            break  

df_joueurs = pd.DataFrame(joueurs)

df_joueurs.to_csv(
    r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\joueurs_brut.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"joueurs_brut.csv généré avec goals ({len(df_joueurs)} joueurs)")
