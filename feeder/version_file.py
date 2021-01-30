import yaml
from os import path


class VersionFile:
    def __init__(self, name: str, path_inside_repo: str):
        self.name = name
        self.path_inside_repo = path_inside_repo

    def get_app_version(self):
        with open(path.join(self.path_inside_repo, self.name)) as file:
            version_file = yaml.load(file, Loader=yaml.FullLoader)
        return version_file['version']

