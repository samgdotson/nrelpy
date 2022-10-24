import numpy as np
import sys
import os
import pandas as pd


with open("C:/Users/samgd/Research/nrel_api_key.txt", 'r') as file:
    key = file.readlines()[0]

PERSONAL_DATA = {'api_key': None,
                 'name': None,
                 'reason': None,
                 'affiliation': None,
                 'email': None,
                 'mailing_list': None}

PARAMETERS = {'lat': None,
              'lon': None,
              'year': None,
              'leap_day': None,
              'selector': None,
              'utc': None,
              'interval': None,
              'attr_list': None}

AVAILABLE_ATTRIBUTES = {
    "solar": [
        "air_temperature",
        "clearsky_dhi",
        "clearsky_dni",
        "clearsky_ghi",
        "cloud_type",
        "dew_point",
        "dhi",
        "dni",
        "fill_flag",
        "ghi",
        "ghuv-280-400",
        "ghuv-285-385",
        "relative_humidity",
        "solar_zenith_angle",
        "surface_albedo",
        "surface_pressure",
        "total_precipitable_water",
        "wind_direction",
        "wind_speed"],
    "wind": [
        "pressure_0m",
        "pressure_100m",
        'pressure_200m',
        "relativehumidity_2m",
        "precipitationrate_0m",
        "windspeed_10m",
        "windspeed_40m",
        "windspeed_60m",
        "windspeed_80m",
        "windspeed_100m",
        "windspeed_120m",
        "windspeed_140m",
        "windspeed_160m",
        "windspeed_200m",
        "winddirection_10m",
        "winddirection_40m",
        "winddirection_60m",
        "winddirection_80m",
        "winddirection_100m",
        "winddirection_120m",
        "winddirection_140m",
        "winddirection_160m",
        "winddirection_200m",
        "temperature_10m",
        "temperature_40m",
        "temperature_60m",
        "temperature_80m",
        "temperature_100m",
        "temperature_120m",
        "temperature_140m",
        "temperature_160m",
        "temperature_200m"]}


def make_wkt(selector, lat, lon):
    """
    This function generates a well known text (wkt)
    string for use with the NREL API.

    Parameters
    ----------
    selector : String
        Indicates how you want to access the data.
        Accepts: 'POINT', 'MULTIPOINT', 'POLYGON'
    lat : Float or List
        The latitude, or set of latitudes, of interest.
    lon : Float or List
        The longitude, or set of longitudes, of interest.

    Returns
    -------
    wkt : String
        The well known text string.
    """

    method = selector.upper()

    if method == 'POINT':
        wkt = '{method}({lat}%20{lon})'.format(method=method,
                                               lon=lon,
                                               lat=lat)
    else:
        try:
            combinations = [f'{i}%20{j}' for i, j in zip(lon, lat)]
        except ValueError:
            "Longitude and Latitudes are different sizes."
        coord_list = ('%2C').join(combinations)
        wkt = "{method}({coordinates})".format(method=method,
                                               coordinates=coord_list)

    return wkt


