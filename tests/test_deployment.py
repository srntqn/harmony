from unittest import mock
from harmony.k8s_cluster import KubernetesCluster

cluster = KubernetesCluster(False,
                            'localhost',
                            'api_key')


def test_list_namespaced_deployment_call_during_get_deployment_call():
    cluster.apps.list_namespaced_deployment = mock.MagicMock()
    cluster.get_deployment('default', 'nginx')
    cluster.apps.list_namespaced_deployment.assert_called_once_with(watch=False,
                                                                    namespace='default',
                                                                    label_selector='app=nginx')


def test_patch_namespaced_deployment_call_during_patch_deployment_call():
    cluster.apps.patch_namespaced_deployment = mock.MagicMock()
    deployment = mock.MagicMock()
    cluster.patch_deployment(deployment,
                             '1.16.0',
                             'nginx-deployment',
                             'default')
    cluster.apps.patch_namespaced_deployment.assert_called_once_with(name='nginx-deployment',
                                                                     namespace='default',
                                                                     body=deployment)
