# K8S-Deployment-Monitoring-Codespace

A tiny K8s demo app that uses only Python stdlib (no Flask). Includes:
- Dockerfile (no pip installs)
- K8s manifests: Deployment, Service, Ingress, HPA
- Prometheus PrometheusRule + ServiceMonitor + Grafana datasource ConfigMap
- GitHub Actions workflow to build and push image to GHCR and apply manifests

Quick start (local Docker + kind or pushing to GHCR):

1. Build image locally:
   docker build -t myk8sapp:latest ./app

2A. If using kind (local cluster):
   kind create cluster --name demo
   kind load docker-image myk8sapp:latest --name demo
   kubectl apply -f manifests/deployment.yaml
   kubectl apply -f manifests/service.yaml
   kubectl apply -f manifests/ingress.yaml

2B. If pushing to GHCR:
   docker tag myk8sapp:latest ghcr.io/<YOUR_GH_USER>/myk8sapp:latest
   docker login ghcr.io
   docker push ghcr.io/<YOUR_GH_USER>/myk8sapp:latest
   edit manifests/deployment.yaml to set the image to ghcr.io/<YOUR_GH_USER>/myk8sapp:latest
   kubectl apply -f manifests/

3. (Optional) Install ingress-nginx and kube-prometheus-stack via Helm as in project docs.

Endpoints:
- /        -> greeting
- /ping    -> ok JSON
- /healthz -> health for probes
- /metrics -> tiny Prometheus-format metrics

