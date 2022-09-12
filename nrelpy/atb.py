from urllib.error import HTTPError
import pandas as pd
from nrelpy.utils.data_io import check_stored_data, save_local


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
    A class that allows simplified access to the various
    cases and data values.
    """

    def __init__(
            self,
            year,
            database='electricity',
            case='R&D',
            scenario='Moderate',
            crp = '20',
            **kwargs) -> None:
        """
        Initializes the ATB class.

        Parameters
        ----------
        year : int
            Specifies the ATB year
        database : string
            Specifies which ATB database. 
            Accepts ['electricity', 'transportation']
            Default is 'electricity'.
        case : string
            Specifies the technology case. 
            Accepts ['Market', 'R&D']
        scenario : string
            Specifies the technology scenario. 
            Accepts ['Conservative', 'Moderate', 'Advanced']
        crp : string or int
            `crp` stands for "cost recovery period." This parameter only
            influences the levelized cost of electricity (LCOE) 
            calculation. Default is 20 years.
        """

        self.year = year
        self.database = database
        self.case = case
        self.scenario = scenario
        self.crp = crp


    @property
    def dataframe(self):
        """
        Creates a subset of the ATBe according to the settings
        stored as class attributes. Updates whenever a setting
        is changed.
        
        >>> atbe = ATBe(2022)
        >>> print(atbe.dataframe.scenario.unique())
        ['Moderate']
        >>> atbe.scenario = 'Advanced'
        >>> print(atbe.dataframe.scenario.unique())
        ['Advanced']
        """
        df = as_dataframe(year=self.year, database=self.database)
        df = df[(df.core_metric_case == self.case) &
                (df.scenario == self.scenario) &
                (df.crpyears) == str(self.crp)]
        return df


    def get_data(self, 
                technology, 
                core_metric_param, 
                techdetail,
                value_only=True):
        """
        Retrieves a specific piece of technology data.

        Parameters
        ----------
        technology : string
            Specifies the technology. 
        core_metric_param : string
            The parameter of interest.
            Accepts ['CAPEX', 'Fixed O&M', 'Variable O&M', 
                    'Fuel', 'CF', 'LCOE']
        techdetail : string
            A more descriptive parameter to narrow down
            technology selection. For example, `LandbasedWind`
            has data for multiple wind classes (e.g. `Class9`).
            This must be specified in order to distinguish values.
        value_only : boolean
            An optional parameter that indicates whether the
            value is returned as a Unyt object or as the value
            only. Default is True.
        """

        self.dataframe



if __name__ == "__main__":

    
    year = 2022
    atb_class = ATBe(year=2022)

    print(atb_class.scenario)

    print(atb_class.dataframe.scenario.unique())

    atb_class.scenario = 'Advanced'

    print(atb_class.dataframe.scenario.unique())
