

# Canary Deployment

## Objective

Implemented a Kubernetes Canary Deployment with stable v1 and canary v2 versions, gradually shifting traffic using pod ratios.

---

## 1. Deploy Stable v1

```bash
kubectl apply -f deployment-stable.yaml
kubectl apply -f service.yaml

kubectl get pods -l app=myapp-canary --show-labels
```

Deployed 9 stable v1 pods and verified that the application was accessible.

### Screenshot 1 — Stable Deployment

![Stable v1 Deployment](screenshots/01-stable.png)

---

## 2. Deploy Canary v2

```bash
kubectl apply -f deployment-canary.yaml

kubectl get pods -l app=myapp-canary --show-labels
```

Test traffic using:

```bash
for i in $(seq 1 20); do
  curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"
done
```

With 9 stable pods and 1 canary pod, approximately 10% of traffic was directed to the canary.

### Screenshot 2 — Canary Traffic Split

![Canary Traffic Split](screenshots/02-canary.png)

---

## 3. Promote Canary

Scale the canary to 9 replicas and the stable deployment to 0:

```bash
kubectl scale deployment app-canary --replicas=9
kubectl scale deployment app-stable --replicas=0
```

Verify that all traffic is now served by the canary:

```bash
for i in $(seq 1 5); do
  curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"
done
```

### Screenshot 3 — Canary Promoted

![Canary Promoted to 100%](screenshots/03-promoted.png)

---

## Result

- Stable v1 deployed with 9 replicas
- Canary v2 deployed with 1 replica
- Approximately 10% traffic routed to canary
- Canary v2 successfully promoted to 100% traffic
- Kubernetes Canary Deployment strategy demonstrated

