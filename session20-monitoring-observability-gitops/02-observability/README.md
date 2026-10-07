# Task 2: Observability — The Three Pillars & Kubernetes Observability

## Overview
While **monitoring** alerts you that something is broken, **observability** is the degree to which you can infer the internal states of a system based on knowledge of its external outputs. It answers the critical question: **"Why is the system failing, and where is the root cause bottleneck?"**

---

## 1. The Three Pillars of Observability

```
                       ┌─────────────────────────┐
                       │     OBSERVABILITY       │
                       │ Understanding Unknowns  │
                       └────────────┬────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│   METRICS    │            │     LOGS     │            │    TRACES    │
│  "Is there a │            │  "What error │            │ "Where is the│
│   problem?"  │            │   occurred?" │            │  bottleneck?"│
└──────────────┘            └──────────────┘            └──────────────┘
Aggregation & Trends         Detailed Context           Request Flow Path
```

### 1.1 Metrics (Quantitative Aggregation)
- Numeric, time-stamped aggregated data.
- **Strength:** Lightweight to store, cheap to query, ideal for real-time alerting and historical trend graphs.
- **Limitation:** Lacks granular context (cannot explain why an individual user encountered a 500 error).
- **Core Standard:** OpenTelemetry (OTel), Prometheus metrics format.

### 1.2 Logs (Event Records & Context)
- Timestamped, structured (JSON) or unstructured text lines outputted by application code.
- **Strength:** Deepest contextual insight into application crashes, runtime exceptions, stack traces, and transactional flows.
- **Limitation:** High storage volume and indexing overhead; expensive to aggregate across high-scale distributed systems.
- **Common Tools:** FluentBit, Promtail + Grafana Loki, Elasticsearch/Logstash/Kibana (ELK).

### 1.3 Traces (Distributed Request Flow)
- Tracks the journey of an HTTP/gRPC request as it traverses across multiple microservices.
- **Span:** A single unit of work (e.g., executing a SQL query or calling an external auth API) containing execution duration, metadata, and status.
- **Trace:** A directed acyclic graph (DAG) of spans linked by a common `TraceId`.
- **Strength:** Directly pinpoints network latency bottlenecks and downstream cascading timeouts across microservice architectures.
- **Common Tools:** Jaeger, Zipkin, AWS X-Ray, Grafana Tempo.

---

## 2. Why Observability is Required in Modern Cloud Systems

| Traditional Monolith | Cloud-Native Microservices | Observability Need |
| :--- | :--- | :--- |
| Single server & log file | Hundreds of ephemeral containers | Correlate logs, traces, and metrics across dynamic pods |
| In-memory function calls | Network calls (REST/gRPC/Kafka) | Trace distributed network hops and packet delays |
| Predictable failure modes | Complex cascading partial failures | Debug "unknown unknowns" that static alerts miss |

---

## 3. Common Observability Tool Ecosystem

| Capability | Open-Source Leader | Cloud-Native Standard | Enterprise / SaaS |
| :--- | :--- | :--- | :--- |
| **Metrics** | Prometheus, VictoriaMetrics | OpenTelemetry Collector | Datadog, Dynatrace |
| **Logs** | Grafana Loki, FluentBit | OpenTelemetry Logs | Splunk, New Relic |
| **Traces** | Jaeger, Grafana Tempo | OpenTelemetry Tracing | AWS X-Ray, Honeycomb |
| **Unified Visualization** | Grafana | Grafana Cloud | Datadog Single Pane |

---

## 4. Kubernetes Observability Architecture

Observing Kubernetes requires insight into four distinct layers:

```
  ┌─────────────────────────────────────────────────────────┐
  │  Layer 4: Application Code (Custom Metrics, OTel Traces)│
  ├─────────────────────────────────────────────────────────┤
  │  Layer 3: Kubernetes Objects (Pods, Deployments, HPAs)  │
  │           Scraped via kube-state-metrics                │
  ├─────────────────────────────────────────────────────────┤
  │  Layer 2: Container Runtime (cAdvisor: CPU/Memory/Net)  │
  ├─────────────────────────────────────────────────────────┤
  │  Layer 1: Node Infrastructure (node-exporter: OS/Disk)  │
  └─────────────────────────────────────────────────────────┘
```

1. **Host & Node Health:** `node-exporter` daemonset collects disk space, CPU saturation, network drops, and OS kernel metrics.
2. **Container Level:** `cAdvisor` (built into the Kubelet) exposes per-container CPU throttling, memory limits, and OOM kills.
3. **Cluster State:** `kube-state-metrics` translates Kubernetes API objects (Pod readiness, replica drift, pending jobs) into Prometheus metrics.
4. **Log Collection:** `FluentBit` or `DaemonSet Promtail` mounts `/var/log/pods` to ship container stdout/stderr to Loki or Elasticsearch.
