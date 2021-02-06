from kubernetes.client import V1Deployment
from k8s_cluster import KubernetesCluster


class KubernetesDeployment:

    def __init__(self, deployment: V1Deployment) -> None:
        self.deployment = deployment

    def get_deployment_name(self) -> str:
        return self.deployment.metadata.name

    def get_container_name(self) -> str:
        return self.deployment.spec.template.spec.containers[0].name

    def get_container_image_name(self) -> str:
        return self.deployment.spec.template.spec.containers[0].image

    def get_container_image_tag(self) -> str:
        return self.deployment.spec.template.spec.containers[0].image.split(':')[1]


deploy = KubernetesDeployment(KubernetesCluster(True).get_deployment('default', 'nginx'))
print(deploy.get_container_image_tag())

