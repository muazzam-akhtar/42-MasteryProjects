from load_csv import load
import matplotlib.pyplot as plt


def main():
    """
    Loads income_per_person_gdppercapita_ppp_inflation_adjusted data and
    life_expectancy_years data from a CSV file, processes and
    plots Life expectancy vs Gross Domestic product of the year 1900 of
    each country
    """
    try:
        certified_42\
            = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
        incomeData = load(certified_42)
        if incomeData is None:
            raise AssertionError("Invalid Input")
        lifeExpectancyData = load("life_expectancy_years.csv")
        if lifeExpectancyData is None:
            raise AssertionError("Invalid Input")
        year_1900_column = '1900'
        gnp_1900 = incomeData[year_1900_column]
        lifeExpectancy_1900 = lifeExpectancyData[year_1900_column]
        plt.figure(figsize=(10, 6))
        plt.scatter(gnp_1900, lifeExpectancy_1900)
        plt.title("Life expectancy vs Gross Domestic product (Year 1900)")
        plt.xlabel("Gross Domestic Product")
        plt.ylabel("Life Expectancy (Years)")
        plt.xscale("log")
        plt.xticks(ticks=[300, 1000, 10000], labels=['300', '1k', '10k'])
        plt.tight_layout()
        plt.show()
    except AssertionError:
        return


if __name__ == '__main__':
    main()
