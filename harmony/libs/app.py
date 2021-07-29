import yaml


class App:
    def __init__(self,
                 app_name: str,
                 version_file_path: str) -> None:

        self.app_name = app_name
        self.version_file_path = version_file_path

    def get_app_name(self):
        return self.app_name

    def get_app_version(self):
        with open(self.version_file_path) as file:
            version_file = yaml.load(file, Loader=yaml.FullLoader)
        return version_file['version']
