import pandas as pd
from pathlib import Path


df_groupes = pd.read_csv(r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\groupes.csv")
df_equipes = pd.DataFrame(
    sorted(df_groupes["equipe"].unique()),
    columns=["equipe"]
)

df_equipes.to_csv(r"C:\Users\WIJDANE TAFTAF\Desktop\can2025-chatbot\data\equipes.csv", index=False, encoding="utf-8-sig")
print("equipes.csv généré")
