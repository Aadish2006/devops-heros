# Blue-Green Deployment

## Objective

Implemented Blue-Green Deployment in Kubernetes using Blue (v1) and Green (v2) environments.

## 1. Deploy Blue & Green

```bash
kubectl apply -f deployment-blue.yaml
kubectl apply -f deployment-green.yaml
kubectl get pods -l app=myapp --show-labels
kubectl apply -f service-blue.yaml
```

Blue was configured as the live environment and Green was running as the standby environment.

![Blue Live](screenshots/01-blue-live.png)

## 2. Switch Traffic to Green

```bash
kubectl apply -f service-green.yaml
curl http://$(minikube ip):30020
kubectl describe svc myapp-service | grep Selector
```

Traffic was successfully switched from Blue (v1) to Green (v2).

![Green Live](screenshots/02-green-switch.png)

## 3. Rollback to Blue

```bash
kubectl apply -f service-blue.yaml
curl http://$(minikube ip):30020
```

Traffic was successfully switched back to Blue (v1).

![Rollback](screenshots/03-blue-rollback.png)

## Result

- Blue (v1) deployed successfully
- Green (v2) deployed successfully
- Traffic switched Blue → Green
- Rollback performed Green → Blue
- Blue-Green deployment successfully demonstrated
