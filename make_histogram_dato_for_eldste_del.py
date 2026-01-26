import pandas as pd
import matplotlib.pyplot as plt

# Last inn xlsx
df = pd.read_excel("hydro_power_plants_in_operation.xlsx")

# Sørg for at kolonnen tolkes som dato
datoer = pd.to_numeric(
    df["DatoForEldsteKraftproduserendeDel"],
    errors="coerce"
).dropna()

df_filtered = df[df["MaksYtelse"] > 10]

# Histogram (år)
counts, bins, _ = plt.hist(df_filtered["DatoForEldsteKraftproduserendeDel"], bins=20, rwidth=0.95)
plt.xlabel("År")
plt.ylabel("Antall")
plt.title("Antall kraftverk > 10MVA etter årstall for eldste kraftproduserende del")
plt.xticks(bins.astype(int), rotation=45)  # roter labels om ønskelig
plt.show()