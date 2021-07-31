import tempfile
from yaml import dump
from harmony.libs.projects_config import ProjectsConfig

config_path = tempfile.gettempdir() + '/test_config.yaml'
config = ProjectsConfig(config_path)


def test_get_projects():

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

    with open(config_path, 'w') as file:
        dump(config_data, file)

    projects = config.get_projects()
    assert projects['nginx']['name'] == 'nginx'
