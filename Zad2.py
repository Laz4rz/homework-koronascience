from typing import List
import pandas as pd
import datetime
import os

# confirmed cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
dfC = pd.read_csv(url, error_bad_lines=False)

# deaths
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
dfD = pd.read_csv(url, error_bad_lines=False)

# recovered cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
dfR = pd.read_csv(url, error_bad_lines=False)


# Helper function (strftime not cross platform) ???
def format_date(date: datetime.date):
    if os.name == "nt":
        return date.strftime('%#m/%#d/%y')
    else:
        return date.strftime('%-m/%-d/%y')


def countries_with_no_deaths_count(date: datetime.date) -> int:
    """
    Returns the number of areas (countries, region, provinces) in the data set
    where infections were found, but nobody died on a given date. (DO NOT GROUP BY)
    Ex.
    countries_with_no_deaths_count(datetime.date(2020, 3, 15))
    171
    countries_with_no_deaths_count(datetime.date(2020, 2, 18))
    46
    :param date: Date object of the date to get the results for
    :return: Number of countries with no deaths but with active cases on a given date as an integer
    """

    day = format_date(date)
    deaths_day = dfD[["Country/Region", day]]
    cases_day = dfC[["Country/Region", day]]

    comp = pd.concat([deaths_day[day], cases_day[day]], axis=1, keys=("deaths", "cases"))
    result = len(comp[(comp["deaths"] == 0) & (comp["cases"] > 0)])

    print(comp[(comp["deaths"] == 0) & (comp["cases"] > 0)])

    return result


def more_cured_than_deaths_indices(date: datetime.date) -> List[int]:
    """
    Returns table indices of areas (countries, region, provinces) in the data set
    with more cured cases than deaths on a given date. (DO NOT GROUP BY)
    Ex.
     more_cured_than_deaths_indices(datetime.date(2020, 3, 15))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19,
    21, 24, 25, 27, 28, 29, 30, 32, 33, 34, 37, 38, 40, 41, 43, 44,
    45, 46, 53, 55, 58, 59, 60, 62, 64, 65, 68, 86, 92, 101, 110, 118,
    128, 154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167,
    168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182,
    183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 202, 208]
    more_cured_than_deaths_indices(datetime.date(2020, 2, 18))
    [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 15, 18, 19, 20, 92, 154, 156,
    157, 158, 159, 160, 161, 162, 163, 164, 166, 167, 168, 169, 171, 172,
    173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187,
    188, 189, 190, 191, 192, 193, 194, 202, 347, 348, 403]
    :param date: Date object of the date to get the results for
    :return: A List of integers containing indices of countries which had more cured cases than deaths on a given date
    """

    day = format_date(date)
    deaths_day = dfD[["Country/Region", day]]
    rec_day = dfR[["Country/Region", day]]

    comp = pd.concat([deaths_day[day], rec_day[day]], axis=1, keys=("deaths", "recovered"))
    result = list(comp[(comp["deaths"] < comp["recovered"])].index)

    print(comp[(comp["deaths"] < comp["recovered"])])

    return result

#First shows else than the example but looks to be working fine after looking into the data table, possibly the data has changed after time
print("No new deaths, with incresing cases for 27.03.20: "+str(countries_with_no_deaths_count(datetime.date(2020,3,27))))

#Second, same goes here, but then again - data seems to be correct, but is different than the example
print("More cured than dead for 18.02.20: "+str(more_cured_than_deaths_indices(datetime.date(2020,2,18))))
