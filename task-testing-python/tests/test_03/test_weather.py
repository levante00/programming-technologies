from weather_03.weather_wrapper import WeatherWrapper
import pytest
import requests_mock

token = "OwEPxcuW0NeSDf2ar88jUs1LV4vwl2Hm"

BASE_URL = "http://dataservice.accuweather.com/currentconditions/v1/"
FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
LOCATION_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"

city_1 = "Yerevan"
city_2 = "Moscow"
city_3 = "Amsterdam"
city_4 = "Berlin"
city_5 = "London"

city_1_key = "16890"
city_2_key = "294021"
city_3_key = "249758"
city_4_key = "178087"
city_5_key = "328328"

def matcher_1(request):
    if city_1 in str(request):
        return True
    return None

def matcher_2(request):
    if city_2 in str(request):
        return True
    return None

def matcher_3(request):
    if city_3 in str(request):
        return True
    return None

def matcher_4(request):
    if city_4 in str(request):
        return True
    return None

def matcher_5(request):
    if city_5 in str(request):
        return True
    return None


def test_get():
    wrapper = WeatherWrapper(token)
    with requests_mock.Mocker() as m:
        m.get(BASE_URL, json=[{"Key": city_1_key}], status_code=200)
        assert wrapper.get(city_1, BASE_URL)


def test_get_response_city():
    wrapper = WeatherWrapper(token)
    with requests_mock.Mocker() as m:
        m.get(LOCATION_URL, json=[{"Key": city_1_key}], status_code=200)
        assert wrapper.get_response_city(city_1, LOCATION_URL) == [{"Key": city_1_key}]

        m.get(LOCATION_URL, status_code=500)

        with pytest.raises(AttributeError) as error:
            assert wrapper.get_response_city(city_1, LOCATION_URL)
        assert str(error.value) == "Incorrect city"


def test_get_location_key():
    wrapper = WeatherWrapper(token)
    wrapper.location_cache = {city_1: city_1_key}

    assert wrapper.get_location_key(city_1) == city_1_key

    with requests_mock.Mocker() as m:
        m.get(LOCATION_URL, json=[{"Key": city_1_key}], status_code=200)
        assert wrapper.get_location_key(city_1) == city_1_key

        m.get(LOCATION_URL, json=[], status_code=200)

        with pytest.raises(ValueError) as error:
            assert wrapper.get_location_key("Not_Existing_City")
        assert str(error.value) == f"City Not_Existing_City not found"


def test_get_temperature():
    wrapper = WeatherWrapper(token)
    with requests_mock.Mocker() as m:
        m.get(LOCATION_URL, json=[{"Key": city_1_key}], status_code=200)
        m.get(
            BASE_URL + city_1_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 8.3, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 47, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )

        assert wrapper.get_temperature(city_1) == 8.3

        m.get(LOCATION_URL, json=[], status_code=200)

        with pytest.raises(ValueError) as error:
            assert wrapper.get_temperature("Not_Existing_City")
        assert str(error.value) == "City Not_Existing_City not found"


