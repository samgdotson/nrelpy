from isort import file
import pytest
from nrelpy.utils.data_io import save_local, check_stored_data, DATA_PATH, generate_db_filename
from pathlib import Path
import sys
import os
import glob
import pandas as pd

# set up test data
data = {'tech': ['nuclear', 'solar', 'wind', 'naturalgas'],
            'variable_cost': [20, 0, 0, 180],  # $/GWh
            'fixed_cost': [92, 4, 11, 21],
            'capital_cost': [5.9, 0.8, 1.4, 1.0],
            'capacity_GW': [12, 3, 7, 5],
            'capacity_factor': [0.93, 0.17, 0.33, 0.45],
            'resentment': [100, 20, 50, 70]
            }
tech_df = pd.DataFrame(data)

db = 'electricity'
yr = 1882

data_path_exists = DATA_PATH.exists()

user_path = DATA_PATH / 'tmp_path'
user_path.mkdir(exist_ok=True, parents=True)

@pytest.fixture
def filename():
    fname = "ATBe_1882.pkl"

    return fname

def test_generate_db_filename(filename):
    """
    Tests that the function creates the correct filename.
    """

    obs = generate_db_filename(db, yr, pickled=True)

    assert obs == filename


def test_save_local_case1(filename):
    """
    This tests the standard use case of `save_local`
    where a dataframe, database type, and year are passed.
    """
    save_local(tech_df, filename)
    file_name = str(DATA_PATH / filename)
    print(file_name)
    files = glob.glob(file_name)
    os.remove(file_name)
    assert len(files) == 1
    return

def test_save_local_case2(filename):
    """
    This tests a standard use case of `save_local`
    where a dataframe, database type, and year are passed.
    The dataframe is saved as a CSV instead of pickled.
    """
    fname = filename.replace('pkl','csv')
    save_local(tech_df, fname)
    file_name = str(DATA_PATH / fname)
    files = glob.glob(file_name)
    os.remove(file_name)
    assert len(files) == 1
    return


def test_save_local_case3(filename):
    """
    This tests a standard use case of `save_local`
    where a dataframe, database type, and year are passed.
    The dataframe is saved to a user specified directory.
    """
    save_local(tech_df, filename, path=user_path)
    file_name = str(user_path / filename)
    files = glob.glob(file_name)
    os.remove(file_name)
    assert len(files) == 1
    return


def test_check_stored_data_case1(filename):
    """
    This tests a standard use case of `check_stored_data`
    where a database type and a year are passed.
    """
    save_local(tech_df, filename)
    df = check_stored_data(filename)
    file_name_yr = str(DATA_PATH / filename)
    os.remove(file_name_yr)
    assert df.equals(tech_df)
    return


def test_check_stored_data_case2(filename):
    """
    This tests a standard use case of `check_stored_data`
    where a database type and a year are passed.
    """
    fname = filename.replace(f'_{yr}','')
    save_local(tech_df, fname)
    df = check_stored_data(fname)
    file_name_no_yr = str(DATA_PATH / f'ATBe.pkl')
    os.remove(file_name_no_yr)
    assert df.equals(tech_df)
    return


def test_check_stored_data_case3(filename):
    """
    This tests saving and reading the data in a csv format.
    """
    fname = filename.replace('pkl', 'csv').replace(f'_{yr}', '')
    save_local(tech_df, fname)
    df = check_stored_data(fname)
    file_name_no_yr = str(DATA_PATH / fname)
    os.remove(file_name_no_yr)
    assert df.equals(tech_df)
    return