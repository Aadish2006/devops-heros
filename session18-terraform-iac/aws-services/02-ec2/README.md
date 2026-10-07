# AWS EC2 (Elastic Compute Cloud) - Scalable Cloud Compute

## Overview
Amazon Elastic Compute Cloud (Amazon EC2) provides scalable computing capacity in the AWS Cloud. It eliminates the need to invest in hardware up front, enabling rapid deployment, scaling, and management of virtual servers.

---

## 1. What is EC2?
Amazon EC2 is an Infrastructure-as-a-Service (IaaS) offering that allows users to launch virtual servers called **instances** on demand. EC2 provides complete control over compute configurations, operating systems, networking, and storage.

```
                         AWS Cloud / VPC
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │                  ┌──────────────────────┐                    │
  │                  │   Security Group     │                    │
  │                  │  (Virtual Firewall)  │                    │
  │                  │  - Port 22 (SSH)     │                    │
  │                  │  - Port 80 (HTTP)    │                    │
  │                  │  - Port 443 (HTTPS)  │                    │
  │                  └──────────┬───────────┘                    │
  │                             │                                │
  │                  ┌──────────▼───────────┐                    │
  │                  │     EC2 Instance     │                    │
  │                  │ ┌──────────────────┐ │                    │
  │                  │ │  AMI (OS/Kernel) │ │                    │
  │                  │ ├──────────────────┤ │                    │
  │                  │ │ Instance Type    │ │                    │
  │                  │ │ (vCPU / RAM)     │ │                    │
  │                  │ ├──────────────────┤ │                    │
  │                  │ │ Key Pair (SSH)   │ │                    │
  │                  │ └──────────────────┘ │                    │
  │                  └──────────┬───────────┘                    │
  │                             │                                │
  │             ┌───────────────┴───────────────┐                │
  │             ▼                               ▼                │
  │     ┌───────────────┐               ┌───────────────┐        │
  │     │   Root EBS    │               │ Additional EBS│        │
  │     │    Volume     │               │    Volume     │        │
  │     │  (Persistent) │               │  (Data Disk)  │        │
  │     └───────────────┘               └───────────────┘        │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

---

## 2. Core Concepts

### 2.1 Amazon Machine Image (AMI)
An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.
- **AWS Provided AMIs:** Official Amazon Linux 2023, Ubuntu Server, Red Hat, Windows Server.
- **Custom AMIs:** Pre-baked machine images with proprietary configurations and application runtimes.
- **AWS Marketplace:** Third-party vendor appliances (e.g., Cisco, Fortinet, WordPress).

### 2.2 Instance Types
Instance types comprise varying combinations of CPU, memory, storage, and networking capacity:
- **General Purpose (`t3`, `t4g`, `m6i`):** Balanced compute, memory, and networking. Ideal for web servers, dev environments.
- **Compute Optimized (`c6i`, `c7g`):** High-performance processors. Ideal for batch processing, gaming servers, high-performance web servers.
- **Memory Optimized (`r6i`, `x2gd`):** Fast performance for workloads that process large datasets in memory (Redis, in-memory caches, distributed analytics).
- **Accelerated Computing (`p4`, `g5`):** Hardware GPU accelerators for machine learning and graphic rendering.
- **Storage Optimized (`i3en`, `d3`):** High sequential read/write access to large datasets on local storage (NoSQL, data warehouses).

### 2.3 Key Pairs
A key pair, consisting of a **public key** and a **private key** (.pem file), is a set of security credentials used to authenticate when connecting to an EC2 instance:
- AWS stores the public key inside `~/.ssh/authorized_keys` on the Linux instance.
- The user retains the private key locally and connects via:
  ```bash
  ssh -i my-key.pem ubuntu@<ec2-public-ip>
  ```
- *Modern alternative:* AWS Systems Manager (SSM) Session Manager allows secure browser-based terminal access without managing SSH keys or opening port 22.

### 2.4 Security Groups
A Security Group acts as a **stateful virtual firewall** for your EC2 instances that controls inbound and outbound traffic.
- **Stateful:** If an inbound request is permitted, response traffic is automatically allowed regardless of outbound rules.
- Supports **Allow** rules only (cannot create explicit Deny rules).
- Filter by IP address (CIDR blocks) or by referencing other Security Groups.

### 2.5 Elastic Block Store (EBS)
EBS provides persistent block storage volumes for use with EC2 instances.
- **Lifecycle independent:** Data on an EBS volume persists independently of the life of the EC2 instance (unlike ephemeral Instance Store).
- **Volume Types:**
  - `gp3` / `gp2`: General Purpose SSD (recommended default).
  - `io2`: Provisioned IOPS SSD for latency-critical databases.
  - `st1`: Throughput Optimized HDD for big data/streaming.
- Supports automatic point-in-time **snapshots** saved to Amazon S3.

---

## 3. Public vs. Private IP Addresses

| Feature | Public IPv4 Address | Private IPv4 Address | Elastic IP (EIP) |
| :--- | :--- | :--- | :--- |
| **Routability** | Internet-routable | Internal VPC only (RFC 1918) | Internet-routable |
| **Persistence** | Released when instance stops | Retained across stops/starts | Static; retained until released |
| **Cost** | Included / AWS standard | Free | Free when attached to a running instance |
| **Typical Use** | Bastion hosts, public web servers | Internal microservices, backend databases | Fixed outbound NAT / public endpoints |

---

## 4. EC2 Instance Lifecycle

```
[ Launch ] ──► [ Pending ] ──► [ Running ] ◄──► [ Rebooting ]
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
                [ Stopping ]                [ Shutting-down ]
                     │                           │
                     ▼                           ▼
                [ Stopped ]                 [ Terminated ]
                     │
                     ▼
                [ Starting ] ──► [ Running ]
```

- **Pending:** AWS prepares the host hardware and boots the AMI.
- **Running:** The instance is fully active and accessible.
- **Stopping / Stopped:** EBS-backed instances can be stopped. CPU/memory are released (no compute charges; EBS storage charges continue).
- **Terminated:** Instance is permanently deleted; root EBS volume deleted by default.

---

## 5. Common Use Cases
1. **Web and Application Hosting:** Running containers, Node.js, Spring Boot, or Django web apps behind an Application Load Balancer (ALB).
2. **Batch Processing & Workers:** Processing SQS queue jobs dynamically with Auto Scaling Groups (ASG).
3. **Legacy Enterprise Workloads:** Migrating on-premise Windows / Linux enterprise systems directly to AWS.
