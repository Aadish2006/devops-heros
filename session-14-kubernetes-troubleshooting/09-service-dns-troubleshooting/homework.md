# Service and DNS Troubleshooting Homework

## Objective

Trace an in-cluster request from a client Pod through Kubernetes DNS and a Service to its selected Pods, then diagnose a selector mismatch.

## Tasks

1. Apply `deployment.yaml` and `service.yaml`. Verify the Pods are Ready and `web-service` has Pod IPs in its endpoints.
2. Apply `dns-test-pod.yaml`. From `dns-test`, resolve `web-service` and request `http://web-service`.
3. Apply `broken-service.yaml`. Compare its selector with the application Pod labels and verify `broken-service` has no endpoints.
4. Explain the difference between a DNS lookup failure, an empty Service endpoint list, and an application response failure.
5. Remove the broken Service and confirm the healthy Service still has endpoints and serves the Nginx page.

## Commands to Capture

```bash
kubectl get pods --show-labels
kubectl get services
kubectl get endpoints web-service
kubectl exec dns-test -- nslookup web-service
kubectl exec dns-test -- wget -qO- http://web-service
kubectl get endpoints broken-service
kubectl describe service broken-service
```

## Screenshot Evidence

Capture your own terminal output after running the exercise. Save the screenshots beside this file using these names.

### Screenshot 1: Healthy Service, Endpoints, and DNS/HTTP test

![Healthy Service and DNS test](1.png)

### Screenshot 2: Broken selector and empty endpoints

![Broken Service investigation](2.png)

**Deliverable:** Both screenshots and a short incident note listing the symptom, evidence, root cause, fix, and verification.