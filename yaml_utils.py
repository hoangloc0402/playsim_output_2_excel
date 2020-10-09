import os
import yaml
from collections import namedtuple
from typing import Dict, List


YamlTuple = namedtuple('YamlTuple' , 'config kpi')
YAML_FILE_NAMES = YamlTuple('config.yaml', 'kpi.yaml')


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


def list_yaml_paths_inside_exec_dir(path: str):
    '''
        Inspecting through all subdirectory inside the execution
            directory and retrieve paths of all yaml files

        Args:
            path: absolute path to one execution folder

        Returns:
            yaml_paths (List[YamlTuple]): a list of YamlTuple, each
                tuple contains 1 relative path for config and 1 for kpi file

    '''
    yaml_paths = list()

    for sub_dir in list_all_public_dirs(path):
        # Skip is either config file or kpi file is missing

        config_relative_path = os.path.join(sub_dir, YAML_FILE_NAMES.config)
        config_absolute_path = os.path.join(path, config_relative_path)
        if not os.path.exists(config_absolute_path):
            continue

        kpi_relative_path = os.path.join(sub_dir, YAML_FILE_NAMES.kpi)
        kpi_absolute_path = os.path.join(path, kpi_relative_path)
        if not os.path.exists(kpi_absolute_path):
            continue

        yaml_tuple = YamlTuple(config_relative_path, kpi_relative_path)
        yaml_paths.append(yaml_tuple)

    return yaml_paths
