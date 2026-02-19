#-*- coding: utf-8 -*-
from pandas import read_excel, to_numeric, DataFrame, Series
from numpy import random, argmax
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")
matplotlib.rcParams['toolbar'] = 'None'

FORVENTET_LEVETID = 65
SIGMA = 8


def main():
    årstall_store_kraftverk = read_årstall_store_kraftverk()

    plot_byggeår(årstall_store_kraftverk)

    for i in range(10):
        årstall_utskifting_trafo = simuler(årstall_store_kraftverk)
        plot_simulering(årstall_utskifting_trafo, i)

    plt.show()


def read_årstall_store_kraftverk():
    # Last inn xlsx
    df = read_excel("hydro_power_plants_in_operation.xlsx")
    df["DatoForEldsteKraftproduserendeDel"] = to_numeric(
        df["DatoForEldsteKraftproduserendeDel"],
        errors="coerce"
    ).dropna()

    df_filtered = df[df["MaksYtelse"] > 10]

    return df_filtered["DatoForEldsteKraftproduserendeDel"]


def simuler(årstall_store_kraftverk: Series):
    variasjon = random.normal(loc=0, scale=SIGMA, size=len(årstall_store_kraftverk))

    årstall_utskifting_trafo = årstall_store_kraftverk + FORVENTET_LEVETID + variasjon.astype(int)

    return årstall_utskifting_trafo


def plot_byggeår(df: DataFrame):
    DUS_BLÅ = "#7A9BC9"   # dus blå
    plot(df, "Antall kraftverk bygget > 10MW per år", "Byggår", DUS_BLÅ, 100, 0)


def plot_simulering(df: DataFrame, i: int):
    DUS_RØD = "#C97A7A"   # dus rød
    plot(df, f"Utskifting av trafo > 10MW per år", f"Scenario {i+1}", DUS_RØD, 100 + 400*(i%5), 420 + 420*(i//5), True)


def plot(df: DataFrame, title: str, window_title: str, color: str, x: int, y: int, sim: bool = False):
    DUS_TURKIS = "#40E0D0"

    fig = plt.figure()
    counts, bins, patches = plt.hist(df, bins=30, rwidth=0.95, color=color)

    print(df.min(), df.max(), df.max()-df.min())

    # Marker stolpe med høyest frekvens
    max_index = argmax(counts)
    patches[max_index].set_facecolor(DUS_TURKIS)
    x_pos = bins[max_index+1]
    y_pos = counts[max_index]
    år_start = int(bins[max_index])
    år_slutt = int(bins[max_index+1])
    antall = int(y_pos)
    plt.text(x_pos, y_pos , f"Topp: {antall} stk i årene \n     {år_start}-{år_slutt}", ha="left", va="top", color="#202020", fontsize=8)

    plt.xlabel("År")
    plt.ylabel("Antall")
    plt.ylim(0, 45)

    fig.text(0.5, 0.92, f"{title}", ha="center", fontsize=11)
    if (sim):
        fig.text(0.5, 0.89, f"(μ={FORVENTET_LEVETID}, σ={SIGMA})", ha="center", fontsize=6)

    fig.canvas.manager.set_window_title(window_title)
    fig.canvas.manager.window.resize(370, 370)
    fig.canvas.manager.window.move(x, y)


if __name__ == "__main__":
    main()
