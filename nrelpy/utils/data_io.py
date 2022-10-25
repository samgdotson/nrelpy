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
           're_potential': 'NREL_REP', 
           'solar':'NSRDB',
           'wind':'WTK'}


def generate_db_filename(database, year=None, pickled=True, **kwargs):
    """
    This function creates a unique filename for a given database.

    database : string
        The desired ATB dataset. Accepts: 'electricity,' 'transportation,'
        'potential,' 'wind,' 'solar.'
    year : int
        The ATB year
        * ATB Electricity (ATBe) accepts: [2019,2022] -- inclusive
        * ATB Transportation (ATBt) accepts: [2020]
    pickled : boolean
        Inidcates if the file is pickled. Otherwise saved as `.csv`.
    """
    if pickled:
        ext = 'pkl'
    else:
        ext = 'csv'
    
    print(kwargs)
    print(year)

    if ((len(kwargs) == 0) and year):
        file_name = f'{db_opts[database]}_{str(year)}.{ext}'
    elif ((len(kwargs) > 0) and year):
        lon = kwargs['lon']
        lat = kwargs['lat']
        if isinstance(year, list):
            year = ('_').join([str(y) for y in year])
        file_name = f'{db_opts[database]}_{str(lon)}_{str(lat)}_{str(year)}.{ext}'
    else:
        file_name = f'{db_opts[database]}.{ext}'

    return file_name


def check_stored_data(file_name, path=None):
    """
    This function checks for locally saved databases. Assumes the data
    is readable as a :class:`pandas.DataFrame`.

    Parameters
    ----------
    file_name : string
        Which file to search.
    path : string or Path-like
        Users may specify where NRELPy should look for data.

    Returns
    -------
    df : :class:`pandas.DataFrame`
        A pandas dataframe containing the stored data.
    """
    if path:
        search_path = Path(path) / file_name
    else:
        search_path = DATA_PATH / file_name

    file_match = glob.glob(str(search_path))

    if len(file_match) == 1:
        if '.pkl' in file_name:
            df = pd.read_pickle(file_match[0])
        elif '.csv' in file_name:
            df = pd.read_csv(file_match[0], index_col=[0])
    elif len(file_match) == 0:
        raise FileNotFoundError(
            f"{file_name} file not found.")
    else:
        raise NameError(
            f"{file_name} returned multiple copies. Handling method unspecified. \n {file_match}")

    return df


def save_local(df, file_name, path=None):
    """
    This function saves a dataframe in the package data or to a
    locally defined path. It automatically generates a file name
    based on dataset attributes (e.g. name and year) that
    `nrelpy.utils.data_io.check_stored_data` will use to search.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas dataframe containing an NREL dataset.
    file_name : string
        The name of the file to save to -- must include a file extension.
    path : string or Path-like
        Allows users to specify a local directory to save
        their data. Otherwise, data will be saved to package
        data.
    """
    if path:
        file_path = Path(path).resolve()
    else:
        file_path = DATA_PATH

    if '.pkl' in file_name:
        with open(file_path / f'{file_name}.pkl', 'wb') as f:
            dill.dump(df, f)
    elif (isinstance(df, pd.DataFrame) and ('.csv' in file_name)):
        df.to_csv(file_path / f'{file_name}')
    else:
        raise ValueError(f"Data is type {type(df)}. Save method unknown.")

    return
