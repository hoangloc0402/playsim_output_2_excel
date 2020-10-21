import os
import argparse

import pandas as pd

from yaml_utils import get_yaml_data_from_branch_dir
from pandas_utils import (
    config_2_dataframe,
    kpi_2_dataframes,
)
from constants import DEFAULT_EXCEL_FILE_NAME


parser = argparse.ArgumentParser()
parser.add_argument("branch_path")
parser.add_argument("-o", "--output_path", help="Specify the output directory")
parser.add_argument("-f", "--file_name", help="Specify name for the output Excel file")

args = parser.parse_args()

BRANCH_PATH = args.branch_path

OUTPUT_PATH = args.output_path if args.output_path else BRANCH_PATH

EXCEL_FILE_NAME = args.file_name if args.file_name else DEFAULT_EXCEL_FILE_NAME

EXCEL_PATH = os.path.join(OUTPUT_PATH, EXCEL_FILE_NAME)


yaml_data = get_yaml_data_from_branch_dir(BRANCH_PATH)

if not yaml_data.is_empty():
    df_config = config_2_dataframe(yaml_data.config)
    df_kpi, df_shipment_amount, df_shipment_restriction, df_ship_kpis = kpi_2_dataframes(yaml_data.kpi)

    df_n_sheet_name = (
        (df_config, '設定条件'),
        (df_kpi, 'KPI'),
        (df_shipment_amount, 'Shipment Amount'),
        (df_shipment_restriction, 'Shipment Restriction'),
        (df_ship_kpis, 'Ship KPIs'),
    )

    print(f'SAVING TO {EXCEL_PATH}: START!')
    with pd.ExcelWriter(EXCEL_PATH) as writer:
        for df, sheet_name in df_n_sheet_name:
            if df is not None:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f'SAVING TO {EXCEL_PATH}: DONE!')
