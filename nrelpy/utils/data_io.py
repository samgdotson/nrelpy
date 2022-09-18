import dill
from pathlib import Path
import pandas as pd
import glob
import os

curr_dir_os = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = (curr_dir_os / Path('..')).resolve() / 'data'
DATA_PATH.mkdir(exist_ok=True)

db_opts = {'electricity': 'ATBe',
           'transportation': 'ATBt',
           're_potential': 'NREL_REP'}


def check_stored_data(database, year=None, path=None, pickled=True):
    """
    This function checks for locally saved databases.

    Parameters
    ----------
    database : string
        The desired ATB dataset. Accepts: 'electricity', 'transportation',
        'potential'.
    year : int
        The ATB year
        * ATB Electricity (ATBe) accepts: [2019,2022] -- inclusive
        * ATB Transportation (ATBt) accepts: [2020]
    path : string or Path-like
        Users may specify where NRELPy should look for data.

    Returns
    -------
    df : pandas.DataFrame
        A pandas dataframe containing the stored data.
    """
    if pickled:
        ext = 'pkl'
    else:
        ext = 'csv'

    if year:
        file_name = f'{db_opts[database]}_{str(year)}.{ext}'
    else:
        file_name = f'{db_opts[database]}.{ext}'

    if path:
        search_path = Path(path) / file_name
    else:
        search_path = DATA_PATH / file_name

    file_match = glob.glob(str(search_path))

    if len(file_match) == 1:
        if pickled:
            df = pd.read_pickle(file_match[0])
        else:
            df = pd.read_csv(file_match[0], index_col=[0])
    elif len(file_match) == 0:
        raise FileNotFoundError(
            f"{file_name} file not found.")
    else:
        raise NameError(
            f"{file_name} returned multiple copies. Handling method unspecified. \n {file_match}")

    return df


def save_local(df, database, year=None, path=None, pickle=True):
    """
    This function saves a dataframe in the package data or to a
    locally defined path. It automatically generates a file name
    based on dataset attributes (e.g. name and year) that
    `nrelpy.utils.data_io.check_stored_data` will use to search.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas dataframe containing an NREL dataset.
    database : string
        The database string identifier. Accepts:
        ['electricity', 'transportation', 're_potential']
    year : int
        The database year. Only valid for 'ATBe'. Default
        is None.
    path : string or Path-like
        Allows users to specify a local directory to save
        their data. Otherwise, data will be saved to package
        data.
    pickle : bool
        If True, `df` will be saved as a pickled object using
        the `dill` package. Otherwise, it will be saved as a
        `.csv` file. Default is True.
    """
    if year:
        file_name = f'{db_opts[database]}_{str(year)}'
    else:
        file_name = f'{db_opts[database]}'
    if path:
        file_path = Path(path).resolve()
    else:
        file_path = DATA_PATH

    if pickle:
        with open(file_path / f'{file_name}.pkl', 'wb') as f:
            dill.dump(df, f)
    elif isinstance(df, pd.DataFrame):
        df.to_csv(file_path / f'{file_name}.csv')
    else:
        raise ValueError(f"Data is type {type(df)}. Save method unknown.")

    return
