from cmath import log
import logging
import requests
import sys
import yaml
import time

from .k8s_deployment import K8sDeployment
from .k8s_cluster import KubernetesCluster
from .serializers.project import Project
from .serializers.image import Image
from .serializers.config import Config

logging.basicConfig(stream=sys.stdout,
                    level=logging.getLevelName(Config().log_level))

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self,
                 config: Config,
                 k8s_cluster: KubernetesCluster) -> None:
        self.config = config
        self.k8s_cluster = k8s_cluster

    def _read_projects_from_config(config_path: str):

        with open(config_path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        logger.info(f"Reading the following projects data: {config}")

        return config


    def _fetch_app_version_from_vcs(vcs_url: str) -> str:

        r = yaml.load(requests.get(vcs_url).content, Loader=yaml.FullLoader)

        logger.debug(f"The content of {vcs_url} is {r}")

        return r['version']


    def _sync_versions_in_vcs_and_cluster(project_name: str,
                                         project: Project,
                                         k8s_deployment: K8sDeployment,
                                         image: Image,
                                         k8s_cluster: KubernetesCluster):

        if image.tag_in_vcs != image.tag_in_cluster:
            k8s_cluster.patch_deployment(k8s_deployment.output_k8s_deployment_object(),
                                         f'{image.name}:{image.tag_in_vcs}',
                                         project.app_name,
                                         project.app_namespace)

            logger.info(f"""
                    Image version for {project_name} in cluster: {image.tag_in_cluster}.
                    Image version for {project_name} in git: {image.tag_in_vcs}.
                    Updating deployment...
                    """)
        else:
            logger.info(f"Nothing was changed for {project_name}. Versions are equal.")


    def reconciliation_loop(self) -> None:
        while True:
            for prj_name, prj_spec in self._read_projects_from_config(self.config.config_location).items():

                project = Project(**prj_spec)

                deployment = K8sDeployment(self.k8s_cluster.fetch_deployment(project.app_name, project.app_namespace))

                version_in_vcs = self._fetch_app_version_from_vcs(project.vcs_url)

                image = Image(**{
                    'name': deployment.print_image_name(),
                    'tag_in_cluster': deployment.print_image_tag(),
                    'tag_in_vcs': version_in_vcs
                })

                self._sync_versions_in_vcs_and_cluster(prj_name,
                                                       project,
                                                       deployment,
                                                       image,
                                                       self.k8s_cluster)

            time.sleep(20)

