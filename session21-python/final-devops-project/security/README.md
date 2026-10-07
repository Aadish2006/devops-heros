# Security Policy & Scan Configurations

## 1. SAST (Static Application Security Testing)
- **Tool:** Bandit / CodeQL
- **Configuration:** Scans backend python code (`app/`) for SQL injection, insecure imports, hardcoded tokens, and weak cryptographic primitives.
- **Rule:** Zero High / Medium severity issues allowed.

## 2. SCA (Software Composition Analysis)
- **Tool:** pip-audit & npm audit
- **Configuration:** Scans `requirements.txt` and `package.json` against known CVE vulnerability databases.
- **Rule:** High and Critical CVEs block build execution.

## 3. Secret Scanning
- **Tool:** Gitleaks
- **Configuration:** Detects committed AWS access keys, private certificates, DB passwords, and GitHub personal access tokens.

## 4. Container Image Scanning
- **Tool:** Aqua Security Trivy
- **Configuration:**
  ```bash
  trivy image --severity HIGH,CRITICAL --exit-code 1 taskboard-backend:latest
  trivy image --severity HIGH,CRITICAL --exit-code 1 taskboard-frontend:latest
  ```
- **Rule:** Exit code 1 fails the pipeline if any unfixed High or Critical vulnerability is present.
