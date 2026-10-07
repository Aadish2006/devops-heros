# AWS S3 (Simple Storage Service) - Cloud Object Storage

## Overview
Amazon Simple Storage Service (Amazon S3) is an industry-leading object storage service offering high scalability, data availability, security, and performance. S3 is designed for **99.999999999% (11 9's)** of data durability.

---

## 1. What is S3?
Unlike block storage (EBS) or file storage (EFS), Amazon S3 stores data as **objects** within **buckets**.
- **Objects:** Files (images, videos, backups, logs, code) plus metadata and a unique Key identifier.
- **Buckets:** Top-level containers for objects.
- **Global Namespace:** Bucket names must be **globally unique across all AWS accounts worldwide** (e.g., `s3://yatri-aadish`).

```
                    Amazon S3 Global Storage Namespace
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   Bucket: s3://yatri-aadish (Region: ap-south-1)                │
  │   ┌─────────────────────────────────────────────────────────┐   │
  │   │  Bucket Policy (Access Control & Deny Unencrypted HTTP) │   │
  │   │  Default Encryption: SSE-S3 (AES-256) or SSE-KMS        │   │
  │   │  Versioning: Enabled                                    │   │
  │   └────────────────────────────┬────────────────────────────┘   │
  │                                │                                │
  │        ┌───────────────────────┼───────────────────────┐        │
  │        ▼                       ▼                       ▼        │
  │   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
  │   │ Object 1     │        │ Object 2     │        │ Object 3     │
  │   │ index.html   │        │ images/a.png │        │ logs/app.log │
  │   │ [v1.0, v1.1] │        │ [Standard]   │        │ [Glacier]    │
  │   └──────────────┘        └──────────────┘        └──────────────┘
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Concepts

### 2.1 Buckets & Objects
- **Bucket:** Logical namespace container located in a specific AWS Region.
- **Object Key:** Full path/filename identifier within a bucket (e.g., `assets/images/logo.png`).
- **Object Size:** 0 bytes to a maximum of 5 TB per individual object. Single PUT upload limit is 5 GB (use Multipart Upload for larger files).

### 2.2 S3 Storage Classes
| Storage Class | Availability | Min Storage Duration | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **S3 Standard** | 99.99% | None | Frequently accessed data, active websites, mobile apps |
| **S3 Intelligent-Tiering** | 99.9% | 30 days | Unknown or unpredictable access patterns (auto cost optimization) |
| **S3 Standard-IA** | 99.9% | 30 days | Infrequent access; rapid retrieval when needed |
| **S3 One Zone-IA** | 99.5% | 30 days | Non-critical, recreatable data stored in a single AZ |
| **S3 Glacier Flexible** | 99.99% | 90 days | Long-term archiving; minutes to hours retrieval time |
| **S3 Glacier Deep Archive** | 99.99% | 180 days | Compliance & regulatory archives; 12-48 hours retrieval |

### 2.3 Object Versioning
- Keeps multiple variants of an object in the same bucket.
- Protects against accidental overwrites and deletions (deleting creates a `Delete Marker`, allowing restoration).
- Once enabled on a bucket, versioning cannot be disabled—it can only be **suspended**.

### 2.4 S3 Lifecycle Policies
Lifecycle configurations define rules to automatically transition objects between storage classes or expire (delete) them after a set number of days.
- *Example rule:*
  1. Move objects from **S3 Standard** to **S3 Standard-IA** after 30 days.
  2. Transition to **S3 Glacier Flexible** after 90 days.
  3. Permanently delete non-current versions after 365 days.

### 2.5 Encryption at Rest & In Transit
- **In Transit:** Enforced via TLS/HTTPS (bucket policies can deny `aws:SecureTransport: false`).
- **At Rest:**
  - **SSE-S3 (Server-Side Encryption with Amazon S3-Managed Keys):** Default AES-256 encryption.
  - **SSE-KMS (AWS Key Management Service):** Gives audit trails in CloudTrail and customer control over key rotation.
  - **SSE-C (Customer-Provided Keys):** Encryption handled by AWS, but customer supplies and manages the key.
  - **Client-Side Encryption:** Data encrypted before uploading to S3.

### 2.6 S3 Bucket Policies
A JSON-based resource policy attached directly to the bucket to manage permissions.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceSSLRequestsOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::yatri-aadish",
        "arn:aws:s3:::yatri-aadish/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

---

## 3. Common Use Cases
1. **Static Website Hosting:** Hosting HTML/CSS/JS frontend applications combined with Amazon CloudFront CDN.
2. **Data Lakes & Big Data Analytics:** Centralized raw storage queried by AWS Athena, EMR, or Snowflake.
3. **Backup and Disaster Recovery:** Off-site storage for database dumps, VM images, and application logs.
4. **Terraform Remote State Backend:** Storing `terraform.tfstate` with state locking via DynamoDB.
