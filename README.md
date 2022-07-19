# nrelpy
Simple API to interact with the National Renewable Energy Laboratory's Annual Technology Baseline

### Installing

This package is not currently available on the Python Package Index (PyPI) so 

1. Clone or download the source code with `git clone <url>`.
2. `pip install .` from the top-level `nrelpy` directory.
3. For contributers, consider `pip install -e .`. 

### Using

The motivation for this API is to relieve researchers of the need to carry datasets
in their repositories. Therefore, the most basic function of `nrelpy` returns a 
dataset as a pandas dataframe. This basic usage is shown below.

```py
import nrelpy.atb as ATB

year = 2022
database = 'electricity'

df = ATB.as_dataframe(year=year, database=database)
```


### Testing

From the top-level `nrelpy` directory, run `pytest`.  