from harmony.k8s_cluster import KubernetesCluster
from kubernetes.client import V1Deployment, V1Role
from unittest import mock

cluster = KubernetesCluster()


def test_list_namespaced_deployment_call_during_get_deployment_call():
    cluster.apps.list_namespaced_deployment = mock.MagicMock()
    cluster.get_deployment('default', 'nginx')
    cluster.apps.list_namespaced_deployment.assert_called_once_with(watch=False,
                                                                    namespace='default',
                                                                    label_selector='app=nginx')


def test_return_value_type_is_v1deployment():
    deployment = cluster.get_deployment('default', 'nginx')
    assert type(deployment) == V1Deployment


