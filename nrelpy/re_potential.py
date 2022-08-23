from urllib.error import HTTPError
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def as_dataframe(verbose=False, **kwargs):
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
    url = "https://www.nrel.gov/gis/assets/docs/us-re-technical-potential.xlsx"

    try:
        print(f'Downloading Renewable Energy Technical Potential')
        df = pd.read_excel(url, sheet_name='Data', skiprows=1, index_col='State')
        print('Download Successful.')

    except HTTPError as err:
        fail_str = (f'Failed to download from URL: {url}.')
        print(err.code, fail_str)
        raise

    return df
