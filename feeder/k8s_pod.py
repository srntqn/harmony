from kubernetes.client import V1Pod


class KubernetesPod:

    def __init__(self, pod: V1Pod) -> None:
        self.pod = pod

    def get_pod_name(self):
        return self.pod.metadata.name

    def get_container_name(self):
        return self.pod.spec.containers[0].name

    def get_container_image_name(self):
        return self.pod.spec.containers[0].image

    def get_container_image_tag(self):
        return self.pod.spec.containers[0].image.split(':')[1]
