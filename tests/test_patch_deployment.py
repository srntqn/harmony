from harmony.k8s_cluster import KubernetesCluster
from unittest import mock

cluster = KubernetesCluster()


def test_patch_namespaced_deployment_call_during_patch_deployment_call():
    cluster.apps.patch_namespaced_deployment = mock.MagicMock()
    deployment = cluster.get_deployment('default', 'nginx')
    cluster.patch_deployment(deployment,
                             '1.16.0',
                             'nginx-deployment',
                             'default')
    cluster.apps.patch_namespaced_deployment.assert_called_once_with(name='nginx-deployment',
                                                                     namespace='default',
                                                                     body=deployment)
