from urllib.error import HTTPError
import pandas as pd


def as_dataframe(year, database, verbose=False, **kwargs):
    """
    This function downloads the specified Annual Technology Baseline Dataset.

    Parameters
    ----------
    year : int
        The ATB year
        * ATB Electricity (ATBe) accepts: [2019,2022] -- inclusive
        * ATB Transportation (ATBt) accepts: [2020]
    database : string
        The desired ATB dataset. Accepts: 'electricity', 'transportation'.
    
    Returns
    -------
    df : pandas.DataFrame
        The ATB data as a pandas dataframe.
    """

    atb_urls = {'electricity': f'https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/{year}/ATBe.csv',
                'transportation':f"https://atb-archive.nrel.gov/transportation/{year}/files/{year}_ATB_Data_VehFuels_Download.xlsx"}

    url = atb_urls[database]

    try:
        print(f'Downloading NREL ATB {database} from {year}')
        if database == 'electricity':
            df = pd.read_csv(url, low_memory=False)
        elif database == 'transportation':
            df = pd.read_excel(url, sheet_name='Joined Data for Levelized Calc')
        print('Download Successful.')
        drop_col = ['Unnamed: 0']
        if verbose:
            print(f"Dropping column {drop_col}")
        try:
            df.drop(columns=drop_col, inplace=True)
        except KeyError as err:
            if verbose:
                print(f'No column {drop_col}.')
            else:
                pass
    except HTTPError as err:
        fail_str = (f'Failed to download from URL: {url}.')
        print(err.code, fail_str)
        raise

    return df
