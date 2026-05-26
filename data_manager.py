import pandas as pd

def cargar_datos():
    return pd.read_csv("datos.csv")

def material_mas_caro():
    df = cargar_datos()
    fila = df.loc[df["precio"].idxmax()]
    return fila["nombre"], fila["precio"]

