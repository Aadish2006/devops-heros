# AWS IAM (Identity and Access Management) - Governance & Access Control

## Overview
AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. IAM provides the central control plane for authentication (who can sign in) and authorization (what permissions they have) across your entire AWS infrastructure.

---

## 1. What is IAM?
IAM is a **free, globally available service** (no region selection needed) that enables:
- **Centralized access management:** Control credentials, access keys, and API permissions from a single pane.
- **Granular permissions:** Grant exact access to specific resources under specific conditions (IP ranges, MFA, tags, time).
- **Identity federation:** Connect corporate directories (Active Directory, Okta, Google Workspace) to AWS without creating individual IAM users.

```
                    ┌────────────────────────────┐
                    │      AWS Cloud Account     │
                    └──────────────┬─────────────┘
                                   │
                    ┌──────────────▼─────────────┐
                    │   AWS IAM Policy Engine    │
                    │   Authentication (AuthN)   │
                    │   Authorization  (AuthZ)   │
                    └──────────────┬─────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
 ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
 │  IAM Users  │            │ IAM Groups  │            │  IAM Roles  │
 │ (Long-term) │            │  (Clusters) │            │(Short-term) │
 └──────┬──────┘            └──────┬──────┘            └──────┬──────┘
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                        ┌──────────▼──────────┐
                        │    JSON Policies    │
                        │ (Effect/Action/Res) │
                        └──────────┬──────────┘
                                   ▼
                        AWS Resources (EC2, S3, RDS, DynamoDB)
```

---

## 2. Core IAM Entities

### 2.1 Users
An IAM User represents a human person or an external application service that requires interaction with AWS.
- **Credentials:** Console password (for AWS Management Console) and Access Key ID + Secret Access Key (for AWS CLI / SDK).
- Best practice: Never use the AWS root account for daily activities; create dedicated IAM users with Multi-Factor Authentication (MFA).

### 2.2 Groups
An IAM Group is a collection of IAM users.
- Groups allow permissions to be applied collectively (e.g., `Developers`, `Admins`, `Auditors`).
- A user can belong to multiple groups.
- *Note:* Groups cannot be identified as a `Principal` in resource policies and cannot be nested.

### 2.3 Roles
An IAM Role is an identity with permission policies that determine what the identity can and cannot do in AWS, but is **not associated with a specific person**.
- Uses **temporary security credentials** provided via AWS STS (Security Token Service).
- **AssumeRole:** Intended to be assumed by anyone who needs it — EC2 instances, Lambda functions, cross-account administrators, or federated users.
- Eliminates hardcoded AWS credentials inside code or server configurations.

### 2.4 Policies
An IAM Policy is an object in AWS that, when associated with an identity or resource, defines their permissions. Policies are written in JSON.

#### Policy Structure
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadWriteDevOps",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::yatri-aadish",
        "arn:aws:s3:::yatri-aadish/*"
      ],
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

#### Types of Policies
1. **Identity-based Policies:** Attached to Users, Groups, or Roles (Managed or Inline).
2. **Resource-based Policies:** Attached directly to resources (e.g., S3 Bucket Policies, KMS Key Policies).
3. **Permissions Boundaries:** Set maximum allowed permissions for an IAM entity.
4. **Service Control Policies (SCPs):** Organizational guardrails in AWS Organizations.

---

## 3. Permissions Evaluation Logic

AWS evaluates policies using the following strict logic:
1. **Default Deny:** All requests are denied by default.
2. **Explicit Deny:** Any explicit `"Effect": "Deny"` immediately overrides all permissions.
3. **Explicit Allow:** If no explicit deny exists, an explicit `"Effect": "Allow"` grants access.

---

## 4. Principle of Least Privilege
The **Principle of Least Privilege (PoLP)** dictates that users, workloads, and programs should be granted only the absolute minimum permissions required to perform their intended tasks, and nothing more.

- Avoid `Action: "*"` and `Resource: "*"`.
- Scope resource ARNs down to individual buckets, tables, or instance IDs.
- Use AWS IAM Access Analyzer to review unused permissions and refine policies based on actual CloudTrail access history.

---

## 5. IAM Best Practices
| Practice | Description |
| :--- | :--- |
| **Lock Root Account** | Delete root access keys, set strong complex passwords, enable hardware/virtual MFA. |
| **Enforce MFA** | Require Multi-Factor Authentication on all interactive IAM users. |
| **Use Roles for Compute** | Assign IAM Roles (Instance Profiles) to EC2 instances and Lambda functions instead of saving keys in environment variables. |
| **Rotate Keys Regularly** | Audit and rotate programmatic access keys every 90 days. |
| **Use Groups for Permissions** | Attach policies to Groups, not individual users, to maintain organized access lifecycle. |
| **Implement IAM Access Analyzer** | Continuously detect resource shares with external AWS accounts. |

---

## 6. Common Use Cases
1. **EC2 Application Role:** Granting an EC2 instance permissions to read and write images to an S3 bucket without embedding credentials in code.
2. **Cross-Account Access:** Allowing engineers in a centralized identity account to assume an administrator or auditor role in development and production member accounts.
3. **CI/CD Deployment Pipelines:** Using OpenID Connect (OIDC) between GitHub Actions and AWS IAM to assume temporary deployment roles without long-lived secrets.
