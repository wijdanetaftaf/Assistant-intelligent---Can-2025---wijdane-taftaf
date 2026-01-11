import pandas as pd
from functools import lru_cache
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


class DataLoadError(Exception):
    """Exception personnalisée pour les erreurs de chargement de données"""
    pass


def clean_number(value):
    """Nettoie et convertit une valeur en nombre entier"""
    if pd.isna(value):
        return 0
    value_str = str(value).replace('\xa0', '').replace(' ', '').replace(',', '')
    try:
        return int(float(value_str))
    except (ValueError, TypeError) as e:
        logger.warning(f"Erreur conversion nombre: {value_str} -> {e}")
        return 0


def normalize_team_name(name):
    """Normalise le nom d'une équipe"""
    if pd.isna(name):
        return ""
    return str(name).strip().title()


@lru_cache(maxsize=1)
def load_poules():
    """Charge les matchs de poules avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "poules_matchs.csv")
        df['equipe1'] = df['equipe1'].apply(normalize_team_name)
        df['equipe2'] = df['equipe2'].apply(normalize_team_name)
        logger.info(f"✓ Matchs de poules chargés: {len(df)} matchs")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: poules_matchs.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement poules_matchs.csv: {e}")
        raise DataLoadError(f"Erreur chargement poules: {e}")


@lru_cache(maxsize=1)
def load_finales():
    """Charge les matchs de phases finales avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "phases_finales_matchs.csv")
        df['equipe1'] = df['equipe1'].apply(normalize_team_name)
        df['equipe2'] = df['equipe2'].apply(normalize_team_name)
        logger.info(f"✓ Phases finales chargées: {len(df)} matchs")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: phases_finales_matchs.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement phases_finales_matchs.csv: {e}")
        raise DataLoadError(f"Erreur chargement finales: {e}")


@lru_cache(maxsize=1)
def load_joueurs():
    """Charge la liste des joueurs avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "joueurs_brut.csv")
        df['equipe'] = df['equipe'].apply(normalize_team_name)
        logger.info(f"✓ Joueurs chargés: {len(df)} joueurs")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: joueurs_brut.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement joueurs_brut.csv: {e}")
        raise DataLoadError(f"Erreur chargement joueurs: {e}")


@lru_cache(maxsize=1)
def load_classement():
    """Charge le classement des groupes avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "classement_groupes.csv")
        df['equipe'] = df['equipe'].apply(normalize_team_name)
        logger.info(f"✓ Classements chargés: {len(df)} équipes")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: classement_groupes.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement classement_groupes.csv: {e}")
        raise DataLoadError(f"Erreur chargement classement: {e}")


@lru_cache(maxsize=1)
def load_groupes():
    """Charge la composition des groupes avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "groupes.csv")
        df['equipe'] = df['equipe'].apply(normalize_team_name)
        logger.info(f"✓ Groupes chargés: {len(df)} équipes")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: groupes.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement groupes.csv: {e}")
        raise DataLoadError(f"Erreur chargement groupes: {e}")


@lru_cache(maxsize=1)
def load_stades():
    """Charge la liste des stades avec cache et normalisation"""
    try:
        df = pd.read_csv(DATA_DIR / "stades.csv")
        # Normaliser les capacités
        df['capacite'] = df['capacite'].apply(clean_number)
        logger.info(f"✓ Stades chargés: {len(df)} stades")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier manquant: stades.csv")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur chargement stades.csv: {e}")
        raise DataLoadError(f"Erreur chargement stades: {e}")


@lru_cache(maxsize=1)
def load_equipes():
    """Charge la liste des équipes avec cache"""
    try:
        df = pd.read_csv(DATA_DIR / "equipes.csv")
        equipes = df['equipe'].apply(normalize_team_name).tolist()
        logger.info(f"✓ Équipes chargées: {len(equipes)} équipes")
        return equipes
    except FileNotFoundError:
        logger.error(f"Fichier manquant: equipes.csv")
        return []
    except Exception as e:
        logger.error(f"Erreur chargement equipes.csv: {e}")
        raise DataLoadError(f"Erreur chargement équipes: {e}")


def load_all_data():
    """
    Charge toutes les données nécessaires
    Retourne un dictionnaire avec tous les DataFrames
    """
    return {
        'poules': load_poules(),
        'finales': load_finales(),
        'joueurs': load_joueurs(),
        'classement': load_classement(),
        'groupes': load_groupes(),
        'stades': load_stades(),
        'equipes': load_equipes()
    }


def clear_cache():
    """Vide le cache de toutes les données"""
    load_poules.cache_clear()
    load_finales.cache_clear()
    load_joueurs.cache_clear()
    load_classement.cache_clear()
    load_groupes.cache_clear()
    load_stades.cache_clear()
    load_equipes.cache_clear()
    logger.info("✓ Cache vidé")


if __name__ == "__main__":
    # Test de chargement
    print("Test de chargement des données...")
    data = load_all_data()
    for key, value in data.items():
        if isinstance(value, pd.DataFrame):
            print(f"{key}: {len(value)} lignes")
        else:
            print(f"{key}: {len(value)} éléments")
