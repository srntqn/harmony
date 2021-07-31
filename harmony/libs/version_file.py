import requests
import yaml
from os import path, mkdir


class VersionFile:
    def __init__(self, app_name: str, storage_url: str, version_file_name: str) -> None:
        self.app_name = app_name
        self.storage_url = storage_url
        self.version_file_name = version_file_name
        self.version_file = path.join(app_name, version_file_name)

    def get_version_file(self) -> str:

        if not path.exists(self.app_name):
            mkdir(self.app_name)

        r = requests.get(self.storage_url).content

        with open(self.version_file, 'wb+') as f:
            f.write(r)

        return self.version_file

    def get_app_name(self):
        return self.app_name

    def get_app_version(self):
        with open(self.version_file) as file:
            version_file = yaml.load(file, Loader=yaml.FullLoader)
        return version_file['version']
