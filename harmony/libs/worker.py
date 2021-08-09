from os import mkdir, path

import logging
import requests
import yaml

from .k8s_deployment import K8sDeployment
from .k8s_cluster import KubernetesCluster
from .serializers.project import Project
from .serializers.image import Image


def read_projects_from_config(config_path: str):

    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config


def fetch_app_version_from_vcs(vcs_url: str) -> str:

    r = yaml.load(requests.get(vcs_url).content, Loader=yaml.FullLoader)

    return r['version']


def sync_versions_in_vcs_and_cluster(project_name: str,
                                     project: Project,
                                     k8s_deployment: K8sDeployment,
                                     image: Image,
                                     k8s_cluster: KubernetesCluster):

    if image.tag_in_vcs != image.tag_in_cluster:
        k8s_cluster.patch_deployment(k8s_deployment.output_k8s_deployment_object(),
                                     f'{image.name}:{image.tag_in_vcs}',
                                     project.app_name,
                                     project.app_namespace)

        logging.info(f"""
                Image version for {project_name} in cluster: {image.tag_in_cluster}. 
                Image version for {project_name} in git: {image.tag_in_vcs}. 
                Updating deployment...
                """)
    else:
        logging.info(f"Nothing was changed for {project_name}. Versions are equal.")