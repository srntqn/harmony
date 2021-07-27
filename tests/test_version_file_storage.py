from os import path
from shutil import rmtree
from harmony.libs.version_file_storage import VersionFileStorage
import requests

name = 'mock'
storage_url = 'http://example.com/version.yaml'
version_file_name = 'version.yaml'

storage = VersionFileStorage(name, storage_url, version_file_name)


class MockResponse:
    @property
    def content(self):
        return 'key value'.encode()


def mocked_requests_get(*args, **kwargs):
    return MockResponse()


def test_get_version_file_local_path(monkeypatch):

    monkeypatch.setattr(requests, 'get', mocked_requests_get)

    version_path = path.join(name, version_file_name)
    version_file = storage.get_version_file_local_path()

    assert version_file == version_path

    d = {}

    with open(version_path, 'r') as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    assert d['key'] == 'value'

    rmtree(name)
