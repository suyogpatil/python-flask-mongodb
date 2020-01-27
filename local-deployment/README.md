# Description

This deployment is for local testing using `minikube` hence high availability is not desired so all the settings are kept
at minimum working condition.


## Requirements

  - Docker,Minikube should be installed


**Note:**
 If you dont have minikube then can test it on katakoda env at https://www.katacoda.com/courses/kubernetes/launch-single-node-cluster

## Limitations

  - Single app (Can be scaled by simply increasing `replicas` in `kubernetes/k8s-minikube-app.yml`)

  - Single standalone mongodb instance without authentication (Need extra configuration for authentication and cluster mode.Out of scope for this testing)

  - Persistent storage claims are fulfilled by Minikube.


## Procedure to deploy

```
# Start minikube
minikube start

# Set docker env
eval $(minikube docker-env)

# Start mongodb
kubectl apply -f kubernetes/k8s-minikube-mongodb.yml

# check mongodb is running
kubectl get all -n birthday-mongodb

# Build image
docker build -t birthday-app ../docker/

# Run birthday-app
kubectl apply -f kubernetes/k8s-minikube-app.yml

# Check that birthday-app is running
kubectl get all -n birthday-app

APP_URL=$(minikube service birthday-app-svc -n birthday-app --url)

# Sample data insert
curl -i -X PUT -H "Content-Type:application/json" \
   -d '{"dateOfBirth": "2019-01-02"}' \
   ${APP_URL}/hello/userX

# Check data
curl ${APP_URL}/hello/userX
```
