# Scenario 1: CrashLoop

The Pod exits because its application requires the missing `DATABASE_URL` environment variable.

1. Apply `broken.yaml`; record the Pod status and restart count.
2. Use `kubectl describe pod fail-1-crashloop-pod`, `kubectl logs`, and `kubectl logs --previous` to identify the failure.
3. Add a safe placeholder `DATABASE_URL` value to the Pod environment, apply the corrected manifest, and verify the application reports that it started successfully.

## Screenshot Evidence

Save actual terminal captures as `1.png` and `2.png` beside this file.

### Screenshot 1: Crash status and diagnostic logs

![CrashLoop diagnosis](1.png)

### Screenshot 2: Corrected Pod running

![CrashLoop recovery](2.png)

**Deliverable:** Both screenshots and a brief root-cause/fix note. Use a non-secret placeholder; do not include real credentials.