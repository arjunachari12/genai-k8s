# Training Modules

## Available Modules

### Module 4: Autoscaling with KEDA and Prometheus Metrics

This module builds on the observability-enabled Helm deployment and teaches custom metrics, Prometheus Adapter, KEDA, and latency-driven autoscaling.

Start here:

[module4-keda/README.md](module4-keda/README.md)

### Module 6: GitOps & Progressive Delivery with ArgoCD

This module builds on the Helm deployment from earlier labs and adds two platform workflows:

- GitOps reconciliation with ArgoCD
- Progressive delivery with Argo Rollouts and Prometheus analysis

Module structure:

1. **ArgoCD Installation** - Set up ArgoCD in the cluster
2. **Creating ArgoCD Applications** - Deploy the Helm chart through ArgoCD
3. **Auto-Sync & Self-Healing** - Enable automated reconciliation
4. **Drift Detection** - Understand and observe drift
5. **Argo Rollouts Installation** - Install the rollouts controller
6. **Canary Deployment** - Trigger a canary rollout in a dedicated demo namespace
7. **Prometheus Analysis** - Add metrics-based rollout validation
8. **Rollback Scenarios** - Handle deployment failures

## Prerequisites

- A running KIND Kubernetes cluster
- Your GenAI application deployed via Helm (from `genai-platform/helm/genai-platform/`)
- GitHub repository created and code pushed
- `kubectl` access to the cluster
- `helm` CLI installed
- `argocd` CLI (we'll install it in Lab 01)

Start here:

[module6-gitops/01-argocd-installation.md](module6-gitops/01-argocd-installation.md)
