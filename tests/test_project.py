import tempfile
from harmony.libs.project import Project

version_file_path = tempfile.gettempdir() + '/test_version_file.yaml'
project_name = 'test_project'

project = Project(project_name, version_file_path)


def test_get_project_name():
    prj_name = project.get_project_name()
    assert prj_name == project_name


def test_get_app_version():

    with open(version_file_path, "w") as f:
        f.write("version: 1.0.0")

    app_version = project.get_app_version()
    assert app_version == "1.0.0"
