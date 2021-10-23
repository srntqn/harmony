from kubernetes.client import V1Deployment
from tests.test_data import DEPLOYMENT


def test_output_k8s_deployment_object():
    assert type(DEPLOYMENT.output_k8s_deployment_object()) == V1Deployment
    assert DEPLOYMENT.output_k8s_deployment_object().metadata.name == 'test'


def test_print_image_name():
    assert DEPLOYMENT.print_image_name() == 'test'


def test_print_image_tag():
    assert DEPLOYMENT.print_image_tag() == '1.0.0'