def make_nrel_url(parameters, personal_data, kind='solar', format="csv"):
    """
    This function generates a url to access renewable energy
    data through the NREL API. This function requires your
    personal API key. If you want to sign up with NREL and
    get your own API key, visit this website:
    https://developer.nrel.gov/signup/

    Parameters
    ----------
    parameters : dictionary
        This dictionary contains all of the information about
        the dataset you wish to download. Required values are:
        * 'lon' : The longitude of the location of interest, float or list
        * 'lat' : The latitude of the location of interest, float or list
        * 'year' : The year of interest, integer
        * 'leap_day' : Boolean. If 'true', includes leap day.
        * 'utc' : Boolean. If 'true', uses the time at the location.
                  Else, uses your local time.
        * 'selector' : String. Indicates how you want to access the
                       data. Accepts: 'POINT', 'MULTIPOINT', 'POLYGON'
        * 'interval' : String or integer. The desired resolution in minutes.
                       For solar, resolutions are: 30 or 60
                       For wind, resolutions are: 5, 10, 15, 30, or 60
        * 'attr_list' : List. The list of desired columns in your dataset.

    personal_data : dictionary
        This dictionary contains all of the information about
        the user seeking data. Required values are:
        * 'api_key' : The API key generated for you by NREL
        * 'name' : The name of the user
        * 'reason' : How you will use the data
        * 'affiliation' : The institution you are affiliated with
        * 'mailing_list' : 'true' or 'false.' If true, will add you
                            to the mailing list.
        * 'email' : The email of the user

    kind : string
        Indicates what kind of data should be downloaded. Currently
        accepts 'solar' or 'wind.' Default is 'solar'.

    format : string
        Indicates data download format. Accepts either 'csv' or
        'json' strings. Default is 'csv.'

    .. warning:
        Only a json format allows simultaneous download of many locations
        and years simultaneously.

    Returns
    -------
    url : string
        A well formed URL to access NREL data.
    """
    databases = {'wind': 'api/wind-toolkit/v2/wind/wtk-download',
                 'solar': 'api/nsrdb/v2/solar/psm3-download'}

    db_to_access = databases[kind.lower()]

    wkt = make_wkt(parameters['selector'],
                   parameters['lon'],
                   parameters['lat'])

    name = personal_data['name'].replace(' ', '+')
    email = personal_data['email']
    key = personal_data['api_key']
    affiliation = personal_data['affiliation'].replace(' ', '+')
    reason = personal_data['reason'].replace(' ', '+')
    mailing_list = str(personal_data['mailing_list']).lower()

    attributes = (',').join(parameters['attr_list'])
    leap_day = str(parameters['leap_day']).lower()
    if isinstance(parameters['year'], int):
        year = parameters['year']
    elif isinstance(parameters['year'], float):
        year = int(parameters['year'])
    elif isinstance(parameters['year'], list):
        years = [str(int(y)) for y in parameters['year']]
        year = (',').join(years)
    interval = int(parameters['interval'])
    utc = str(parameters['utc']).lower()

    # url = ("https://developer.nrel.gov/{db}.{format}?wkt={wkt}&names={year}"
    #        "&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}"
    #        "&email={email}&affiliation={affiliation}&mailing_list={mailing_list}"
    #        "&reason={reason}&api_key={api}&attributes={attr}").format(db=db_to_access,
    #                                                                   wkt=wkt,
    #                                                                   year=year,
    #                                                                   leap=leap_day,
    #                                                                   interval=interval,
    #                                                                   utc=utc,
    #                                                                   name=name,
    #                                                                   email=email,
    #                                                                   affiliation=affiliation,
    #                                                                   mailing_list=mailing_list,
    #                                                                   reason=reason,
    #                                                                   api=key,
    #                                                                   attr=attributes,
    #                                                                   format=format)

    url = (
        f"https://developer.nrel.gov/{db_to_access}.{format}?wkt={wkt}&names={year}"
        f"&leap_day={leap_day}&interval={interval}&utc={utc}&full_name={name}"
        f"&email={email}&affiliation={affiliation}&mailing_list={mailing_list}"
        f"&reason={reason}&api_key={key}&attributes={attributes}")

    return url


def get_nrel_data(
        lat,
        lon,
        years,
        database,
        parameters=PARAMETERS,
        personal_data=PERSONAL_DATA):
    """
    This function collects data using NREL's data API.

    Parameters
    ----------
    lat : float, list of float
        The latitude(s) of the location(s) of interest.
    lon : float, list of float
        The longitude(s) of the location(s) of interest.
    years : int, list of int
        The years of data to be downloaded.
    database : str
        Database of interest. Accepts ['solar', 'wind'].
    parameters : dict
        The parameters that indicate a unique data request.
    personal_data : dict
        The dictionary of personal data.
    """
    frames = []
    for y in list(years):
        parameters['year'] = y
        url = make_nrel_url(parameters=parameters,
                            personal_data=personal_data,
                            kind=database)
        if database == 'solar':
            df = pd.read_csv(url, skiprows=2)
        elif database == 'wind':
            df = pd.read_csv(url, skiprows=1)
        # breakpoint()
        cols = ['Year', 'Month', 'Day', 'Hour', 'Minute']
        df['time'] = pd.to_datetime(df[cols])
        df.drop(columns=cols, inplace=True)
        df.set_index('time', inplace=True)
        frames.append(df)
    full_df = pd.concat(frames, axis=0)

    return full_df


if __name__ == "__main__":
    PERSONAL_DATA = {
        'api_key': key,
        'name': 'Samuel+G+Dotson',
        'reason': 'Research',
        'affiliation': 'University+of+Illinois+at+Urbana+Champaign',
        'email': 'sgd2@illinois.edu',
        'mailing_list': 'false'}
    PARAMETERS = {'lat': 40.09,
                  'lon': -88.26,
                  'year': 2019,
                  'leap_day': 'true',
                  'selector': 'POINT',
                  'utc': 'false',
                  'interval': '30',
                  'attr_list': ['ghi',
                                'dhi',
                                ]}
    years = [2010, 2011, 2012]

    db = 'wind'
    PARAMETERS['attr_list'] = AVAILABLE_ATTRIBUTES[db]
    df = get_nrel_data(40.09, -88.26, years, db, PARAMETERS, PERSONAL_DATA)

    df.to_csv(f'../data//nrel_data_{db}.csv')
