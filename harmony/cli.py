import time
import typer
import logging
import sys

from os import getenv

from . import __version__, __module_name__
from .libs.projects_config import ProjectsConfig
from .libs.version_file import VersionFile
from .libs.k8s_cluster import KubernetesCluster
from .libs.serializers.project import Project
from .libs.serializers.config import Config
from .libs.serializers.image import Image
from .libs.k8s_deployment import K8sDeployment

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CONFIG = Config(**{'config_location': getenv('CONFIG_LOCATION'),
                   'verify_ssl': getenv('VERIFY_SSL'),
                   'k8s_api_server': getenv('K8S_API_SERVER_HOST'),
                   'k8s_api_key': getenv('K8S_API_KEY')})

PROJECTS = ProjectsConfig(CONFIG.config_location).get_projects()
CLUSTER = KubernetesCluster(CONFIG.verify_ssl,
                            CONFIG.k8s_api_server,
                            CONFIG.k8s_api_key)

cli = typer.Typer(name=__module_name__)


@cli.command(help="Returns Harmony version")
def version() -> str:
    return typer.echo(__version__)


@cli.command(help="Run Harmony")
def run() -> None:
    while True:
        for prj_name, prj_spec in PROJECTS.items():

            project = Project(**prj_spec)

            version_file = VersionFile(project.name, project.storage_url, project.version_file_name)

            deployment = K8sDeployment(CLUSTER.get_deployment(project.app_name, project.app_namespace))

            version_file.get_version_file()

            image = Image(**{
                'name': deployment.get_image_name(),
                'tag_in_cluster': deployment.get_image_tag(),
                'tag_in_vcs': version_file.get_app_version()
            })

            if image.tag_in_vcs != image.tag_in_cluster:
                CLUSTER.patch_deployment(deployment.get_k8s_spec(),
                                         f'{image.name}:{image.tag_in_vcs}',
                                         project.app_name,
                                         project.app_namespace)
                logging.info(f"""
                Image version in cluster: {image.tag_in_cluster}, image version in git: {image.tag_in_vcs}. 
                Updating deployment...
                """)
            else:
                logging.info(f"Nothing was changed for {prj_name}. Versions are equal.")
        time.sleep(20)
