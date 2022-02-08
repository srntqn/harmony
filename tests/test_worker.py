from yaml import dump
from os import path

import tempfile
import requests

import harmony.libs.worker as worker
from tests.test_data import CLUSTER, DEPLOYMENT, IMAGE, PROJECT


class MockResponse:
    @property
    def content(self):
        return 'version: 1.0.0'.encode()


def mocked_requests_get(*args, **kwargs):
    return MockResponse()


def test_read_projects_from_config():

    config_path = path.join(tempfile.gettempdir(), 'test_config.yaml')
    config_data = {
        'nginx': {
            'name': 'nginx',
            'app_namespace': 'default'
        }
    }

    with open(config_path, 'w') as file:
        dump(config_data, file)

    projects = worker.read_projects_from_config(config_path)

    assert projects['nginx']['name'] == 'nginx'
    assert projects['nginx']['app_namespace'] == 'default'


def test_fetch_app_version_from_vcs(monkeypatch):
    vcs_url = 'https://example.com/version.yaml'

    monkeypatch.setattr(requests, 'get', mocked_requests_get)
    version = worker.fetch_app_version_from_vcs(vcs_url)

    assert version == '1.0.0'


def test_sync_versions_in_vcs_and_cluster():
    worker.sync_versions_in_vcs_and_cluster(
        project_name='test',
        project=PROJECT,
        k8s_deployment=DEPLOYMENT,
        image=IMAGE,
        k8s_cluster=CLUSTER
    )

    assert DEPLOYMENT.print_image_tag() == '1.0.1'
