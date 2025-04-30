import yaml
import csv
import pandas as pd
from difflib import get_close_matches
from bs4 import BeautifulSoup
from config import config

EXCLUDE = ['Ahorro', 'Interno']

def find_best_match(concept):
    translations = config.translations

    if not isinstance(translations, dict) or not translations:
        return ""

    best_key = None
    best_match_score = 0

    for reference, concepts in translations.items():
        if not isinstance(concepts, list):
            continue

        match = get_close_matches(concept, concepts, n=1, cutoff=0.6)

        if match:
            similarity_score = get_similarity(concept, match[0])

            if similarity_score > best_match_score:
                best_match_score = similarity_score
                best_key = reference

    return best_key if best_key else ""

def get_similarity(word1, word2):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, word1, word2).ratio()


def update_yaml(df):
    for _, row in df.iterrows():
        concept = row["Concepto"]
        reference = row["Nota"]

        if reference:
            if reference in config.translations:

                if concept not in config.translations[reference]:
                    config.translations[reference].append(concept)
            else:

                config.translations[reference] = [concept]

    config.save_translations()

def calculate_expenses(df):
    data = {}
    for _, row in df.iterrows():
        concept = row["Nota"]
        if concept in EXCLUDE:
            continue
        value = abs(float(row["Importe"].replace('.', '').replace(',', '.')))
        if concept not in data:
            data[concept] = value
        else:
            data[concept] = value + data[concept]

    return pd.DataFrame(list(data.items()), columns=['Concepto', 'Importe'])

