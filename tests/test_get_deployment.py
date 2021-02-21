from harmony.k8s_cluster import KubernetesCluster


def test_get_deployment(cluster: KubernetesCluster, ns: str, label: str):
    deployment = cluster.get_deployment(ns, label)
    assert deployment.metadata.labels['app'] == label
    assert deployment.metadata.namespace == ns


test_get_deployment(KubernetesCluster(), 'default', 'nginx')
