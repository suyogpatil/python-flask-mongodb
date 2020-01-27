# Description

This deployment is for local testing using `minikube` hence high availability is not desired so all the settings are kept
at minimum working condition.


## Requirements

  - Docker,Minikube should be installed

## Limitations

  - Single app

  - Single standalone mongodb instance without authentication


## Procedure to test

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

# Run in minikube
kubectl apply -f kubernetes/k8s-minikube-app.yml

# Check that app is running
kubectl get all -n birthday-app

APP_URL=$(minikube service birthday-app-svc -n birthday-app --url)

# Sample data insert
curl -i -X PUT -H "Content-Type:application/json" \
   -d '{"dateOfBirth": "2019-11-02"}' \
   ${APP_URL}/hello/userX

# Check data
curl ${APP_URL}/hello/userX
```
