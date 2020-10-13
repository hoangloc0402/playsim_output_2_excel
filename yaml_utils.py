import os
import re
import yaml
from typing import Dict, List


CONFIG_FILE = 'config.yaml'
KPI_FILE = 'kpi.yaml'


class YAML_Data():
    '''
        Object for containing data read from one execution directory.

    '''
    # Each dictionary contains data read from 1 yaml file
    config: List[Dict]
    kpi: List[Dict]

    def __init__(self) -> None:
        self.config = list()
        self.kpi = list()

    def add(self, config_data: Dict, kpi_data: Dict) -> None:
        self.config.append(config_data)
        self.kpi.append(kpi_data)

    def is_empty(self) -> bool:
        return len(self.config) == len(self.kpi) == 0


def load_yaml_file(path: str) -> Dict:
    '''
        Read the config.yaml or kpi.yaml file located at
            the provided path and return it as a dictionary

    '''
    try:
        with open(path, 'r') as stream:
            data = yaml.safe_load(stream)
            if not isinstance(data, dict):
                raise ValueError(f'{path} has unsupported format!')
            return data

    except yaml.YAMLError as e:
        print(e)


def list_all_public_dirs(path: str, sort=False) -> List[str]:
    '''
        List all public subdirectories inside the provided root.

        Args:
            path(str): root path
            sort(bool): if True, sort the list of directory.

        Returns:
            dirs (List[str]): list containing all names of public
                subdirectories inside the root directory.

    '''

    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    dirs = list()
    for dir_entry in os.scandir(path):
        if not dir_entry.is_dir() or dir_entry.name.startswith("."):
            continue
        dirs.append(dir_entry.name)
    if sort:
        dirs = sorted_alphanumeric(dirs)
    return dirs


def get_yaml_data_from_branch_dir(path: str) -> YAML_Data:
    '''
        Read all config and kpi files inside the provided branch directory.

        Args:
            path(str): path of a branch directory

    '''
    yaml_data = YAML_Data()
    count = 1

    print(f'LOADING BRANCH {path}/: START!')

    for sub_dir in list_all_public_dirs(path, sort=True):
        config_path = os.path.join(path, sub_dir, CONFIG_FILE)
        kpi_path = os.path.join(path, sub_dir, KPI_FILE)
        if not os.path.exists(config_path) or not os.path.exists(kpi_path):
            print(f'\t    Skipped .../{sub_dir}/')
            continue
        print(f'\t[{count}] Reading .../{sub_dir}/')
        count += 1
        config_data = load_yaml_file(config_path)
        config_data['execution_folder'] = sub_dir
        kpi_data = load_yaml_file(kpi_path)
        yaml_data.add(config_data, kpi_data)

    if yaml_data.is_empty():
        print(f'LOADING BRANCH {path}/: NO DATA!\n')
    else:
        print(f'LOADING BRANCH {path}/: DONE!\n')
    return yaml_data
