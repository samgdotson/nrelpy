from nrelpy.re_potential import *
import pytest
import pandas as pd


def test_as_dataframe_standard():
    """
    This tests the base case where no
    arguments are passed.
    """

    df = as_dataframe()

    assert isinstance(df, pd.DataFrame)

    return


def test_as_dataframe_bad_url():
    """
    This tests the base case where a bad
    url is passed.
    """

    bad_url = "https://www.nrel.gov/gis/assets/docs/us-re-technical-potential"
    with pytest.raises(HTTPError) as e:
        as_dataframe(url=bad_url)

    return


@pytest.mark.filterwarnings("ignore")
def test_as_dataframe_verbose():
    """
    This tests the verbosity setting of
    """

    df = as_dataframe(verbose=True)

    assert isinstance(df, pd.DataFrame)

    return
