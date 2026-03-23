# Training Modules

## Available Modules

### Module 4: Autoscaling with KEDA and Prometheus Metrics

This module builds on the observability-enabled Helm deployment and teaches custom metrics, Prometheus Adapter, KEDA, and latency-driven autoscaling.

Start here:

[module4-keda/README.md](module4-keda/README.md)

### Module 6: GitOps & Progressive Delivery with ArgoCD

This hands-on training module builds upon your existing GenAI application deployed via Helm on a KIND Kubernetes cluster. You'll learn to implement GitOps practices using ArgoCD for continuous deployment and Argo Rollouts for progressive delivery strategies.

Module structure:

1. **ArgoCD Installation** - Set up ArgoCD in your cluster
2. **Creating ArgoCD Applications** - Deploy your Helm chart via ArgoCD
3. **Auto-Sync & Self-Healing** - Enable automated reconciliation
4. **Drift Detection** - Understand and observe drift
5. **Argo Rollouts Installation** - Install the rollouts controller
6. **Canary Deployment** - Implement progressive delivery
7. **Prometheus Analysis** - Add metrics-based rollout validation
8. **Rollback Scenarios** - Handle deployment failures

Start here:

[module6-gitops/01-argocd-installation.md](module6-gitops/01-argocd-installation.md)
