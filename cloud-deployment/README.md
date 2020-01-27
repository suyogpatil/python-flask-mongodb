# Description

**Deployment flow**
This deployment is for production level and can be deployed in any cloud solution having kubernetes.
Kubernetes will take care of update using rolling strategy(https://kubernetes.io/docs/tasks/run-application/rolling-update-replication-controller/) for `birthday-app` deployment and stateful deployment(https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies) for `mongodb`.


**Note on mongodb:**
We have not added replicaset based high availability mongodb settings as its out of scope for this solution and separate topic of its own.But I've attached ideal application design diagram in cloud environment where high availability mongodb cluster is used.

**System diagram**
![alt text](https://raw.githubusercontent.com/suyogpatil/python-flask-mongodb/master/cloud-deployment/python_flask.png)

## Requirements

  - Cloud hosted kubernetes (GKE,AKS,EKS etc.) access is needed

  - Setup load balancer settings for kubernetes in cloud provider(https://kubernetes.io/docs/tasks/access-application-cluster/configure-cloud-provider-firewall/#restrict-access-for-loadbalancer-service)



## Limitations

  - Standalone mongodb instance without authentication (Need extra configuration for authentication and cluster mode.Out of scope for this testing)

  - for persistent storage of mongodb we have used hostpath but we can use advanced storage solutions(https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)


## Procedure to deploy

```
# Check kubernetes cluster
kubectl cluster-info
kubectl get nodes

# Start mongodb
kubectl apply -f kubernetes/k8s-cloud-mongodb.yml

# check mongodb is running
kubectl get all -n birthday-mongodb


# For cloud deployment I have already pushed image to `suyogpatil36/birthday-app` and updated `kubernetes/k8s-cloud-app.yml` so you can skip below docker build and push image part.If you want to use your own docker repo image then follow below steps
    # Build image
    docker build -t birthday-app ../docker/
    # Push image to public docker repo
    docker login --username={yourhubusername} --email={youremail@company.com}
    docker tag birthday-app {yourhubusername}/birthday-app
    docker push {yourhubusername}/birthday-app

# Run birthday-app
kubectl apply -f kubernetes/k8s-cloud-app.yml

# Check that birthday-app is running
kubectl get all -n birthday-app

APP_URL=$(kubectl get service birthday-app-svc -n birthday-app -ojsonpath='{.status.loadBalancer.ingress[].ip}')

# Sample data insert
curl -i -X PUT -H "Content-Type:application/json" \
   -d '{"dateOfBirth": "2018-01-02"}' \
   ${APP_URL}:8080/hello/userX

# Check data
curl ${APP_URL}:8080/hello/userX
```
