# Troubleshooting Scenario Gauntlet

## Objective

Triage five intentionally broken Pods by collecting evidence before changing their manifests, then fix and verify each root cause.

## Tasks

1. From this folder, run `./triage_all.sh` and inspect the resulting Pods with `kubectl get pods -l tier=triage-gauntlet -o wide`.
2. For each Pod, use `kubectl describe` and the relevant logs or DNS check to record the symptom, evidence, root cause, and proposed fix. Do not edit a manifest before recording the initial evidence.
3. Complete the focused exercise in each scenario folder: [CrashLoop](scenario-1-crashloop/Homework.md), [Image Pull](scenario-2-imagepull/Homework.md), [Pending](scenario-3-pending/Homework.md), [DNS Failure](scenario-4-dns-failure/Homework.md), and [OOMKilled](scenario-5-oomkilled/Homework.md).
4. Apply each corrected manifest and verify the workload reaches the expected state. A DNS test is successful when the corrected hostname resolves; an HTTP authorization response can still demonstrate successful name resolution and connectivity.
5. Remove the gauntlet Pods after collecting evidence with `kubectl delete pods -l tier=triage-gauntlet`.

## Screenshot Evidence

Capture actual terminal output from the initial triage and the completed fixes. Save the screenshots in this folder.

### Screenshot 1: Initial status of all five scenarios

![Initial scenario statuses](1.png)

### Screenshot 2: Evidence and recovery of the five scenarios

![Scenario investigation and verification](2.png)

**Deliverable:** The two screenshots and a five-row incident table containing symptom, evidence, root cause, fix, and verification for each scenario.