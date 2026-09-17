## 1. Deploy Version 1

Commands used:

```bash
kubectl apply -f deployment-v1.yaml
kubectl apply -f service.yaml
kubectl rollout status deployment/app-rolling
kubectl get pods -l app=app-rolling --show-labels
```

### Evidence

![v1 deployment](screenshots/01-v1.png)


## 2. Rolling Update v1 → v2

Commands used:

```bash
kubectl apply -f deployment-v2.yaml
kubectl get pods -l app=app-rolling -w --show-labels
```

During the rollout, v2 pods were created while v1 pods were gradually terminated.

### Evidence

![Rolling update](screenshots/02-rolling-update.png)


## 3. Rollback v2 → v1

Commands used:

```bash
kubectl rollout undo deployment/app-rolling
kubectl rollout status deployment/app-rolling
kubectl get pods -l app=app-rolling --show-labels
```

The application was successfully rolled back to v1.

### Evidence

![Rollback](screenshots/03-rollback.png)
```

