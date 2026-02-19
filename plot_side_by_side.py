#-*- coding: utf-8 -*-
from pandas import read_excel, to_numeric, Series
from numpy import random, argmax, median, floor, ceil, arange
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import weibull_min

matplotlib.use("QtAgg")
matplotlib.rcParams['toolbar'] = 'None'

FORVENTET_LEVETID = 65
SIGMA = 20


def main():
    byggeår = read_byggeår()

    for i, beta in enumerate(range(2, 8, 1)):
        utskiftingsår = simuler_utskiftingsår(byggeår, beta)
        plot(byggeår, utskiftingsår, i, beta)

    plt.show()


def read_byggeår():
    # Last inn xlsx
    df = read_excel("hydro_power_plants_in_operation.xlsx")
    df["DatoForEldsteKraftproduserendeDel"] = to_numeric(
        df["DatoForEldsteKraftproduserendeDel"],
        errors="coerce"
    ).dropna()

    df_filtered = df[df["MaksYtelse"] > 10]

    return df_filtered["DatoForEldsteKraftproduserendeDel"]


def simuler_utskiftingsår(byggeår: Series, β: float = 4.1):

    λ = 65.0
    levetid = weibull_min.rvs(β, scale=λ, size=len(byggeår))

    utskiftingsår = byggeår + levetid.astype(int)

    return utskiftingsår



def plot(byggeår: Series, utskiftingsår: Series, i: int, β: float):
    title =  "Antall kraftverk bygget > 10MW per år"
    window_title = "Byggår"

    DUS_BLÅ = "#7A9BC9"   # dus blå
    DUS_RØD = "#C97A7A"   # dus rød

    fig = plt.figure()

    plot_hist(utskiftingsår, DUS_RØD, label="Utskiftingsår")
    plot_hist(byggeår, DUS_BLÅ, label="Byggeår")

    plt.xlabel("År")
    plt.ylabel("Antall")
    plt.ylim(0, 40)

    fig.text(0.5, 0.92, f"{title}", ha="center", fontsize=11)
    fig.text(0.5, 0.89, f"(μ={FORVENTET_LEVETID}, β={β})", ha="center", fontsize=6)

    fig.canvas.manager.set_window_title(window_title)
    fig.canvas.manager.window.resize(900, 370)
    fig.canvas.manager.window.move(300 + (i // 3)*950, 100 + (i % 3)*450)


def plot_hist(series: Series, color: str, label: str):
    DUS_TURKIS = "#40E0D0"

    OFFSET_YEARS = 40
    SIZE_YEARS = 4

    medi = median(series)
    lower = SIZE_YEARS * floor((medi - OFFSET_YEARS) / SIZE_YEARS)
    upper = SIZE_YEARS * ceil((medi + OFFSET_YEARS) / SIZE_YEARS)
    bins = arange(lower, upper + SIZE_YEARS, SIZE_YEARS)

    series = series[(series >= lower) & (series <= upper)]

    counts, bins, patches = plt.hist(series, bins=bins, rwidth=0.95, color=color, label=label)

    # Marker stolpe med høyest frekvens
    max_index = argmax(counts)
    patches[max_index].set_facecolor(DUS_TURKIS)
    x_pos = bins[max_index+1]
    y_pos = counts[max_index]
    år_start = int(bins[max_index])
    år_slutt = int(bins[max_index+1])
    antall = int(y_pos)
    plt.text(x_pos, y_pos + 4, f"Topp: {antall} stk i årene \n     {år_start}-{år_slutt}", ha="left", va="top", color="#202020", fontsize=8)


if __name__ == "__main__":
    main()
