# Kubernetes Troubleshooting Mini-Project

## Objective

Use a repeatable troubleshooting process to verify a working Nginx Deployment and Service, diagnose an invalid image, and find a Service selector mismatch.

## Tasks

1. Apply `deployment.yaml` and `service.yaml`. Verify both replicas become Ready and the Service has endpoints.
2. From a temporary in-cluster client Pod, request `http://troubleshooting-service` and record the response.
3. Apply `broken-pod.yaml`. Before changing the manifest, use `kubectl get` and `kubectl describe` to identify the image-pull failure in Events.
4. Record the broken Pod's status, the exact useful event, the root cause, and a valid replacement image. Apply the correction and verify the Pod runs.
5. Change the Service selector from `app: troubleshooting-app` to `app: wrong-app`. Apply the change and verify its endpoints become empty.
6. Compare the Service selector with the Pod labels, restore the correct selector, and verify endpoints and HTTP access recover.
7. Summarize the incident using **symptom → evidence → root cause → fix → verification** for both failures.

## Screenshot Evidence

Capture actual terminal output from your cluster. Save each image in this folder.

### Screenshot 1: Healthy Deployment, Service endpoints, and application response

![Healthy application and Service](1.png)

### Screenshot 2: Broken Pod status and image-pull Events

![Broken Pod investigation](2.png)

### Screenshot 3: Empty endpoints, selector correction, and recovery

![Service selector fix and recovery](3.png)

**Deliverable:** The three screenshots and your incident summary. Do not include credentials or unrelated cluster output.