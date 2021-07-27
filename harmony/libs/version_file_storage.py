import requests
from os import getcwd, path, mkdir


class VersionFileStorage:
    def __init__(self, app_name: str, storage_url: str, version_file_name: str) -> None:
        self.app_name = app_name
        self.storage_url = storage_url
        self.version_file_name = version_file_name

    def get_version_file_local_path(self) -> str:

        if not path.exists(self.app_name):
            mkdir(self.app_name)

        file_path = path.join(self.app_name, self.version_file_name)

        r = requests.get(self.storage_url)

        print(getcwd())
        with open(file_path, 'wb+') as f:
            f.write(r.content)

        return file_path
