from harmony.libs.serializers.project import Project
from harmony.libs.k8s_cluster import KubernetesCluster
from harmony.libs.k8s_deployment import K8sDeployment
from harmony.libs.serializers.image import Image
from kubernetes.client import V1Deployment, V1ObjectMeta, V1DeploymentSpec, V1Container, V1PodTemplateSpec, V1PodSpec

PROJECT = Project(
    name='test',
    vcs_url='https://example.com',
    app_name='test',
    app_namespace='test-ns'
)

CLUSTER = KubernetesCluster(False,
                            'localhost',
                            'api_key')


def generate_k8s_deployment() -> V1Deployment:
    sample_container = V1Container(name='test', image='test:1.0.0')
    sample_deployment = V1Deployment(api_version='apps/v1',
                                     kind='Deployment',
                                     metadata=V1ObjectMeta(name='test'),
                                     spec=V1DeploymentSpec(selector={'matchLabels': {'app': 'test'}},
                                                           template=(V1PodTemplateSpec(
                                                               spec=V1PodSpec(containers=[sample_container])))
                                                           )
                                     )
    return sample_deployment


DEPLOYMENT = K8sDeployment(generate_k8s_deployment())

IMAGE = Image(
    name='test',
    tag_in_cluster='1.0.0',
    tag_in_vcs='1.0.1'
)
