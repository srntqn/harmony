from kubernetes.client import (
    AppsV1Api,
    V1Deployment,
    Configuration,
    ApiClient
)


class KubernetesCluster:
    def __init__(self,
                 verify_ssl: bool,
                 host: str,
                 api_key: str) -> None:

        self.configuration = Configuration()

        self.configuration.verify_ssl = verify_ssl
        self.configuration.host = host
        self.configuration.api_key['authorization'] = api_key
        self.configuration.api_key_prefix['authorization'] = 'Bearer'

        with ApiClient(self.configuration) as api_client:
            self.apps = AppsV1Api(api_client)

    def fetch_deployment(self,
                         name: str,
                         namespace: str) -> V1Deployment:
        return self.apps.read_namespaced_deployment(name=name, namespace=namespace)

    def patch_deployment(self,
                         deployment: V1Deployment,
                         container_tag: str,
                         name: str,
                         namespace: str) -> V1Deployment:
        deployment.spec.template.spec.containers[0].image = container_tag
        return self.apps.patch_namespaced_deployment(name=name,
                                                     namespace=namespace,
                                                     body=deployment)
