import pandas as pd

df_temp = pd.read_csv("dataset/datos_limpios_eerr.csv", encoding="latin1", delimiter=",", on_bad_lines="skip")

print("🔍 Columnas encontradas en el archivo:")
print(df_temp.columns)
