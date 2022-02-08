from unittest import mock
from tests.test_data import CLUSTER


def test_fetch_deployment_call():
    CLUSTER.apps.read_namespaced_deployment = mock.MagicMock()
    CLUSTER.fetch_deployment('nginx-deployment', 'default')
    CLUSTER.apps.read_namespaced_deployment.assert_called_once_with(name='nginx-deployment',
                                                                    namespace='default')


def test_patch_deployment_call():
    CLUSTER.apps.patch_namespaced_deployment = mock.MagicMock()
    deployment = mock.MagicMock()
    CLUSTER.patch_deployment(deployment,
                             '1.16.0',
                             'nginx-deployment',
                             'default')
    CLUSTER.apps.patch_namespaced_deployment.assert_called_once_with(name='nginx-deployment',
                                                                     namespace='default',
                                                                     body=deployment)
