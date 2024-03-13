from urllib.error import HTTPError
import pandas as pd
import numpy as np
from nrelpy.utils.data_io import check_stored_data, save_local
import warnings

pd.set_option('display.max_columns', None)


def as_dataframe(year, database, verbose=False, **kwargs):
    """
    This function downloads the specified Annual Technology Baseline Dataset.

    Parameters
    ----------
    year : int
        The ATB year * ATB Electricity (ATBe) accepts: [2019,2023] -- inclusive
        * ATB Transportation (ATBt) accepts: [2020]
    database : string
        The desired ATB dataset. Accepts: 'electricity', 'transportation'.
        Default is `electricity`.

    Returns
    -------
    df : pandas.DataFrame
        The ATB data as a pandas dataframe.
    """

    try:
        df = check_stored_data(database=database, year=year)
    except FileNotFoundError:
        atb_urls = {
            'electricity': f'https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/{year}/ATBe.csv',
            'transportation': f"https://atb-archive.nrel.gov/transportation/{year}/files/{year}_ATB_Data_VehFuels_Download.xlsx"}

        url = atb_urls[database]

        try:
            print(f'Downloading NREL ATB {database} from {year}')
            if database == 'electricity':
                df = pd.read_csv(url, low_memory=False)
            elif database == 'transportation':
                df = pd.read_excel(
                    url, sheet_name='Joined Data for Levelized Calc')
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

        save_local(df, database=database, year=year)

    return df


class ATBe(object):
    """
    A class that allows simplified access to the various cases and data values.
    """

    def __init__(
            self,
            year,
            **kwargs) -> None:
        """
        Initializes the ATB class.

        Parameters
        ----------
        year : int
            Specifies the ATB year
            
        Examples
        --------
        The ATBe class makes it easy to access data from the ATBe.
        
        >>> from nrelpy.atb import ATBe
        >>> atbe = ATBe(2023)
        >>> atbe.get_index_values('technology')
        ['Battery',
        'AEO',
        'Biopower',
        'CSP',
        'Coal',
        'CommPV',
        'Geothermal',
        'Hydropower',
        'LandbasedWind',
        'NaturalGas',
        'Nuclear',
        'OffShoreWind',
        'ResPV',
        'UtilityPV']
        
        You can filter data from the ATBe simply passing an index and value
        
        >>> atbe(technology='Nuclear')
        
        or passing an unpacked dictionary
        
        >>> opts = {'technology':'Nuclear',
        >>>         'core_metric_parameter':'LCOE',
        >>>         'core_metric_variable':2024}
        >>> atbe(**opts)
        """
        self.year = year
        self.database = 'electricity'
        self.raw_dataframe = as_dataframe(year=self.year, database=self.database)
        self.dataframe = _atbe_formatter(self.raw_dataframe, self.year)
        
        self.index_names = list(self.dataframe.index.names)
        
    def __call__(self, **kwargs):
        cases = {key:slice(None) for key in self.index_names}
        for k, v in kwargs.items():
            cases[k] = v
        data_slice = tuple(cases.values())
        
        selection = self.dataframe.xs(data_slice).dropna(axis=1, how='all')
        
        return selection
    
    def get_index_values(self, key):
        
        try:
            key_list = self.dataframe.index.get_level_values(key).unique().to_list()
        except KeyError as err:
            msg = f"Key not found. Try one of {print(self.index_names)}"
            raise KeyError(msg)
        
        return key_list

    @property
    def acronyms(self):
        """
        Retrieves a dataset with the long form of acronyms in the `ATBe`.
        Only valid for years in [2021, 2022, 2023].    

        Returns
        -------
        acronyms : :class:`pandas.DataFrame`
            A dataframe of acronyms.
        """
        acro_df = None
        try:
            acro_df = pd.read_html(f"https://atb.nrel.gov/electricity/{self.year}/acronyms")[0]
            acro_df.columns = ['acronym','long name']
            acro_df.set_index("acronym", inplace=True, drop=True)
        except HTTPError as e:
            msg = f"Year {self.year} not in [2021,2022,2023]."
            warnings.warn(msg, RuntimeWarning)
        
        return acro_df
    
    @property
    def variable_units(self):
        """
        A dictionary with the variables as keys and the units as values.
        """
        metrics = self.raw_dataframe['core_metric_parameter'].values
        units = self.raw_dataframe['units'].values
        unit_df = pd.DataFrame.from_dict(dict(zip(metrics,units)), 
                                         orient='index', 
                                         columns=['units']).dropna(axis=0)
        
        return unit_df
   
        
def _atbe_formatter(df, year):
    """
    Creates a pivot table for the ATBe

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        raw ATBe dataframe.
    year : int
        The ATBe year.
    
    Returns
    -------
    pivoted : :class:`pandas.DataFrame`
        A pivoted dataframe.
    """
    
    pivoted = df.pivot_table(index=ATBe_INDEXES[year],
                             columns=ATBe_COLUMNS[year],
                             values='value'
                             )

    return pivoted

ATBe_INDEXES = {
                2019:['core_metric_case', 
                      'crpyears', 
                      'scenario',
                      'technology', 
                      'core_metric_parameter',
                      'core_metric_variable'],
                2020:['core_metric_case', 
                      'crpyears', 
                      'scenario', 
                      'technology', 
                      'core_metric_parameter',
                      'core_metric_variable'],
                2021:['core_metric_case', 
                      'crpyears', 
                      'scenario',
                      'technology',
                      'core_metric_parameter',
                      'core_metric_variable'],
                2022:['core_metric_case', 
                      'crpyears', 
                      'scenario',
                      'technology',
                      'core_metric_parameter',
                      'core_metric_variable'],
                2023:['core_metric_case',
                      'crpyears',
                      'maturity',
                      'scale',
                      'scenario',
                      'technology',
                      'core_metric_parameter',
                      'core_metric_variable',
                      ],
                }

ATBe_COLUMNS = {
                2019:'techdetail',
                2020:'techdetail',
                2021:'display_name',
                2022:'display_name',
                2023:'display_name',
                }