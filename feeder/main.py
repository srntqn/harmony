from project import Project
from git_repo import GitRepo
from core_config import CoreConfig
from k8s_cluster import KubernetesCluster
from k8s_pod import KubernetesPod
from time import time
from os import path

projects = CoreConfig('conf.yaml', '../').get_projects()
cluster = KubernetesCluster(True)


def run():
    for app in projects.keys():

        version_file_name = projects[app]['version_file_name']
        name = projects[app]['name']
        version_file_path = projects[app]['version_file_path']
        git_url = projects[app]['git_url']
        app_label = projects[app]['app_label']
        app_namespace = projects[app]['app_namespace']

        repo = GitRepo(name, git_url, 'master', name)

        app = Project(name, version_file_name, version_file_path, git_url)
        pod = KubernetesPod(cluster.get_pod(app_label, app_namespace))

        version_in_cluster = pod.get_container_image_tag()
        version_in_git = app.get_app_version()

        if path.isdir(name):
            repo.pull_git_repo()
        else:
            repo.clone_git_repo()

        if version_in_git != version_in_cluster:
            cluster.delete_pod(app_label, app_namespace)
        else:
            print("Nothing was changed. Versions are equal.")


if __name__ == '__main__':
    while True:
        time.sleep(20)
        run()
