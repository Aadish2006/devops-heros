# Scenario 2: Image Pull Failure

The Pod uses an invalid image name and tag.

1. Apply `broken.yaml`; inspect the Pod with `kubectl get pod fail-2-imagepull-pod`.
2. Run `kubectl describe pod fail-2-imagepull-pod` and record the relevant image-pull Event.
3. Replace the invalid image with an available public image such as `nginx:1.27`, apply the corrected manifest, and verify the Pod becomes Ready.

## Screenshot Evidence

Save actual terminal captures as `1.png` and `2.png` beside this file.

### Screenshot 1: Image pull failure and Event

![Image pull failure](1.png)

### Screenshot 2: Corrected image and running Pod

![Image pull recovery](2.png)

**Deliverable:** Both screenshots and a short explanation of how the Event exposed the invalid image.