from nrelpy.atb import as_dataframe, ATBe
from urllib.error import HTTPError
import pytest

good_year = 2020
bad_year = -999
nonexistent_year = 2000

good_tech = 'Nuclear'
good_detail = 'NuclearSMR'
good_metric = 'CAPEX'
bad_tech = 'Dark Matter Engine'
bad_detail = 'PlanetExpress'
bad_metric = 'Kajiggers'

def test_as_dataframe_electricity_good_year():
    database = 'electricity'

    df = as_dataframe(good_year, database)

    return


def test_as_dataframe_electricity_bad_year():
    database = 'electricity'

    with pytest.raises(HTTPError) as e:
        df = as_dataframe(bad_year, database)

    assert (e.type == HTTPError)

    return


def test_as_dataframe_electricity_nonexistent():
    database = 'electricity'

    with pytest.raises(HTTPError) as e:
        df = as_dataframe(nonexistent_year, database)

    assert (e.type == HTTPError)

    return


def test_as_dataframe_transportation_good_year():
    database = 'transportation'

    df = as_dataframe(good_year, database)

    return


def test_as_dataframe_transportation_nonexistent():
    database = 'transportation'

    with pytest.raises(HTTPError) as e:
        df = as_dataframe(nonexistent_year, database)

    assert (e.type == HTTPError)

    return


def test_as_dataframe_transportation_bad_year():
    database = 'transportation'

    with pytest.raises(HTTPError) as e:
        df = as_dataframe(bad_year, database)

    assert (e.type == HTTPError)

    return


def test_as_dataframe_bad_database():
    database = 'heating'

    with pytest.raises(KeyError) as e:
        df = as_dataframe(bad_year, database)

    assert (e.type == KeyError)

    return


def test_ATB_init():

    atb_class = ATBe(year=2022)

    assert atb_class.scenario == 'Moderate'
    assert atb_class.case == 'R&D'
    assert atb_class.year == 2022
    assert atb_class.dataframe.scenario.unique() == ['Moderate']

    return

def test_ATB_scenario_change():
    
    atb_class = ATBe(year=2022)

    assert atb_class.dataframe.scenario.unique() == ['Moderate']
    assert atb_class.dataframe.core_metric_case.unique() == ['R&D']

    atb_class.scenario = 'Advanced'
    atb_class.case = 'Market'
    assert atb_class.dataframe.scenario.unique() == ['Advanced']
    assert atb_class.dataframe.core_metric_case.unique() == ['Market']



atb_class = ATBe(year=2022)
def test_ATB_get_data_good_values():
    exp_value = 7988.95108
    actual_value = atb_class.get_data(good_tech, good_metric, good_detail)
    assert (abs(exp_value - actual_value) < 1e-5)

def test_ATB_get_data_bad_values():
    with pytest.raises(AssertionError):
        atb_class.get_data(bad_tech, good_metric, good_detail)
        atb_class.get_data(good_tech, bad_metric, good_detail)
        atb_class.get_data(good_tech, good_metric, bad_detail)

