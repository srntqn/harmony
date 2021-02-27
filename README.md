## Prepare local development environment

### Install third-party tools

* Install and configure [docker](https://docs.docker.com/get-docker/)
* Install and configure [skaffold](https://skaffold.dev/docs/install/)
* Install and configure [minikube](https://minikube.sigs.k8s.io/docs/start/)

### Configure k8s 

* Setup RBAC

```
kubectl create serviceaccount harmony
kubectl create clusterrolebinding harmony --clusterrole=admin --serviceaccount=default:harmony
```
* Get harmony service account token

`kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='harmony')].data.token}" | base64 --decode`

* Create secret with harmony service account token

`kubectl create secret generic k8s-api-key --from-literal='api_key={TOKEN}`

### Build and deploy to minikube cluster

* Use skaffold to build a container image and create a deployment in the cluster

`skaffold run`

* Or use skaffold to build and deploy continuously

`skaffold dev`
