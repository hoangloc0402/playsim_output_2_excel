import pandas as pd
from copy import deepcopy as clone
from collections import OrderedDict 
from typing import Dict, List

from constants import (
    MISSING_VALUE,
    KPI_MUST_HAVE_ATTRS,
    SHIPMENT_MUST_HAVE_ATTRS,
)


def dicts_2_dataframe(dicts: List[Dict],
                      musthave_attrs: List[str] = None) -> pd.DataFrame:
    '''
        Convert a list of dictionary into a dataframe, each dict
            can have a different number of keys.

        The column labels of the output dataframe will be a union of the
            'musthave_attrs' and all the key sets of all dictionaries in dicts.

        The values of one dictionary will be represented as one row on
            the output pandas dataframe.

        Args:
         dicts: All the dict values must be primitive, like this:
            { '5GO': 15600.0, '7GO': 6928.255963025, 'JET': 49980.0, ... }

        musthave_attrs: List of attributes that the dataframe must have.
            This list should be imported from constants.py

        Returns:
            Return value can be either None or a dataframe object.

    '''
    if len(dicts) == 0:
        return None

    # Because each dict can have different number of attributes
    # we need to merge them by first retrieving all the attribute names (keys)
    all_keys = clone(musthave_attrs) if musthave_attrs else list()

    # TODO: this code is really inefficient
    for dictionary in dicts:
        for key in dictionary.keys():
            if key not in all_keys:
                all_keys.append(key)

    pd_columns = ['case No.'] + all_keys

    pd_data = list()
    for index, dictionary in enumerate(dicts):
        data = [index + 1, ]
        for key in all_keys:
            if key in dictionary.keys() and dictionary[key] is not None:
                data.append(dictionary[key])
            else:
                data.append(MISSING_VALUE)
        pd_data.append(data)

    return pd.DataFrame(data=pd_data, columns=pd_columns)


def config_2_dataframe(config_data: List[Dict]) -> pd.DataFrame:
    '''
        Convert data from all config.yaml files into 1 DataFrame object

        Data of each file will be represented as 1 line in the returned DataFrame

        Args:
            config_data (List[Dict]): each dict contains data of one config.yaml file

    '''
    return dicts_2_dataframe(config_data)


def kpi_2_dataframes(kpi_data: List[Dict]) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    '''
        Convert data from all kpi.yaml files into DataFrame objects

        Args:
            kpi_data (List[Dict]): each dict contains data of one kpi.yaml file

        Returns:
            3 dataframes for KPI, Shipment Amount and Shipment Restriction respectively.

    '''
    list_kpi, list_shipment_amount = list(), list()
    list_shipment_restriction, list_ship_kpis = list(), list()

    # TODO: These loops make it so complicated
    # For each kpi.yaml file
    for data in kpi_data:
        list_kpi.append(dict())
        # For each key, val in one kpi.yaml file
        for key, val in data.items():
            if isinstance(val, dict):
                if key == 'per_oil_amt':
                    list_shipment_amount.append(val)

                elif key == 'kisei':
                    list_shipment_restriction.append(val)

                elif key == 'ship_KPIs':
                    new_dict = OrderedDict()
                    for ship_name, ship_kpis in val.items():
                        # ship_kpis is a dict
                        for kpi_name, kpi_val in ship_kpis.items():
                            new_key = f'{ship_name}:{kpi_name}'
                            new_dict[new_key] = kpi_val

                    list_ship_kpis.append(new_dict)

            else:
                list_kpi[-1][key] = val

    df_kpi = dicts_2_dataframe(
        list_kpi,
        KPI_MUST_HAVE_ATTRS,
    )
    df_shipment_amount = dicts_2_dataframe(
        list_shipment_amount,
        SHIPMENT_MUST_HAVE_ATTRS,
    )
    df_shipment_restriction = dicts_2_dataframe(
        list_shipment_restriction,
        SHIPMENT_MUST_HAVE_ATTRS,
    )
    df_ship_kpis = dicts_2_dataframe(
        list_ship_kpis,
    )
    return df_kpi, df_shipment_amount, df_shipment_restriction, df_ship_kpis
