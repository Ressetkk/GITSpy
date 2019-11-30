# GITSpy
GITSpy is a simple Flask/VueJS application that was made as a way to learn and practice Kubernetes.
It fetches from GitHub API specific information about provided user:

* Username
* Public e-mail (after providing GitHub Personal Access Token)
* Repositories
* Language stats
* Latest commit push activity from repos.

The application is split into two parts - backend and frontend. Each one is a separate application.
Backend is a simple API server that returns scraped information in JSON format.
Frontend shows those information in a user-friendly format.

## Personal Access Token
GitHub restricts API calls per hour and e-mail visibility for non-authenticated users. In order to get more information you need to provide your generated Personal Access Token from [GitHub Settings](https://github.com/settings/tokens).

## Deployment

### Locally
For local run you need to have [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/) installed on your machine. After that just clone the repository and type `docker-compose up -d`. Then the application will be running on http://localhost/.

If you want to build the image from source type:
```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
```

### Kubernetes

There are several yaml files for Kubernetes. `backend-deployment.yml` and `frontend-deployment.yml` define Deployment and service for backend and frontend. Each one of them has 4 replicas and has exposed port 80 for internal routing.

TO deploy the application connect to your cluster via kubectl and issue commands below:
```
kubectl apply -f frontend-deployment.yml
kubectl apply -f backend-deployment.yml
```
The new deployments and services assigned to it will be created and application will be accessible internally. To access the services you need to make ingress rule to route requests to hostname + "/" for frontend and hostname + "/api" for backend.

For GKE the rules in `gitspy-ingress.yml` were used.
```
kubectl apply -f gitspy-ingress.yml
```