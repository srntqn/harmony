import tempfile
from harmony.libs.app import App

version_file_path = tempfile.gettempdir() + '/test_version_file.yaml'
app_name = 'test_project'

app = App(app_name, version_file_path)


def test_get_project_name():
    name = app.get_app_name()
    assert name == app_name


def test_get_app_version():

    with open(version_file_path, "w") as f:
        f.write("version: 1.0.0")

    app_version = app.get_app_version()
    assert app_version == "1.0.0"
