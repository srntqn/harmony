from kubernetes import client, config
from kubernetes.client.rest import ApiException
from requests.auth import HTTPBasicAuth
from requests import get
from argparse import ArgumentParser
import time
import os
import json


parser = ArgumentParser()
parser.add_argument('--privateRegistry', action="store_true", default=False)


config.load_incluster_config()  # for execution inside k8s cluster
# config.load_kube_config()  # for local execution
app = os.environ['APP']
ns = 'default'
core = client.CoreV1Api()
apps = client.AppsV1Api()


def getToken():
    image_name = getContainerImageName()
    url = (f'https://auth.docker.io/token?scope=repository:{image_name}:' +
           'pull&service=registry.docker.io')
    if parser.parse_args().privateRegistry is True:
        return get(url, auth=HTTPBasicAuth(os.environ['docker_user'],
                   os.environ['docker_password'])).json()['token']
    else:
        return get(url).json()['token']


def getRegistryImageId():
    image_name = getContainerImageName()
    token = getToken()
    headers = {
        'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
        'Authorization': f'Bearer {token}'
    }
    manifest = ('https://registry-1.docker.io/v2/' +
                f'{image_name}/manifests/latest')
    r = get(url=manifest, headers=headers)
    return r.headers['Docker-Content-Digest']


def checkImageUpdate():
    i = getContainerImageName()
    current_image_id = getCurrentImageId()
    pulled_image_id = getRegistryImageId()
    if current_image_id == pulled_image_id:
        print(f'No changes for {i}')
    else:
        deletePod()
        print(f'{i} have changes. New pod is created.')


def run():
    while True:
        time.sleep(20)
        checkImageUpdate()


if __name__ == '__main__':
    run()
