import yaml
from os import path


class CoreConfig:
    def __init__(self,
                 config_name: str,
                 path_to_config: str) -> None:
        self.config_name = config_name
        self.path_to_config = path_to_config

    def get_projects(self):
        with open(path.join(self.path_to_config, self.config_name)) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

