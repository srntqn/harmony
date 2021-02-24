from harmony.project import Project
from os import path

import tempfile

project = Project('test_project',
                  'test_version_file.yaml',
                  tempfile.gettempdir(),
                  'git@github.com:srntqn/sample_harmony_version_file_source.git')


def test_get_project_name():
    project_name = project.get_project_name()
    assert project_name == 'test_project'


def test_get_app_version():
    version_vile = path.join(tempfile.gettempdir(), "test_version_file.yaml")

    with open(version_vile, "w") as f:
        f.write("version: 1.0.0")

    app_version = project.get_app_version()
    assert app_version == "1.0.0"

