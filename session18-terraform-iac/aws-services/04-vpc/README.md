# AWS VPC (Virtual Private Cloud) - Cloud Networking

## Overview
Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network that you've defined. It gives you complete control over your virtual networking environment, including selection of your own IP address range, subnets, route tables, and network gateways.

---

## 1. What is VPC?
A VPC is an isolated, private virtual network dedicated to your AWS account within a single AWS Region. It spans all Availability Zones (AZs) in that region.

```
                         AWS VPC (CIDR: 10.0.0.0/16)
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │                  ┌────────────────────────┐                     │
  │                  │ Internet Gateway (IGW) │                     │
  │                  └───────────┬────────────┘                     │
  │                              │                                  │
  │                              ▼                                  │
  │                     [Public Route Table]                        │
  │                      0.0.0.0/0 -> IGW                           │
  │                              │                                  │
  │   ┌──────────────────────────┴──────────────────────────────┐   │
  │   │  Public Subnet (10.0.1.0/24)                            │   │
  │   │  ┌────────────────────┐      ┌────────────────────────┐ │   │
  │   │  │  NAT Gateway       │      │  Bastion / ALB         │ │   │
  │   │  │  (Allocated EIP)   │      │  (Public IP Attached)  │ │   │
  │   │  └─────────┬──────────┘      └────────────────────────┘ │   │
  │   └────────────┼────────────────────────────────────────────┘   │
  │                │                                                │
  │                ▼                                                │
  │     [Private Route Table]                                       │
  │      0.0.0.0/0 -> NAT Gateway                                   │
  │                │                                                │
  │   ┌────────────┴────────────────────────────────────────────┐   │
  │   │  Private Subnet (10.0.2.0/24)                           │   │
  │   │  ┌────────────────────┐      ┌────────────────────────┐ │   │
  │   │  │  EC2 App Server    │      │  RDS Database Instance │ │   │
  │   │  │  (Private IP Only) │      │  (No Internet Access)  │ │   │
  │   │  └────────────────────┘      └────────────────────────┘ │   │
  │   └─────────────────────────────────────────────────────────┘   │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 2. Core VPC Networking Components

### 2.1 CIDR (Classless Inter-Domain Routing)
When creating a VPC, you assign an IPv4 CIDR block (e.g., `10.0.0.0/16`).
- Block size ranges from `/16` (65,536 IP addresses) to `/28` (16 IP addresses).
- Adheres to private RFC 1918 address spaces (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).

### 2.2 Subnets
A subnet is a range of IP addresses in your VPC located in a **single Availability Zone**.
- **Reserved IPs:** AWS reserves **5 IP addresses** in every subnet (Network address, VPC router, DNS server, future use, Network broadcast).
  - A `/24` subnet has 256 theoretical IPs, but only **251 usable IPs**.

### 2.3 Route Tables
A route table contains a set of rules (called routes) that determine where network traffic from your subnet or gateway is directed.
- Every VPC has a default **Main Route Table**.
- Custom route tables can be associated explicitly with specific subnets.

### 2.4 Internet Gateway (IGW)
An Internet Gateway is a horizontally scaled, redundant, highly available VPC component that enables communication between resources in your VPC and the internet.
- Does not impose bandwidth constraints or single points of failure.
- Performs Network Address Translation (NAT) for instances with public IPv4 addresses.

### 2.5 NAT Gateway (Network Address Translation)
A managed NAT service that allows instances in a **private subnet** to connect to services outside your VPC (e.g., software patches, external APIs), but **prevents external internet hosts from initiating inbound connections**.
- Deployed inside a **public subnet** with an Elastic IP (EIP) address.
- Private subnet route table routes `0.0.0.0/0 -> nat-xxxxxxxx`.

---

## 3. Public Subnet vs. Private Subnet

| Characteristic | Public Subnet | Private Subnet |
| :--- | :--- | :--- |
| **Route Table Target** | Route `0.0.0.0/0` directs to `Internet Gateway (IGW)` | Route `0.0.0.0/0` directs to `NAT Gateway` (or no default route) |
| **Auto-assign Public IP** | Enabled | Disabled |
| **Inbound Internet** | Directly reachable (subject to SG/NACL) | Never directly reachable from outside |
| **Typical Workloads** | Load Balancers (ALB/NLB), Bastion hosts | Microservices, Backend APIs, RDS databases, ElastiCache |

---

## 4. Security Groups vs. Network ACLs (NACLs)

| Feature | Security Group (SG) | Network ACL (NACL) |
| :--- | :--- | :--- |
| **Level** | Instance level (attached to ENI) | Subnet level |
| **State** | **Stateful** (return traffic automatically allowed) | **Stateless** (inbound and outbound evaluated separately) |
| **Rules** | **Allow rules only** | **Allow and Deny rules** |
| **Evaluation Order** | All rules evaluated collectively | Processed in strict numerical order (lowest first) |
| **Ephemeral Ports** | Handled automatically | Must explicitly open outbound ports (1024-65535) |

---

## 5. Common Use Cases
1. **Multi-Tier Web Architecture:** Public web tier behind ALB, private application tier on EC2 Auto Scaling, isolated database tier on RDS Multi-AZ.
2. **Hybrid Cloud Connectivity:** Linking corporate on-premise data centers to AWS VPC via AWS Site-to-Site VPN or AWS Direct Connect.
3. **VPC Peering & Transit Gateway:** Connecting hundreds of VPCs across multiple accounts and regions in a hub-and-spoke topology.
