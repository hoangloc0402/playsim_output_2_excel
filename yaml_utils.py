import os
import yaml
from typing import Dict, List, Generator


CONFIG_FILE = 'config.yaml'
KPI_FILE = 'kpi.yaml'


class YAML_Data():
    '''
        Object for containing data read from one execution
            directory

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
    with open(path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            if not isinstance(data, dict):
                raise ValueError('Wrong file format!')
            return data

        except yaml.YAMLError as e:
            print(e)


def list_all_public_dirs(path: str) -> List[str]:
    '''
        Args:
            path (str): root path

        Returns:
            dirs (List[str]): list containing all names of public
                subdirectories inside the root directory.

    '''
    dirs = list()
    for dir_entry in os.scandir(path):
        if not dir_entry.is_dir() or dir_entry.name.startswith("."):
            continue
        dirs.append(dir_entry.name)
    return dirs


def get_yaml_data_from_exec_dir(path: str) -> YAML_Data:
    '''
        Read all config and kpi files inside one execution
            directory

        Args:
            path(str): path of an execution directory
        
    '''
    yaml_data = YAML_Data()
    for root, _, files in os.walk(path):
        if CONFIG_FILE not in files or KPI_FILE not in files:
            continue
        config_data = load_yaml_file(
            os.path.join(root, CONFIG_FILE))
        kpi_data = load_yaml_file(
            os.path.join(root, KPI_FILE))
        yaml_data.add(config_data, kpi_data)

    return yaml_data


def iterate_yaml_data_from_root(path: str) -> Generator[str, YAML_Data]:
    '''
        Load data by going through all execution directories

        Args:
            path(str): root path, the directory which contains multiple
                execution directories
        
        Returns:
            A tuple of root_path, name of the execution directory
                and an YAML_Data object
        
    '''
    for exec_dir in list_all_public_dirs(path):
        print(f'LOADING FROM .../{exec_dir}/: START!')
        exec_dir_abs_path = os.path.join(path, exec_dir)
        yaml_data = get_yaml_data_from_exec_dir(exec_dir_abs_path)

        if yaml_data.is_empty():
            print(f'LOADING FROM .../{exec_dir}/: NO DATA!')
            continue
        print(f'LOADING FROM .../{exec_dir}/: DONE!')
        yield exec_dir, yaml_data
