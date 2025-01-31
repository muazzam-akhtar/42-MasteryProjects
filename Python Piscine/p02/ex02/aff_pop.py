from load_csv import load
import matplotlib.pyplot as plt


def preprocess_population(pop_str):
    """
    Preprocesses the population string to convert it into
    a numeric value in standard form.

    Args:
        pop_str (str): Population string with or without
        the 'M' suffix for million.

    Returns:
        float: Numeric population value.
    """
    if pop_str.endswith("B"):
        return float(pop_str[:-1]) * 1e6
    elif pop_str.endswith("M"):
        return float(pop_str[:-1]) * 1e6
    elif pop_str.endswith("k"):
        return float(pop_str[:-1]) * 1e3
    else:
        return float(pop_str)


def main():
    """
    Loads population data from a CSV file, processes and
    plots(used for creating line plots)
    the population comparison of three countries.
    """
    try:
        data = load("population_total.csv")
        if data is None:
            raise AssertionError("Invalid Input")

        country1 = "United Arab Emirates"
        country2 = "France"

        uae_data = data[data['country'] == country1].iloc[:, 1:]
        france_data = data[data['country'] == country2].iloc[:, 1:]

        uae_pop = uae_data.values.flatten()
        france_pop = france_data.values.flatten()
        years = uae_data.columns.astype(int)

        uae_pop = [preprocess_population(pop) for pop in uae_pop]
        france_pop = [preprocess_population(pop) for pop in france_pop]

        plt.plot(years, uae_pop, label=country1)
        plt.plot(years, france_pop, label=country2)

        plt.title("Population in {} and {}".format(country1, country2))
        plt.xlabel("Year")
        plt.xticks(range(1800, 2051, 40), range(1800, 2051, 40))
        plt.xlim(1800, 2050)
        plt.ylabel("Population")
        plt.legend()
        plt.tight_layout()
        max_pop = max(max(uae_pop), max(france_pop))
        y_ticks = [i * 1e7 for i in range(int(max_pop / 1e7) + 1)]
        plt.yticks(y_ticks, ["{:,.0f}M".format(pop / 1e6) for pop in y_ticks])
        plt.show()
    except AssertionError:
        return


if __name__ == "__main__":
    main()
