from project import Project
from git_repo import GitRepo
from core_config import CoreConfig
from k8s_cluster import KubernetesCluster
from k8s_deployment import KubernetesDeployment
import time
from os import path

projects = CoreConfig('conf.yaml', '../').get_projects()
cluster = KubernetesCluster()


def run():
    for app in projects.keys():

        version_file_name = projects[app]['version_file_name']
        name = projects[app]['name']
        version_file_path = projects[app]['version_file_path']
        git_url = projects[app]['git_url']
        app_label = projects[app]['app_label']
        app_namespace = projects[app]['app_namespace']

        repo = GitRepo(name, git_url, 'master', './')

        if path.isdir(name):
            repo.pull_git_repo()
        else:
            repo.clone_git_repo()

        app = Project(name, version_file_name, version_file_path, git_url)
        deployment = KubernetesDeployment(cluster.get_deployment(app_namespace, app_label))
        image_name = deployment.get_container_image_name()
        deployment_name = deployment.get_deployment_name()

        version_in_cluster = deployment.get_container_image_tag()
        version_in_git = app.get_app_version()

        if version_in_git != version_in_cluster:
            cluster.patch_deployment(deployment.deployment,
                                     '{0}:{1}'.format(image_name, version_in_git),
                                     deployment_name,
                                     app_namespace)

            print('''Version in cluster: {0}, version in git: {1}. Updating deployment...
                  '''.format(version_in_cluster,
                             version_in_git))
        else:
            print("Nothing was changed. Versions are equal.")


if __name__ == '__main__':
    while True:
        run()
        time.sleep(20)
