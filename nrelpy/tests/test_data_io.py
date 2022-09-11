from nrelpy.utils.data_io import save_local, check_stored_data, DATA_PATH
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

def test_save_local_case1():
    """
    This tests the standard use case of `save_local`
    where a dataframe, database type, and year are passed.
    """
    save_local(tech_df, database=db, year=yr)
    file_name = str(DATA_PATH / f'ATBe_{yr}.pkl')
    files = glob.glob(file_name)
    os.remove(file_name)
    assert len(files) == 1
    return

def test_save_local_case2():
    """
    This tests a standard use case of `save_local`
    where a dataframe, database type, and year are passed.
    The dataframe is saved as a CSV instead of pickled.
    """
    save_local(tech_df, database=db, year=yr, pickle=False)
    file_name = str(DATA_PATH / f'ATBe_{yr}.csv')
    files = glob.glob(file_name)
    os.remove(file_name)
    assert len(files) == 1
    return

