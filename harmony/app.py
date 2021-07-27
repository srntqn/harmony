import time
import typer

from os import getenv
from distutils.util import strtobool

from . import __version__, __module_name__
from harmony.libs.core_config import CoreConfig
from harmony.libs.version_file_storage import VersionFileStorage
from harmony.libs.k8s_cluster import KubernetesCluster
from harmony.libs.project import Project


PROJECTS = CoreConfig(getenv('CONFIG_LOCATION')).get_projects()
CLUSTER = KubernetesCluster(strtobool(getenv('VERIFY_SSL')),
                            getenv('K8S_API_SERVER_HOST'),
                            getenv('K8S_API_KEY'))

cli = typer.Typer(name=__module_name__)


@cli.command(help="Returns Harmony version")
def version() -> None:
    typer.echo(__version__)


@cli.command(help="Run Harmony")
def run():
    while True:
        for project in PROJECTS.keys():

            name = PROJECTS[project]['name']
            storage_url = PROJECTS[project]['storage_url']
            version_file_name = PROJECTS[project]['version_file_name']
            app_name = PROJECTS[project]['app_name']
            app_namespace = PROJECTS[project]['app_namespace']

            storage = VersionFileStorage(name, storage_url, version_file_name)

            application = Project(name, storage.get_version_file_local_path())

            deployment = CLUSTER.get_deployment(app_name, app_namespace)

            image_name = deployment.spec.template.spec.containers[0].image.split(':')[0]
            image_tag_in_cluster = deployment.spec.template.spec.containers[0].image.split(':')[1]
            image_tag_in_storage = application.get_app_version()

            if image_tag_in_storage != image_tag_in_cluster:
                CLUSTER.patch_deployment(deployment,
                                         '{0}:{1}'.format(image_name, image_tag_in_storage),
                                         app_name,
                                         app_namespace)

                print('''Image version in cluster: {0}, image version in git: {1}. Updating deployment...
                      '''.format(image_tag_in_cluster,
                                 image_tag_in_storage))
            else:
                print("Nothing was changed. Versions are equal.")
        time.sleep(20)
