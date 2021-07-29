import time
import typer
import logging
import sys

from os import getenv
from distutils.util import strtobool

from . import __version__, __module_name__
from harmony.libs.core_config import CoreConfig
from harmony.libs.version_file_storage import VersionFileStorage
from harmony.libs.k8s_cluster import KubernetesCluster
from harmony.libs.project import Project
from harmony.libs.app import App
from harmony.libs.k8s_deployment import K8sDeployment

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

PROJECTS = CoreConfig(getenv('CONFIG_LOCATION')).get_projects()
CLUSTER = KubernetesCluster(strtobool(getenv('VERIFY_SSL')),
                            getenv('K8S_API_SERVER_HOST'),
                            getenv('K8S_API_KEY'))

cli = typer.Typer(name=__module_name__)


@cli.command(help="Returns Harmony version")
def version() -> str:
    return typer.echo(__version__)


@cli.command(help="Run Harmony")
def run() -> None:
    while True:
        for prj_name, prj_spec in PROJECTS.items():
            project = Project(**prj_spec)

            storage = VersionFileStorage(project.name, project.storage_url, project.version_file_name)

            application = App(project.name, storage.get_version_file_local_path())

            deployment = K8sDeployment(CLUSTER.get_deployment(project.app_name, project.app_namespace))

            image_name = deployment.get_image_name()
            image_tag_in_cluster = deployment.get_image_tag()
            image_tag_in_storage = application.get_app_version()

            if image_tag_in_storage != image_tag_in_cluster:
                CLUSTER.patch_deployment(deployment.get_k8s_spec(),
                                         '{0}:{1}'.format(image_name, image_tag_in_storage),
                                         project.app_name,
                                         project.app_namespace)
                logging.info(f"""
                Image version in cluster: {image_tag_in_cluster}, image version in git: {image_tag_in_storage}. 
                Updating deployment...
                """)
            else:
                logging.info(f"Nothing was changed for {prj_name}. Versions are equal.")
        time.sleep(20)
