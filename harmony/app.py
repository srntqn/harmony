import time
import typer

from os import path, getenv, getcwd
from distutils.util import strtobool

from . import __version__, __module_name__
from harmony.libs.core_config import CoreConfig
from harmony.libs.git_repo import GitRepo
from harmony.libs.k8s_cluster import KubernetesCluster
from harmony.libs.project import Project

WORKDIR = getenv('PROJECTS_DIR')
projects = CoreConfig(getenv('CONFIG_LOCATION')).get_projects()
cluster = KubernetesCluster(strtobool(getenv('VERIFY_SSL')),
                            getenv('K8S_API_SERVER_HOST'),
                            getenv('K8S_API_KEY'))

cli = typer.Typer(name=__module_name__)


@cli.command(help="Returns Harmony version")
def version() -> None:
    typer.echo(__version__)


@cli.command(help="Run Harmony")
def run():
    while True:
        for project in projects.keys():

            name = projects[project]['name']
            version_file_path = projects[project]['version_file_path']
            git_url = projects[project]['git_url']
            git_branch = projects[project]['git_branch']
            app_name = projects[project]['app_name']
            app_namespace = projects[project]['app_namespace']

            repo = GitRepo(name,
                           git_url,
                           git_branch,
                           WORKDIR)

            if path.isdir(WORKDIR + name):
                repo.pull_git_repo()
            else:
                repo.clone_git_repo()

            application = Project(name,
                                  WORKDIR + repo.repo_name + version_file_path,
                                  git_url)

            deployment = cluster.get_deployment(app_name, app_namespace)

            image_name = deployment.spec.template.spec.containers[0].image.split(':')[0]
            image_tag_in_cluster = deployment.spec.template.spec.containers[0].image.split(':')[1]
            image_tag_in_git = application.get_app_version()

            if image_tag_in_git != image_tag_in_cluster:
                cluster.patch_deployment(deployment,
                                         '{0}:{1}'.format(image_name, image_tag_in_git),
                                         app_name,
                                         app_namespace)

                print('''Image version in cluster: {0}, image version in git: {1}. Updating deployment...
                      '''.format(image_tag_in_cluster,
                                 image_tag_in_git))
            else:
                print("Nothing was changed. Versions are equal.")
        time.sleep(20)
