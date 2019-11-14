import os

import yaml

from logger.logger import logger


class Configuration(object):

    def __init__(self, file_dir):
        with open(file_dir) as f:
            data = yaml.safe_load(f)
            self.__dict__.update(data)

    def get_property(self, property_path):
        value = self._get_property_from_env(property_path)
        if value is None:
            value = self._get_property_from_application_config(property_path)
        return value

    @staticmethod
    def _get_property_from_env(property_path):
        env_name = Configuration._get_env_name_for_property(property_path)
        return os.environ.get(env_name, None)

    @staticmethod
    def _get_env_name_for_property(property_path: str) -> str:
        path_list = property_path.split(".")
        return "_".join([path.upper() for path in path_list])

    def _get_property_from_application_config(self, property_path: str) -> object:
        path_list = property_path.split(".")

        def _get_property_from_dict(current_path_list: list, current_dict: dict):
            if current_path_list[0] not in current_dict:
                logger.warning("Could not find property [ {} ] in configuration".format(property_path))
                return None
            else:
                if len(current_path_list) == 1:
                    return current_dict.get(current_path_list[0])
                else:
                    return _get_property_from_dict(current_path_list[1:], current_dict.get(current_path_list[0]))

        return _get_property_from_dict(path_list, self.__dict__)
