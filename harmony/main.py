import time
from os import path, getenv
from distutils.util import strtobool
from core_config import CoreConfig
from git_repo import GitRepo
from k8s_cluster import KubernetesCluster
from project import Project

projects = CoreConfig('conf.yaml', '../').get_projects()
cluster = KubernetesCluster(strtobool(getenv('VERIFY_SSL')),
                            getenv('K8S_API_SERVER_HOST'),
                            getenv('K8S_API_KEY'))


def run():
    for project in projects.keys():

        version_file_name = projects[project]['version_file_name']
        name = projects[project]['name']
        version_file_path = projects[project]['version_file_path']
        git_url = projects[project]['git_url']
        git_branch = projects[project]['git_branch']
        app_label = projects[project]['app_label']
        app_namespace = projects[project]['app_namespace']

        repo = GitRepo(name,
                       git_url,
                       git_branch,
                       './')

        if path.isdir(name):
            repo.pull_git_repo()
        else:
            repo.clone_git_repo()

        app = Project(name,
                      version_file_name,
                      version_file_path,
                      git_url)

        deployment = cluster.get_deployment(app_namespace, app_label)

        image_name = deployment.spec.template.spec.containers[0].image.split(':')[0]
        image_tag_in_cluster = deployment.spec.template.spec.containers[0].image.split(':')[1]
        image_tag_in_git = app.get_app_version()

        if image_tag_in_git != image_tag_in_cluster:
            cluster.patch_deployment(deployment,
                                     '{0}:{1}'.format(image_name, image_tag_in_git),
                                     deployment.metadata.name,
                                     app_namespace)

            print('''Image version in cluster: {0}, image version in git: {1}. Updating deployment...
                  '''.format(image_tag_in_cluster,
                             image_tag_in_git))
        else:
            print("Nothing was changed. Versions are equal.")


if __name__ == '__main__':
    while True:
        run()
        time.sleep(20)
