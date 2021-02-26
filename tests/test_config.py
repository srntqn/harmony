import tempfile
from os import path
from yaml import dump
from harmony.core_config import CoreConfig

config_dir = tempfile.gettempdir()
config_name = 'test_config.yaml'

config = CoreConfig(config_name,
                    config_dir)


def test_get_projects():

    config_file = path.join(config_dir, config_name)
    config_data = {
        'nginx': {
            'name': 'nginx',
            'git_url': 'git@github.com:srntqn/sample_harmony_version_file_source.git',
            'git_branch': 'master',
            'version_file_name': 'version.yaml',
            'version_file_path': './nginx',
            'app_label': 'nginx',
            'app_namespace': 'default'
        }
    }

    with open(config_file, 'w') as f:
        dump(config_data, f)

    projects = config.get_projects()
    assert projects['nginx']['name'] == 'nginx'

