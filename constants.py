CONFIG_FILE = 'config.yaml'
KPI_FILE = 'kpi.yaml'

DEFAULT_EXCEL_FILE_NAME = 'playsim_yaml_compiled.xlsx'

# This is used for filling the missing value
# when converting a list of dicts to dataframe
MISSING_VALUE = ''

KPI_MUST_HAVE_ATTRS = [
    'amt', 'cost', 'dist', 'full_loading_dist', 'empty_loading_dist', 'fuel_a_used',
    'fuel_c_used', 'liter_yen', 'num_late', 'total_demand', 'min_rem_steps',
]
SHIPMENT_MUST_HAVE_ATTRS = [
    'PG', 'VP', 'RG', 'KR', 'JET', 'GO', '5GO', '7GO', '7SGO', 'PGA',
    'FRN', 'RLN', 'MHN', 'LCO', 'LGO', 'DWGO', '7SGO', 'MHN', 'DWGO',
]
