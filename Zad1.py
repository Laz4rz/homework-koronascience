from typing import List
import datetime as dt
import pandas as pd

CONFIRMED_CASES_URL = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

"""
When downloading data it's better to do it in a global scope instead of a function.
This speeds up the tests significantly
"""
confirmed_cases = pd.read_csv(CONFIRMED_CASES_URL, error_bad_lines=False)


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    """
    Returns confirmed infection cases for country 'Poland' given a date.
    Ex.
    poland_cases_by_date(7, 3, 2020)
    5
    poland_cases_by_date(11, 3)
    31
    :param year: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param day: Day of month to get the cases for as an integer indexed from 1
    :param month: Month to get the cases for as an integer indexed from 1
    :return: Number of cases on a given date as an integer
    """
    cases = confirmed_cases.loc[confirmed_cases["Country/Region"] == "Poland"]['/'.join([str(month), str(day), str(year % 100)])].values[0]
    return cases


def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    """
    Returns the top 5 infected countries given a date (confirmed cases).
    Ex.
    top5_countries_by_date(27, 2, 2020)
    ['China', 'Korea, South', 'Cruise Ship', 'Italy', 'Iran']
    top5_countries_by_date(12, 3)
    ['China', 'Italy', 'Iran', 'Korea, South', 'France']
    :param day: 4 digit integer representation of the year to get the countries for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: A list of strings with the names of the coutires
    """
    day = ('/'.join([str(month), str(day), str(year % 100)]))
    top5 = list(confirmed_cases.groupby("Country/Region").sum()[[day]].sort_values(by=day, ascending=False).head(5).index)
    return top5


def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    """
    Returns the number of countries/regions where the infection count in a given day was the same as the previous day.
    Ex.
    no_new_cases_count(11, 2, 2020)
    35
    no_new_cases_count(3, 3)
    57
    :param day: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: Number of countries/regions where the count has not changed in a day
    """

    today = '/'.join([str(month), str(day), str(year % 100)])
    yesterday = '/'.join([str(int(str(dt.date(year, month, day) - dt.timedelta(days=1))[2:].split('-')[(i + 1) % 3])) for i in range(3)])
    confirmed_cases2 = confirmed_cases[["Country/Region", today, yesterday]]
    return len(confirmed_cases2[(confirmed_cases2[today] != confirmed_cases2[yesterday]) & (confirmed_cases2[today] > 0)].index)

#First works like charm, Ministry of Health reported 1389 cases at the end of 27.03.20
print("Number of cases for 27.03.20: "+str(poland_cases_by_date(27,3,2020)))

#Second gives same results as worldometer coronavirus page
print("Top 5 countries for 27.03.20: "+str(top5_countries_by_date(27,3,2020)))

#Third works well with the example shown in the comment
print("No new cases since previous day for 11.2.20: "+str(no_new_cases_count(11,2,2020)))




