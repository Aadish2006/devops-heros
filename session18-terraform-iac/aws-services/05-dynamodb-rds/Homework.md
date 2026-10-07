# AWS DynamoDB & RDS - Database Services

## Overview
AWS offers a comprehensive suite of purpose-built database engines. This guide contrasts **Amazon DynamoDB** (fully managed serverless NoSQL key-value & document store) and **Amazon RDS** (managed relational database service).

---

## 1. Amazon DynamoDB (NoSQL Service)

### 1.1 What is DynamoDB?
Amazon DynamoDB is a fully managed, serverless, key-value and document NoSQL database designed to deliver single-digit millisecond latency at any scale.
- **Serverless:** No servers to provision, patch, or manage.
- **High Availability:** Automatically replicates data across three Availability Zones (AZs) in an AWS Region.
- **Capacity Modes:**
  - **On-Demand:** Pay per request; ideal for unpredictable spikes.
  - **Provisioned:** Specify read/write capacity units (RCU/WCU) with auto-scaling.

```
                          Amazon DynamoDB Architecture
  ┌────────────────────────────────────────────────────────────────────────┐
  │                                                                        │
  │   Table: "Users"                                                       │
  │   ┌────────────────────────────────────────────────────────────────┐   │
  │   │  Primary Key: Partition Key (PK) + Sort Key (SK)               │   │
  │   └───────────────────────────────┬────────────────────────────────┘   │
  │                                   │                                    │
  │     ┌─────────────────────────────┼─────────────────────────────┐      │
  │     ▼                             ▼                             ▼      │
  │  [Item 1]                      [Item 2]                      [Item 3]  │
  │  - PK: "user#101"              - PK: "user#101"              - PK: "2" │
  │  - SK: "profile"               - SK: "order#2026-001"        - SK: "p" │
  │  - name: "Aadish"              - total: 149.99               - name: … │
  │  - role: "Admin"               - status: "SHIPPED"           (Dynamic) │
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Data Modeling Concepts
- **Tables:** Collection of items (analogous to a relational table).
- **Items:** A single record consisting of multiple attributes (analogous to a row). Max item size: 400 KB.
- **Attributes:** Individual data elements (analogous to a column/field). Schema is schemaless except for primary keys.
- **Partition Key (HASH):** Internal hash function determines the physical storage partition. Must be uniformly distributed to avoid hot partitions.
- **Sort Key (RANGE):** Enables 1-to-many relationships and range queries (`begins_with`, `between`, `<`, `>`) within the same partition key.
- **Secondary Indexes:**
  - **Global Secondary Index (GSI):** Index with a different partition key and sort key across the entire table.
  - **Local Secondary Index (LSI):** Alternate sort key for the same partition key.

### 1.3 DynamoDB Use Cases
1. **Gaming Leaderboards & Player Sessions:** Microsecond read/write state storage at extreme concurrency.
2. **E-commerce Shopping Carts:** Fast session retrieval keyed by `user_id`.
3. **IoT Sensor Ingestion:** Streaming telemetry data keyed by `device_id` and timestamp.
4. **Terraform State Locking:** Using a simple DynamoDB table with `LockID` string key.

---

## 2. Amazon RDS (Relational Database Service)

### 2.1 What is RDS?
Amazon Relational Database Service (Amazon RDS) is a managed service that simplifies the setup, operation, and scaling of relational databases in the cloud. It automates administrative tasks such as hardware provisioning, database setup, patching, and backups.

```
                     Amazon RDS Multi-AZ Architecture
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  VPC (Private DB Subnet Group across 2 AZs)                      │
  │                                                                  │
  │  Availability Zone A (Primary)    Availability Zone B (Standby)  │
  │  ┌─────────────────────────┐      ┌─────────────────────────┐    │
  │  │   Primary DB Instance   │      │   Standby DB Instance   │    │
  │  │   (Active Read/Write)   │      │   (Passive Synchronous) │    │
  │  │                         ├─────►│                         │    │
  │  └───────────┬─────────────┘ Sync └─────────────────────────┘    │
  │              │ Replication                                       │
  │              ▼ Async Replication                                 │
  │  ┌─────────────────────────┐                                     │
  │  │   Read Replica (AZ C)   │                                     │
  │  │   (Read-Only Scaling)   │                                     │
  │  └─────────────────────────┘                                     │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

### 2.2 Supported Database Engines
1. **Amazon Aurora:** High-performance cloud-native MySQL/PostgreSQL-compatible engine (up to 5x throughput of standard MySQL).
2. **PostgreSQL**
3. **MySQL**
4. **MariaDB**
5. **Oracle Database**
6. **Microsoft SQL Server**

### 2.3 RDS Security Architecture
- Deployed exclusively in **Private VPC Subnet Groups** across at least two AZs.
- DB Security Group only permits inbound database port traffic (e.g., 5432 for Postgres, 3306 for MySQL) from designated application security groups.
- Encryption at rest using **AWS KMS** (AES-256) and TLS/SSL connections in transit.
- Native AWS IAM database authentication (login without passwords using IAM tokens).

### 2.4 Backups & Restore
- **Automated Backups:** Daily full snapshots + transaction logs stored in S3 with retention between 1 to 35 days. Enables point-in-time recovery (PITR) down to the second.
- **Manual DB Snapshots:** User-initiated snapshots retained until explicitly deleted.

### 2.5 Multi-AZ vs. Read Replicas
| Dimension | Multi-AZ Deployment | Read Replicas |
| :--- | :--- | :--- |
| **Purpose** | **High Availability & Disaster Recovery** | **Read Performance Scalability** |
| **Replication** | **Synchronous** | **Asynchronous** |
| **Active/Standby** | Standby is passive (cannot be queried) | Active (serves read-only queries) |
| **Failover** | Automatic DNS failover (typically 60-120s) | Manual promotion to primary |
| **Cross-Region** | Single region (multi-AZ) | Can span across regions for DR |

### 2.6 RDS Use Cases
1. **Transactional Banking / Financial Systems:** ACID-compliant relational schemas requiring foreign keys and complex joins.
2. **Enterprise ERP & CRM Applications:** Standard enterprise database backends (Oracle, SQL Server, Postgres).
3. **Web Applications (Content Management):** WordPress, Drupal, Magento requiring MySQL or MariaDB.

---

## 3. Comparison Matrix: DynamoDB vs. RDS

| Criterion | Amazon DynamoDB | Amazon RDS |
| :--- | :--- | :--- |
| **Database Type** | NoSQL (Key-Value / Document) | Relational (SQL) |
| **Schema** | Flexible / Dynamic Schema | Rigid Structured Schema |
| **Scaling** | Horizontal (Automatic partitioning) | Vertical (Compute) + Horizontal (Read Replicas) |
| **Complex Joins** | Not supported (Client-side / Single-table design) | Native SQL joins and aggregations |
| **Latency** | Consistent single-digit millisecond | Single to double-digit millisecond depending on query |
| **Maintenance** | Fully serverless (Zero admin) | Automated patching, minor version upgrades |
