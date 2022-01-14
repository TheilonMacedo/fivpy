# read version from installed package
from importlib.metadata import version
__version__ = version("fivpy")


from fivpy.srs import RandomSample
from fivpy.datasets import data_1
from fivpy.datasets import data_2
from fivpy.datasets import data_3