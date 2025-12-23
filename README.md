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



Install kind, kubectl, and Helm:
-sudo apt-get update -y
-sudo apt-get install -y ca-certificates curl gnupg lsb-release
-curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
-chmod +x kubectl
-sudo mv kubectl /usr/local/bin/
-curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
-chmod +x kind
-sudo mv kind /usr/local/bin/
-curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
4. Create a Kubernetes cluster in Codespaces
-kind create cluster --name kind-cluster
- kubectl get pods -l app=myk8sapp -w
- kubectl port-forward svc/myk8sapp-svc 8080:80
Open below in browser:
https://crispy-invention-4j65pxg9ppg43j794-8080.app.github.dev/ping
5. kubectl get pods -n monitoring -w
run below in different terminal and open browser(popup u will get after running below commands):
- kubectl port-forward -n monitoring svc/monitoring-grafana-c68f5849b-6nc5f 3000:80
browser site: https://crispy-invention-4j65pxg9ppg43j794-3000.app.github.dev/login
ID : admin
Password: PFX1YTHapCigrCYMjk0xVMXeA57OemJ8nW71a5Gg
- kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-operator-5784686955-krh89 9090:9090
browser site: https://crispy-invention-4j65pxg9ppg43j794-9090.app.github.dev/query
run in prometheus tab: 'up' command and 'kube_pod_info
' command




