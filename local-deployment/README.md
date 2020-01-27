# Requirements

 - Docker,Minikube should be installed

# Procedure to test

```
# Start minikube
minikube start

# Set docker env
eval $(minikube docker-env)

# Start mongodb
kubectl apply -f k8s-minikube-mongodb.yml

# check mongodb is running
kubectl get deploy -n birthday-mongodb

# Build image
docker build -t birthday-app .

# Run in minikube
kubectl apply -f k8s-minikube-app.yml

# Check that app is running
kubectl get deploy -n birthday-app

APP_URL=$(minikube service birthday-app-svc -n birthday-app --url)

# Sample data insert
curl -i -X PUT -H "Content-Type:application/json" \
   -d '{"dateOfBirth": "2019-11-02"}' \
   ${APP_URL}/hello/test

# Check data
curl ${APP_URL}/hello/test
```
