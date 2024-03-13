from nrelpy.atb import as_dataframe, ATBe
import pandas as pd
from urllib.error import HTTPError
import pytest
import numpy as np

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
    atb_class = ATBe(year=good_year)
    assert atb_class.year == good_year
    
    with pytest.raises(HTTPError) as e:
        atb_class = ATBe(bad_year)
        
    with pytest.raises(HTTPError) as e:
        atb_class = ATBe(nonexistent_year)

    return


def test_ATB_acronyms():
    
    atb_class = ATBe(2023)
    assert isinstance(atb_class.acronyms, pd.DataFrame)
    
    with pytest.warns(RuntimeWarning) as w:
        atb_class = ATBe(good_year)
        acros_df = atb_class.acronyms
    
    return


def test_ATB_access():
    atb_class = ATBe(good_year)
    
    subset = atb_class(technology='Nuclear')
    assert subset.shape == (6534,2)
    return
    
def test_ATB_value_access():
    atbe2020 = ATBe(good_year)
    mask = (
        (atbe2020.raw_dataframe['technology']=='Nuclear')&
        (atbe2020.raw_dataframe['core_metric_parameter']=='LCOE')&
        (atbe2020.raw_dataframe['core_metric_case']=='Market')&
        (atbe2020.raw_dataframe['core_metric_variable']==2020)&
        (atbe2020.raw_dataframe['crpyears']==20)
        )
    value = atbe2020.raw_dataframe[mask]['value'].values[0]
    assert np.isclose(value, 88.22242)
    


