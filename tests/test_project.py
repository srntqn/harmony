from harmony.project import Project
from os import path

import tempfile

version_file_name = 'test_version_file.yaml'
version_file_path = tempfile.gettempdir()
project_name = 'test_project'

project = Project(project_name,
                  version_file_name,
                  version_file_path,
                  'git@github.com:srntqn/sample_harmony_version_file_source.git')


def test_get_project_name():
    prj_name = project.get_project_name()
    assert prj_name == project_name


def test_get_app_version():
    version_file = path.join(version_file_path, version_file_name)

    with open(version_file, "w") as f:
        f.write("version: 1.0.0")

    app_version = project.get_app_version()
    assert app_version == "1.0.0"
