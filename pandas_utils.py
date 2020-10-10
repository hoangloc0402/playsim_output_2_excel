import os
import pandas as pd
from typing import Dict, List


def config_2_dataframe(config_data: List[Dict])-> pd.DataFrame:
    '''
        Convert data from all config.yaml files into 1 DataFrame object
        
        Data of each file will be represented as 1 line in the returned
            DataFrame
        
        Args:
            config_data (List[Dict]): each dictionary contains data of one
                config.yaml file
    
    '''
    if len(config_data) == 0:
        raise ValueError('No data to convert!')

    column_labels = ['index'] + list(config_data[0].keys())

    pd_data = list()
    for index, data in enumerate(config_data):
        values = [index] + list(data.values())
        pd_data.append(values)
    
    df = pd.DataFrame(
        data = pd_data,
        columns = column_labels,
    )
    return df


def kpi_2_dataframe(kpi_data: List[Dict])-> pd.DataFrame:
    '''
        Convert data from all kpi.yaml files into 1 DataFrame object
        
        Args:
            kpi_data (List[Dict]): each dictionary contains data of one
                kpi.yaml file
    
    '''
    pass
    
    