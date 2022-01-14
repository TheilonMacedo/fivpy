"""
Tests for the Simple Random Sampling module
"""

import pytest
import pandas as pd
from fivpy.srs import RandomSample


@pytest.fixture
def load_data_1():
    return pd.read_csv('src/fivpy/data/data_1.csv', sep=';', decimal=',')

@pytest.fixture
def load_data_2():
    return pd.read_csv('src/fivpy/data/data_2.csv', sep=';', decimal=',')

def test_get_vol(load_data_2):
    """
    Tests the add_dap function.
    """
    test_inv = RandomSample(load_data_2,
                            unit_area=0.02,
                            sampling_area=11,
                            significance=90,
                            sampling_error=10)
    expected = 7.90
    actual = test_inv.get_vol()["volume"].sum()
    assert expected == pytest.approx(actual, 0.01)

def test_get_sample_size(load_data_1):
    test_inv = RandomSample(load_data_1,
                            unit_area=0.3,
                            sampling_area=46.8,
                            significance=95,
                            sampling_error=20)
    expected = 30
    actual = test_inv.get_sample_size()
    assert expected == actual
    