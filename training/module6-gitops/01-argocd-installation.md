# 01: ArgoCD Installation

## Objective

Install ArgoCD on your KIND cluster and access its web UI to understand the GitOps dashboard.

## Prerequisites

- KIND cluster running with your GenAI application deployed via Helm
- `kubectl` access to the cluster

## Step-by-step Instructions

### 1. Create ArgoCD Namespace

```bash
kubectl create namespace argocd
```

### 2. Install ArgoCD

Apply the official ArgoCD manifests (using a specific version to avoid annotation size issues):

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.10.0/manifests/install.yaml
```

If you encounter annotation size errors, try a different version or use the HA install:

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.9.0/manifests/install.yaml
```

Wait for all pods to be ready:

```bash
kubectl wait --for=condition=Ready pod --all -n argocd --timeout=300s
```

### 3. Install ArgoCD CLI (Optional but Recommended)

```bash
# On Linux
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

### 4. Access ArgoCD UI

Port-forward the ArgoCD server:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

### 5. Get Initial Admin Password
username: admin

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Expected Output

- ArgoCD pods running in `argocd` namespace
- ArgoCD UI accessible at https://localhost:8081 (accept self-signed certificate)
- Login with username `admin` and the password from step 5

## Validation Steps

1. Check ArgoCD pods:
   ```bash
   kubectl get pods -n argocd
   ```
   Should show all pods in Running state.

2. Verify ArgoCD CLI:
   ```bash
   argocd version
   ```

3. Access UI in browser and login.

## Troubleshooting

- **Port-forward fails**: Ensure port 8081 is not in use. Use a different local port if needed.
- **Pods not ready**: Check pod logs: `kubectl logs -n argocd deployment/argocd-server`
- **UI shows certificate error**: This is expected for self-signed cert. Click "Advanced" and "Proceed to localhost".
- **CRD annotation too long error**: Use a specific ArgoCD version instead of 'stable'. Try v2.10.0 or v2.9.0 as shown above. This is a known issue with the stable manifest.

## What Just Happened?

You installed ArgoCD, the GitOps continuous delivery tool for Kubernetes. ArgoCD will monitor your Git repository and keep your cluster in sync with your desired state.

## Challenge Exercise

Explore the ArgoCD UI and note the different sections (Applications, Repositories, Clusters). What do you see in the Clusters section?