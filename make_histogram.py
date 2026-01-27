#-*- coding: utf-8 -*-
from pandas import read_excel, to_numeric, DataFrame
from numpy import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")
matplotlib.rcParams['toolbar'] = 'None'

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


def simuler(årstall_store_kraftverk):
    FORVENTET_LEVETID = 65
    SIGMA = 5
    variasjon = random.normal(loc=0, scale=SIGMA, size=len(årstall_store_kraftverk))

    årstall_utskifting_trafo = årstall_store_kraftverk + FORVENTET_LEVETID + variasjon

    return årstall_utskifting_trafo


def plot_byggeår(df: DataFrame):
    DUS_BLÅ = "#7A9BC9"   # dus blå
    plot(df, "Antall kraftverk > 10MVA bygd per år", DUS_BLÅ, 100, 0)


def plot_simulering(df: DataFrame, i):
    DUS_RØD = "#C97A7A"   # dus rød
    plot(df, "Antall utskifting av trafo per år", DUS_RØD, 100 + 400*(i%5), 420 + 420*(i//5))


def plot(df: DataFrame, title: str, color: str, x: int, y: int):
    fig = plt.figure()
    plt.hist(df, bins=20, rwidth=0.95, color=color)
    plt.xlabel("År")
    plt.ylabel("Antall")
    plt.ylim(0, 60)

    plt.title(title)
    fig.canvas.manager.window.resize(370, 370)
    fig.canvas.manager.window.move(x, y)


if __name__ == "__main__":
    main()
