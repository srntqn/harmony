from .k8s_deployment import K8sDeployment
from .k8s_cluster import KubernetesCluster
from .serializers.project import Project
from .serializers.image import Image

import logging


def sync(project_name: str,
         project: Project,
         k8s_deployment: K8sDeployment,
         image: Image,
         k8s_cluster: KubernetesCluster):

    if image.tag_in_vcs != image.tag_in_cluster:
        k8s_cluster.patch_deployment(k8s_deployment.get_k8s_spec(),
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