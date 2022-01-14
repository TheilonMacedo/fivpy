"""Module to perform forest inventories using Simple Random Sampling
"""

import math
import logging
import pandas as pd
from scipy import stats



logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


class RandomSample:
    """Class to create a forest inventory object
    which uses Simple Random Sampling to estimate total volume"""

    def __init__(self,
                 dataframe,
                 unit_area,
                 sampling_area,
                 significance=95,
                 sampling_error=20,
                 deg_free=None):

        self.dataframe = dataframe
        self.unit_area = unit_area
        self.sampling_area = sampling_area
        self.significance = significance
        self.sampling_error = sampling_error
        self.deg_free = deg_free
        self.n_sampled_units = self.dataframe.groupby("units").count().shape[0]
        self._add_vol()
        self._get_deg_free()
        self.mean = self.dataframe.groupby("units").sum().mean()[["volume"]]
        self.std = self.dataframe.groupby("units").sum().std()[["volume"]]
        self.var_coef = self.std / self.mean * 100
        self.total_units = self.sampling_area / self.unit_area
        self.t_value = stats.t.ppf(1 - (1 - (self.significance/100)) / 2, self.deg_free)


    def _add_vol(self):

        try:
            self.get_vol()
            logging.warning('Adding colum with Volume.')
        except KeyError:
            if 'volume' in self.dataframe.columns:
                logging.warning('Volume column already exists.')
                return self.dataframe

            logging.warning('Adding columns with DBH and Volume.')
            self.dataframe["dbh"] = self.dataframe["cbh"] / math.pi
            self.get_vol()

        return self.dataframe

    def get_vol(self, beta_0=0.000074, beta_1=1.707348, beta_2=1.16873):
        """Add a column with volume info to the dataframe

        Args:
            beta_0 (float, optional): first parameter. Defaults to 0.000074.
            beta_1 (float, optional): second parameter. Defaults to 1.707348.
            beta_2 (float, optional): third parameter. Defaults to 1.16873.

        Returns:
            dataframe (pd.DataFrame): A DataFrame containing volume info.

        Examples
        --------
        >>> instance.get_vol()
        ### To change the equation used to calculate volume
        >>> instance.get_vol(beta_0=0.000025, beta_1=1.4568, beta_2=1.2563)

        """
        self.dataframe["volume"] = beta_0 * (self.dataframe["dbh"] ** beta_1)\
            * (self.dataframe["height"] ** beta_2)
        return self.dataframe

    def _get_deg_free(self):
        # Get the degrees of freedom
        if self.deg_free is None:
            self.deg_free = self.n_sampled_units - 1
            logging.warning("Degrees of freedom not informed."
                            "Using default value: %s", self.deg_free)
        return self.deg_free

    def get_sample_size(self):
        """Returns the estimated required sample size to perform the
        definitive inventory

        Returns:
            sample size (int): the required sample size

        Examples
        --------
        >>> instance.get_sample_size()
        """
        dividend_sample_size = ((self.t_value ** 2) * (self.var_coef ** 2))
        divisor_sample_size = (self.sampling_error ** 2) + (((self.t_value\
            ** 2) * (self.var_coef ** 2)) / self.total_units)
        sample_size = dividend_sample_size / divisor_sample_size
        return math.ceil(sample_size)

    def srs_inventory(self):
        """Performs the Simple Random Sampling inventory

        Raises:
            ValueError: If the required sample size is greater than the number
            of units sampled, it is not possible to perform the inventory.

        Returns:
            dataframe (pd.DataFrame): A DataFrame containing the inventory
            results.

        Examples
        --------
        >>> instance.srs_inventory()
        """
        if self.get_sample_size() > self.n_sampled_units:
            raise ValueError("Required sample size is greater than "
                             "the number of sampled units "
                             f"{self.get_sample_size()}. "
                             "It is necessary to obtain more data")

        logging.info("Calculating final inventory.")
        var = self.dataframe.groupby("units").sum().var()[["volume"]]

        # standardized error of mean - sem
        sem = math.sqrt(((var / self.n_sampled_units) * (1 -\
            (self.n_sampled_units / self.total_units))))
        total_vol = self.total_units * self.mean
        sample_error = sem * self.t_value
        sample_error_perc = (sample_error / self.mean) * 100

        # CI true mean
        ic_up = self.mean + sample_error
        ic_lo = self.mean - sample_error

        # CI prod by ha
        mean_ha = self.mean * (1 / self.unit_area)
        ic_pop_up = (self.mean + sample_error) * (1 / self.unit_area)
        ic_pop_lo = (self.mean - sample_error) * (1 / self.unit_area)

        # CI vol total pop
        ic_pop_total = self.total_units * self.mean
        ic_pop_up_total = (self.total_units * self.mean) + \
            (self.total_units * sample_error)
        ic_pop_lo_total = (self.total_units * self.mean) - \
            (self.total_units * sample_error)

        t_value_uni = stats.t.ppf(1 - ((1 - (self.significance/100)) * 2) \
            / 2, self.deg_free)

        # Minimum Reliable Estimate - mre
        mre = self.mean - (t_value_uni * sem)
        mre_population = (self.mean - (t_value_uni * sem)) * self.total_units

        results = {"Variáveis": ["Ym", "DesvPad", "CV", "S²", "N parcelas",
                                 "N Total", "ErrMédia", "V Total",
                                "Err", "E(%)", "IC Supe", "IC Infe", "Ym/ha",
                                "IC Supe ha", "IC Infe ha",
                                "Ym/total", "IC Supe total",
                                "IC Infe total", "EMC", "EMC Pop"],
                "Dados": [self.mean.item(), self.std.item(),
                          self.var_coef.item(), var.item(), self.deg_free,
                          self.total_units,
                            sem, total_vol.item(), sample_error,
                            sample_error_perc.item(), ic_up.item(),
                            ic_lo.item(), mean_ha.item(), ic_pop_up.item(),
                            ic_pop_lo.item(), ic_pop_total.item(),
                            ic_pop_up_total.item(), ic_pop_lo_total.item(),
                            mre.item(), mre_population.item()]}

        return pd.DataFrame(data=results)
