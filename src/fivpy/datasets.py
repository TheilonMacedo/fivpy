"""
Module with functions to load the data used in examples.
"""

import pandas as pd


def data_1():
    """
    Loads the data from the board 4.1. - Credits to Soares, Paula Neto & Souza
    (2010).
    The board contains the columns:
        units: the sample units used
        columns: the columns selected from the complete data
        rows: the rows selected from the complete data
        volume: the volume of the sample unit
    Returns:
        data (pandas.DataFrame): The data.

    Examples
    --------
    >>> data_1()

    """
    return pd.read_csv('./src/fivpy/data/data_1.csv', sep=';', decimal=',')


def data_2():
    """
    Loads one of the bult-in datasets with data collected in the Atlantic 
    Forest, Bahia, Brazil.
    The dataset contains the columns:
        n_tree: number of the tree on field
        units: the sample units used
        cbh: circumference at breast height
        height: height of the tree
    Returns:
        data (pandas.DataFrame): The data.

    Examples
    --------
    >>> data_2()

    """
    return pd.read_csv('./src/fivpy/data/data_2.csv', sep=';', decimal=',')

def data_3():
    """
    Loads one of the bult-in datasets with data collected in the Atlantic 
    Forest, Bahia, Brazil.
    The dataset contains the columns:
        n_tree: number of the tree on field
        units: the sample units used
        cbh: circumference at breast height
        height: height of the tree
    Returns:
        data (pandas.DataFrame): The data.

    Examples
    --------
    >>> data_3()

    """
    return pd.read_csv('./src/fivpy/data/data_2.csv', sep=';', decimal=',')
