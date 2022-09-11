from urllib.error import HTTPError
import pandas as pd
import warnings


def as_dataframe(url=None, verbose=False, **kwargs):
    """
    This function downloads the specified Annual Technology Baseline Dataset.
    If this data is used in a research publication, users should cite:

    CITE: Lopez, A. et al. (2012). "U.S. Renewable Energy Technical Potentials:
    A GIS-Based Analysis." NREL/TP-6A20-51946. Golden, CO: National Renewable
    Energy Laboratory.

    Returns
    -------
    df : pandas.DataFrame
        The United States Renewable Energy Technical Potential dataset as a pandas dataframe.
    """
    if url:
        URL = url
    else:
        URL = "https://www.nrel.gov/gis/assets/docs/us-re-technical-potential.xlsx"

    try:
        print(f'Downloading Renewable Energy Technical Potential')
        if not verbose:
            warnings.simplefilter(action='ignore', category=UserWarning)
        df = pd.read_excel(
            URL,
            sheet_name='Data',
            skiprows=1,
            index_col='State')
        print('Download Successful.')

    except HTTPError as err:
        fail_str = (f'Failed to download from URL: {URL}.')
        print(err.code, fail_str)
        raise

    return df
