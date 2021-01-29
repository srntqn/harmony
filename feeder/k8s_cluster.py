from kubernetes import config
from kubernetes.client.rest import ApiException
from kubernetes.client import (
    CoreV1Api,
    AppsV1Api,
    V1Pod
)


class KubernetesCluster:
    def __init__(self, local: bool) -> None:
        if local is True:
            self.conf = config.load_kube_config()
        else:
            self.conf = config.load_incluster_config()
        self.core = CoreV1Api
        self.apps = AppsV1Api

    def get_pod(self, namespace: str, label: str) -> V1Pod:
        try:
            pods = self.core().list_namespaced_pod(watch=False, namespace=namespace,
                                                   label_selector=f'app={label}')
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
        for p in pods.items:
            return p

