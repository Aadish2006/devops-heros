# Homework: Ingress, ConfigMaps, and Secrets

1. Move non-sensitive application settings into a ConfigMap and consume them from a workload.
2. Store a sample credential in a Secret and expose it to the workload without placing the value directly in its manifest.
3. Configure Ingress routing for the application and verify the expected host/path behavior in a cluster with an Ingress controller.
4. Explain why Kubernetes Secrets require additional access controls and are not, by themselves, a complete encryption strategy.

**Deliverable:** Manifests with sample-only credentials, access test results, and a brief security note.

## Lesson Homework

Each link opens the Markdown homework file in the corresponding topic folder.

- [ConfigMap](01-configmap/HOMEWORK.md)
- [Secret](02-secret/HOMEWORK.md)
- [Ingress](03-ingress/HOMEWORK.md)
- [Full Demo](04-full-demo/HOMEWORK.md)