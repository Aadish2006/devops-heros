# Scenario 3: Pending Pod

The Pod requests more CPU and memory than the cluster can provide.

1. Apply `broken.yaml`; record the Pod status.
2. Use `kubectl describe pod fail-3-pending-pod` and `kubectl get nodes` to identify the scheduling constraint in Events.
3. Reduce the resource requests to values your cluster can satisfy, apply the corrected manifest, and verify the Pod is scheduled and Ready.

## Screenshot Evidence

Save actual terminal captures as `1.png` and `2.png` beside this file.

### Screenshot 1: Pending status and FailedScheduling evidence

![Pending Pod diagnosis](1.png)

### Screenshot 2: Corrected requests and running Pod

![Pending Pod recovery](2.png)

**Deliverable:** Both screenshots and a short note explaining why the original requests could not be scheduled.