def test_get_tomorrow_temperature():
    wrapper = WeatherWrapper(token)
    with requests_mock.Mocker() as m:
        m.get(LOCATION_URL, json=[{"Key": city_1_key}], status_code=200)
        m.get(
            FORECAST_URL + city_1_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 18.5, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 10.5, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 21.5, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 11.1, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 23.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 10.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 24.1, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 12.2, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 25, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert wrapper.get_tomorrow_temperature(city_1) == 21.5

        m.get(LOCATION_URL, json=[], status_code=200)

        with pytest.raises(ValueError) as error:
            assert wrapper.get_tomorrow_temperature("Not_Existing_City")
        assert str(error.value) == "City Not_Existing_City not found"


def test_find_diff_two_cities():
    wrapper = WeatherWrapper(token)

    with requests_mock.Mocker() as m:
        m.get(
            LOCATION_URL,
            json=[{"Key": city_1_key}],
            status_code=200,
            additional_matcher=matcher_1,
        )
        m.get(
            LOCATION_URL,
            json=[{"Key": city_2_key}],
            status_code=200,
            additional_matcher=matcher_2,
        )
        m.get(
            BASE_URL + city_1_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 8.3, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 47, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )
        m.get(
            BASE_URL + city_2_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 5, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 41, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )

        assert round(wrapper.find_diff_two_cities(city_1, city_2), 1) == 3.3


def test_get_diff_string():
    wrapper = WeatherWrapper(token)

    with requests_mock.Mocker() as m:
        m.get(
            LOCATION_URL,
            json=[{"Key": city_1_key}],
            status_code=200,
            additional_matcher=matcher_1,
        )
        m.get(
            LOCATION_URL,
            json=[{"Key": city_2_key}],
            status_code=200,
            additional_matcher=matcher_2,
        )
        m.get(
            BASE_URL + city_1_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 8.3, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 47, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )
        m.get(
            BASE_URL + city_2_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 5, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 41, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )

        assert (
            wrapper.get_diff_string(city_1, city_2)
            == f"Weather in {city_1} is warmer than in {city_2} "
            f"by 3 degrees"
        )

        assert (
            wrapper.get_diff_string(city_2, city_1)
            == f"Weather in {city_2} is colder than in {city_1} "
            f"by 3 degrees"
        )


def test_get_tomorrow_diff():
    wrapper = WeatherWrapper(token)

    with requests_mock.Mocker() as m:
        m.get(
            LOCATION_URL,
            json=[{"Key": city_1_key}],
            status_code=200,
            additional_matcher=matcher_1,
        )

        m.get(
            BASE_URL + city_1_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 8.3, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 47, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )

        m.get(
            FORECAST_URL + city_1_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 18.5, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 10.5, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 21.5, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 11.1, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 23.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 10.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 24.1, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 12.2, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 25, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert (
            wrapper.get_tomorrow_diff(city_1)
            == f"The weather in {city_1} tomorrow will be much warmer than today"
        )
        # -------------------------------
        m.get(
            LOCATION_URL,
            json=[{"Key": city_2_key}],
            status_code=200,
            additional_matcher=matcher_2,
        )

        m.get(
            BASE_URL + city_2_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 5, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 41, "Unit": "F", "UnitType": 18},
                    }
                }
            ],
            status_code=200,
        )

        m.get(
            FORECAST_URL + city_2_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 3.9, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 7.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 1.2, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 5.6, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 5, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 15, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 7.4, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 10.7, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 2.1, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 12.6, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert (
            wrapper.get_tomorrow_diff(city_2)
            == f"The weather in {city_2} tomorrow will be warmer than today"
        )
        # -------------------------------
        m.get(
            LOCATION_URL,
            json=[{"Key": city_3_key}],
            status_code=200,
            additional_matcher=matcher_3,
        )

        m.get(
            BASE_URL + city_3_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 7.8, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 46, "Unit": "F", "UnitType": 18},
                    },
                }
            ],
            status_code=200,
        )

        m.get(
            FORECAST_URL + city_3_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 5, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 10.6, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": -5, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 2.3, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 3.3, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 10, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 5.9, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 10.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 5.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 11.6, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert (
            wrapper.get_tomorrow_diff(city_3)
            == f"The weather in {city_3} tomorrow will be much colder than today"
        )
        # -------------------------------
        m.get(
            LOCATION_URL,
            json=[{"Key": city_4_key}],
            status_code=200,
            additional_matcher=matcher_4,
        )

        m.get(
            BASE_URL + city_4_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 6.1, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 43, "Unit": "F", "UnitType": 18},
                    },
                }
            ],
            status_code=200,
        )

        m.get(
            FORECAST_URL + city_4_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 5.6, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 15.4, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": -4, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 4.9, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 1.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 11, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 3.4, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 12, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 3.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 9.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert (
            wrapper.get_tomorrow_diff(city_4)
            == f"The weather in {city_4} tomorrow will be colder than today"
        )
        # -------------------------------
        m.get(
            LOCATION_URL,
            json=[{"Key": city_5_key}],
            status_code=200,
            additional_matcher=matcher_5,
        )

        m.get(
            BASE_URL + city_5_key,
            json=[
                {
                    "Temperature": {
                        "Metric": {"Value": 8.4, "Unit": "C", "UnitType": 17},
                        "Imperial": {"Value": 47, "Unit": "F", "UnitType": 18},
                    },
                }
            ],
            status_code=200,
        )

        m.get(
            FORECAST_URL + city_5_key,
            json={
                "DailyForecasts": [
                    {
                        "Temperature": {
                            "Minimum": {"Value": 7, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 12.2, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 4.8, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 8.8, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 3.7, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 11.9, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 7.6, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 13.6, "Unit": "C", "UnitType": 17},
                        },
                    },
                    {
                        "Temperature": {
                            "Minimum": {"Value": 7, "Unit": "C", "UnitType": 17},
                            "Maximum": {"Value": 15.2, "Unit": "C", "UnitType": 17},
                        },
                    },
                ]
            },
            status_code=200,
        )

        assert (
            wrapper.get_tomorrow_diff(city_5)
            == f"The weather in {city_5} tomorrow will be the same than today"
        )
        # -------------------------------
