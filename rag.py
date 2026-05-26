import pandas as pd

def load_data():
    return pd.read_csv("datos.csv")

def retrieve(query):
    df = load_data()
    q = query.lower()

    # RAG simple pero defendible en examen
    if "resistente" in q:
        return df[df["densidad"] >= 0.7]

    if "barato" in q:
        return df[df["precio"] == df["precio"].min()]

    if "ligero" in q:
        return df[df["tipo"] == "ligero"]

    return df
