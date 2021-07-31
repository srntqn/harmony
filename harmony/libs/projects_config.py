import yaml


class ProjectsConfig:
    def __init__(self, config_path: str) -> None:

        self.config_path = config_path

    def get_projects(self):
        with open(self.config_path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config
