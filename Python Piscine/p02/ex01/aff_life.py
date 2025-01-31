from load_csv import load
import matplotlib.pyplot as plt


def main():
    """
    A program that takes the csv file and displays the country information
    of its campus
    """
    try:
        data = load("life_expectancy_years.csv")
        if data is None:
            raise AssertionError("Invalid Input")
        countryData = data[data['country'] == 'United Arab Emirates']
        years = countryData.columns[1:]
        lifeExpectancy = countryData.values[0][1:]

        plt.plot(years, lifeExpectancy, label='UAE')
        plt.title('UAE Life expectancy Projections')
        plt.xlabel('Year')
        plt.xticks(years[::40], rotation=45)
        plt.ylabel('Life Expectancy')
        plt.yticks(range(30, 101, 10))
        plt.legend()
        plt.tight_layout()
        plt.show()
    except AssertionError:
        return


if __name__ == '__main__':
    main()
