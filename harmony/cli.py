import time
import typer

from . import __version__, __module_name__
from .libs.k8s_cluster import KubernetesCluster
from .libs.serializers.project import Project
from .libs.serializers.config import Config
from .libs.serializers.image import Image
from .libs.k8s_deployment import K8sDeployment
from .libs.worker import read_projects_from_config, fetch_app_version_from_vcs, sync_versions_in_vcs_and_cluster

CONFIG = Config()
PROJECTS = read_projects_from_config(CONFIG.config_location)
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

            deployment = K8sDeployment(CLUSTER.fetch_deployment(project.app_name, project.app_namespace))

            version_in_vcs = fetch_app_version_from_vcs(project.vcs_url)

            image = Image(**{
                'name': deployment.print_image_name(),
                'tag_in_cluster': deployment.print_image_tag(),
                'tag_in_vcs': version_in_vcs
            })

            sync_versions_in_vcs_and_cluster(prj_name,
                                             project,
                                             deployment,
                                             image,
                                             CLUSTER)

        time.sleep(20)
