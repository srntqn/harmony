from harmony.k8s_cluster import KubernetesCluster
from unittest import mock


def test_list_namespaced_deployment_call_during_get_deployment_call():
    cluster = KubernetesCluster()
    cluster.apps.list_namespaced_deployment = mock.MagicMock()
    cluster.get_deployment('default', 'nginx')
    cluster.apps.list_namespaced_deployment.assert_called_once_with(watch=False,
                                                                    namespace='default',
                                                                    label_selector='app=nginx')
