**Harmony** is a simple [GitOps](https://www.weave.works/technologies/gitops/) concept implementation.
It is capable to track an application version changes in a git repository and automatically upgrade a Kubernetes workload
to fit the version in a git.

## Prepare local development environment

### Install third-party tools

* Install and configure [helm](https://helm.sh/docs/intro/install/)
* Install and configure [docker](https://docs.docker.com/get-docker/)
* Install and configure [skaffold](https://skaffold.dev/docs/install/)
* Install and configure [minikube](https://minikube.sigs.k8s.io/docs/start/)


### Build and deploy to minikube cluster

* Use skaffold to build a container image and create a deployment in the cluster

`skaffold run`

* Or use skaffold to build and deploy continuously

`skaffold dev`
