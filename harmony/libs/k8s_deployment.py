from kubernetes.client import V1Deployment


class K8sDeployment:
    def __init__(self, deployment: V1Deployment) -> None:
        self.deployment = deployment

    def get_k8s_spec(self) -> V1Deployment:
        return self.deployment

    def get_image_name(self) -> str:
        return self.deployment.spec.template.spec.containers[0].image.split(':')[0]

    def get_image_tag(self) -> str:
        return self.deployment.spec.template.spec.containers[0].image.split(':')[1]