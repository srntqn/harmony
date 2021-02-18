import os
from distutils.util import strtobool
from kubernetes.client import (
    CoreV1Api,
    AppsV1Api,
    V1Deployment,
    Configuration,
    ApiClient
)


class KubernetesCluster:
    def __init__(self) -> None:

        self.configuration = Configuration()

        self.configuration.verify_ssl = strtobool(os.getenv('VERIFY_SSL'))
        self.configuration.host = os.getenv('K8S_API_SERVER_HOST')
        self.configuration.api_key['authorization'] = os.getenv('K8S_API_KEY')
        self.configuration.api_key_prefix['authorization'] = 'Bearer'

        with ApiClient(self.configuration) as api_client:
            self.core = CoreV1Api(api_client)
            self.apps = AppsV1Api(api_client)

    def get_deployment(self,
                       namespace: str,
                       label: str) -> V1Deployment:
        deployments = self.apps.list_namespaced_deployment(watch=False,
                                                           namespace=namespace,
                                                           label_selector='app={0}'.format(label))
        for d in deployments.items:
            return d

    def patch_deployment(self,
                         deployment: V1Deployment,
                         container_tag: str,
                         name: str,
                         namespace: str) -> V1Deployment:
        deployment.spec.template.spec.containers[0].image = container_tag
        return self.apps.patch_namespaced_deployment(name=name,
                                                     namespace=namespace,
                                                     body=deployment)
