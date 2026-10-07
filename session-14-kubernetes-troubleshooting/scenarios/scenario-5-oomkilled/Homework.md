# Scenario 5: OOMKilled Container

The process allocates far more memory than the container's `20Mi` limit.

1. Apply `broken.yaml`; inspect the Pod with `kubectl get pod fail-5-oomkilled-pod` and `kubectl describe pod fail-5-oomkilled-pod`.
2. Record the container's termination reason and memory limit. Use `kubectl logs --previous` if the container has restarted.
3. Make the workload fit a realistic limit by reducing the allocation and increasing the memory limit to a value appropriate for your cluster. Apply the correction and verify it remains running.

## Screenshot Evidence

Save actual terminal captures as `1.png` and `2.png` beside this file.

### Screenshot 1: OOMKilled termination evidence

![OOMKilled diagnosis](1.png)

### Screenshot 2: Corrected workload running

![OOMKilled recovery](2.png)

**Deliverable:** Both screenshots and a short explanation of how memory limits affect container processes.