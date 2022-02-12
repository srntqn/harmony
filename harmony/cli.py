import typer

from . import __version__, __module_name__
from .libs.k8s_cluster import KubernetesCluster
from .libs.serializers.config import Config
from .libs.worker import Worker

CONFIG = Config()
CLUSTER = KubernetesCluster(CONFIG.verify_ssl,
                            CONFIG.k8s_api_server,
                            CONFIG.k8s_api_key)


cli = typer.Typer(name=__module_name__)


@cli.command(help="Returns Harmony version")
def version() -> str:
    return typer.echo(__version__)


@cli.command(help="Run Harmony")
def run() -> None:
    worker = Worker(CONFIG, CLUSTER)
    worker.reconciliation_loop()
