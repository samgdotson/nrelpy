[![Build Status](https://github.com/samgdotson/nrelpy/actions/workflows/python-app.yml/badge.svg)](https://github.com/samgdotson/nrelpy/actions/workflows/python-app.yml)
# nrelpy
Simple API to interact with the National Renewable Energy Laboratory's Annual Technology Baseline

## Features and Datasets

`nrelpy` currently enables access to the following datasets:
* Annual Technology Baseline
    - Transportation (2020)
    - Electricity (2019 - 2022)
* GIS Renewable Energy Potential (state-level resolution)

### Installing

This package may be installed from [PyPI](https://pypi.org/project/nrelpy/) with 

`pip install nrelpy`

### Using

The motivation for this API is to relieve researchers of the need to carry datasets
in their repositories. Therefore, the most basic function of `nrelpy` returns a 
dataset as a pandas dataframe. This basic usage is shown below.


#### ATB

```py
import nrelpy.atb as ATB

year = 2022
database = 'electricity'

df = ATB.as_dataframe(year=year, database=database)
```

#### Renewable Potential

```py
import nrelpy.re_potential as REP

df = REP.as_dataframe()
```

### Testing

From the top-level `nrelpy` directory, run `pytest`.  

You can also check the testing coverage with

```bash
pytest --cov-config=.coveragerc --cov=nrelpy
coverage html
```
`coverage html` creates a nicely formatted html page with 
the entire coverage report. Simply open the `htmlcov/index.html` file in your browser.

### Contributing

Contributors should clone the repository and install an editable installation.

```bash
git clone https://github.com/samgdotson/nrelpy.git

cd nrelpy

pip install -e .
```

*All pull requests must include appropriate, passing, tests.*

Issues and feature requests are welcome.
