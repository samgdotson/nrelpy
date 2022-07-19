# nrelpy
Simple API to interact with the National Renewable Energy Laboratory's Annual Technology Baseline

### Installing

This package may be installed with 

`pip install nrelpy`

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


### Contributing

Contributors should clone the repository and install an editable installation.

```bash
git clone https://github.com/samgdotson/nrelpy.git

cd nrelpy

pip install -e .
```

Issues and feature requests are welcome.