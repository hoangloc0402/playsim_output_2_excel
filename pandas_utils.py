import pandas as pd
from typing import Dict, List

MISSING_VALUE = 'N/A'


def dicts_2_dataframe(data: List[Dict]) -> pd.DataFrame:
    '''
        Convert a list of dictionary into a dataframe, each dict
            can have a different number of keys.

        The values of one dictionary will be represented as one row on
            the output pandas dataframe.

        All the dict values must be primitive, like this:
            { '5GO': 15600.0, '7GO': 6928.255963025, 'JET': 49980.0, ... }

        Returns:
            Return value can be either None or a dataframe object.

    '''
    if len(data) == 0:
        return None

    # Because each dict can have different number of attributes
    # we need to merge them by first retrieving all the attribute names (keys)
    all_keys = list()
    # TODO: this code is really inefficient
    for dictionary in data:
        for key in dictionary.keys():
            if key not in all_keys:
                all_keys.append(key)

    column_labels = ['case No.'] + all_keys

    pd_data = list()
    for index, dictionary in enumerate(data):
        values = [index + 1, ]
        for key in all_keys:
            if key in dictionary.keys():
                values.append(dictionary[key])
            else:
                values.append(MISSING_VALUE)
        pd_data.append(values)

    df = pd.DataFrame(
        data = pd_data,
        columns = column_labels,
    )
    return df


def config_2_dataframe(config_data: List[Dict]) -> pd.DataFrame:
    '''
        Convert data from all config.yaml files into 1 DataFrame object

        Data of each file will be represented as 1 line in the returned DataFrame

        Args:
            config_data (List[Dict]): each dict contains data of one config.yaml file

    '''
    return dicts_2_dataframe(config_data)


def kpi_2_dataframes(kpi_data: List[Dict])-> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    '''
        Convert data from all kpi.yaml files into DataFrame objects

        Args:
            kpi_data (List[Dict]): each dict contains data of one kpi.yaml file

        Returns:
            3 dataframes for KPI, Shipment Amount and Shipment Restriction respectively.

    '''
    list_kpi, list_shipment_amount, list_shipment_restriction = list(), list(), list()

    for data in kpi_data:
        list_kpi.append(dict())
        for key, val in data.items():
            if isinstance(val, dict):
                if key == 'per_oil_amt':
                    list_shipment_amount.append(val)
                elif key == 'kisei':
                    list_shipment_restriction.append(val)
            else:
                list_kpi[-1][key] = val

    df_kpi = dicts_2_dataframe(list_kpi)
    df_shipment_amount = dicts_2_dataframe(list_shipment_amount)
    df_shipment_restriction = dicts_2_dataframe(list_shipment_restriction)

    return df_kpi, df_shipment_amount, df_shipment_restriction
