import yaml
from os import path


class Project:
    def __init__(self,
                 project_name: str,
                 version_file_name: str,
                 version_file_path: str,
                 git_url: str) -> None:

        self.project_name = project_name
        self.version_file_name = version_file_name
        self.version_file_path = version_file_path
        self.git_url = git_url

    def get_project_name(self):
        return self.project_name

    def get_app_version(self):
        with open(path.join(self.version_file_path, self.version_file_name)) as file:
            version_file = yaml.load(file, Loader=yaml.FullLoader)
        return version_file['version']
