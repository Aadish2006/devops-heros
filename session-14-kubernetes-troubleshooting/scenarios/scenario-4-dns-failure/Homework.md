# Scenario 4: DNS Failure

The client tries to reach a Service hostname that does not exist.

1. Apply `broken.yaml`; inspect the Pod with `kubectl get pod fail-4-dns-failure-pod` and `kubectl logs fail-4-dns-failure-pod`.
2. Use `kubectl exec` with a DNS lookup tool available in the image, or run `curl -v` against the configured URL, to capture the hostname-resolution failure.
3. Change the hostname to a valid Service in your cluster. Confirm resolution and connectivity; for the built-in `kubernetes.default.svc.cluster.local` Service, use HTTPS on port 443. An authorization response still confirms that DNS and the connection succeeded.

## Screenshot Evidence

Save actual terminal captures as `1.png` and `2.png` beside this file.

### Screenshot 1: Failed hostname lookup

![DNS failure diagnosis](1.png)

### Screenshot 2: Valid Service hostname resolves

![DNS recovery](2.png)

**Deliverable:** Both screenshots and a short note distinguishing DNS resolution from application-level success.