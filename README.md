# fivpy

A python package to calculate forest inventories.

## Installation

```bash
$ pip install fivpy
```
  
## Usage

- 'fivpy' can be used to perform forest inventories for a dataset containing the columns units (with the sampled units), dbh or cbh (with the diameter or circunference of   the sampled tress) and height (with the height of the sampled trees).

## Examples
``` python
import pandas as pd
from fivpy import RandomSample

# Loading the data
data = pd.read_csv('../src/fivpy/data/data_2.csv', sep=';', decimal=',')

# Creating a inventory instance
inventory_1 = RandomSample(data,
                            unit_area=0.02,
                            sampling_area=11,
                            significance=90,
                            sampling_error=10)

# Calculating inventory atributes
inventory_1.srs_inventory()
```
For more infos and examples of usage please visit **https://fivpy.readthedocs.io/**

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`fivpy` was created by Theilon Macedo. It is licensed under the terms of the MIT license.

## Credits

`fivpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).  

The metodology used here is based on the book 'Dendrometria e Inventário Florestal'. **SOARES, C.P.B.; PAULA NETO. F.; SOUZA, A.L. Dendrometria e inventário florestal. 2. Ed. Viçosa: Editora UFV. 2011. 272 p.**