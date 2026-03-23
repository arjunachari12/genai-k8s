# 02: Creating ArgoCD Applications

## Objective

Create an ArgoCD Application that deploys your existing GenAI Helm chart, establishing GitOps control over your application.

## Prerequisites

- ArgoCD installed and running (from Lab 01)
- Your GenAI Helm chart in `genai-platform/helm/genai-platform/`
- GitHub repository created and code pushed
- ArgoCD UI accessible

## Step-by-step Instructions

### 0. Push Code to GitHub

First, create a GitHub repository and push your code:

```bash
# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/genai-k8s.git
git push -u origin main
```

### 1. Create ArgoCD Application via CLI

Use ArgoCD CLI for better automation:

```bash
# Login to ArgoCD
argocd login localhost:8081 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure

# Create the application
argocd app create genai-platform \
  --repo https://github.com/YOUR_USERNAME/genai-k8s.git \
  --path genai-platform/helm/genai-platform \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace genai-platform \
  --sync-policy automated \
  --self-heal \
  --prune
```

### Alternative: Create via UI

1. Open ArgoCD UI at https://localhost:8081
2. Login with admin credentials
3. Click "New App"
4. Fill in the form:
   - **Application Name**: `genai-platform`
   - **Project**: `default`
   - **Sync Policy**: `Automatic`
   - **Repository URL**: `https://github.com/YOUR_USERNAME/genai-k8s.git` (replace with your repo)
   - **Path**: `genai-platform/helm/genai-platform`
   - **Cluster**: `https://kubernetes.default.svc` (in-cluster)
   - **Namespace**: `genai-platform` (or your app namespace)

### 2. Configure Helm Parameters

In the ArgoCD UI, under "Helm" tab:
- **Values Files**: `values.yaml`
- Add any custom values if needed

### 3. Sync the Application

If using CLI:
```bash
argocd app sync genai-platform
```

Or click "Sync" in the UI and monitor the process.

## Expected Output

- ArgoCD Application created and synced
- Your GenAI application pods redeployed under ArgoCD control
- Application status shows "Synced" in ArgoCD UI

## Validation Steps

1. Check ArgoCD app status:
   ```bash
   kubectl get applications -n argocd
   ```

2. Verify pods are running:
   ```bash
   kubectl get pods -n genai-platform
   ```

3. Check ArgoCD UI for application health.

## Troubleshooting

- **Repository not accessible**: Ensure your GitHub repository exists and is public (or you have proper authentication). Check the repo URL.
- **Helm chart errors**: Validate your Helm chart: `helm template genai-platform/helm/genai-platform/`
- **Sync fails**: Check ArgoCD logs: `kubectl logs -n argocd deployment/argocd-application-controller`
- **CLI login fails**: Ensure port-forward is running: `kubectl port-forward svc/argocd-server -n argocd 8081:443`

## What Just Happened?

You created an ArgoCD Application that connects your Git repository (local Helm chart) to your Kubernetes cluster. ArgoCD now manages the deployment lifecycle of your application.

## Challenge Exercise

Modify a value in your `values.yaml` file and sync the application. Observe how ArgoCD detects and applies the change.