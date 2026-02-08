# Production Security Checklist

Pre-production security audit checklist for the Korean Apartment Transaction Analysis Platform.

## Table of Contents

- [Pre-Production Audit](#pre-production-audit)
- [OWASP Top 10 Verification](#owasp-top-10-verification)
- [Infrastructure Security](#infrastructure-security)
- [Application Security](#application-security)
- [Data Security](#data-security)
- [Compliance Requirements](#compliance-requirements)
- [Penetration Testing](#penetration-testing)
- [Security Sign-Off](#security-sign-off)

---

## Pre-Production Audit

### 1. Secrets Management

- [ ] **No hardcoded secrets**
  ```bash
  # Scan for potential secrets
  git grep -E 'api[_-]?key|secret|password|token' --ignore-case
  git secrets --scan-history
  ```

- [ ] **Environment variables properly configured**
  - [ ] `.env` files in `.gitignore`
  - [ ] Production secrets in Railway/Vercel dashboard
  - [ ] No secrets in version control history
  - [ ] Separate secrets for dev/staging/production
  - [ ] Secret rotation schedule documented

- [ ] **API keys rotated**
  ```bash
  # Generate new secret key
  ./scripts/generate-secret-key.sh

  # Update in Railway
  railway variables set SECRET_KEY=<new-key>

  # Update in Vercel
  vercel env add SECRET_KEY production
  ```

- [ ] **Service keys documented**
  ```bash
  # Document all service keys in secure location
  # - DATABASE_URL
  # - REDIS_URL
  # - SERVICE_KEY (Ministry of Land API)
  # - GEMINI_API_KEY
  # - SENTRY_DSN
  # - SECRET_KEY
  ```

### 2. Authentication & Authorization

- [ ] **JWT security**
  - [ ] Secret key minimum 32 characters
  - [ ] Token expiration configured (24 hours)
  - [ ] Refresh token rotation implemented
  - [ ] Token revocation mechanism in place
  - [ ] Secure token storage (httpOnly cookies)

- [ ] **Password security**
  - [ ] Passwords hashed with bcrypt (cost factor 12+)
  - [ ] Password minimum requirements (8+ chars, mixed case, numbers)
  - [ ] Password reset flow secure (time-limited tokens)
  - [ ] Account lockout after failed attempts
  - [ ] Password history enforced (no reuse of last 5)

- [ ] **Session management**
  - [ ] Session timeout configured (30 minutes idle)
  - [ ] Secure session storage (Redis)
  - [ ] Session invalidation on logout
  - [ ] Concurrent session limits
  - [ ] Session hijacking prevention

### 3. API Security

- [ ] **Rate limiting**
  ```bash
  # Verify rate limiting enabled
  curl -I https://api.your-domain.com/api/v1/analysis/basic-stats
  # Check for: X-RateLimit-Limit, X-RateLimit-Remaining
  ```

  - [ ] Global rate limit: 100 requests/minute
  - [ ] Per-endpoint limits configured
  - [ ] Rate limit by IP and user
  - [ ] Rate limit errors logged

- [ ] **CORS configuration**
  ```python
  # Verify in fastapi-backend/middleware/cors.py
  ALLOWED_ORIGINS = [
      "https://your-domain.com",
      "https://www.your-domain.com",
      # NO wildcards in production!
  ]
  ```

- [ ] **Input validation**
  - [ ] All inputs validated with Pydantic
  - [ ] SQL injection prevention (parameterized queries)
  - [ ] XSS prevention (output escaping)
  - [ ] Path traversal prevention
  - [ ] File upload validation (if applicable)

- [ ] **Authentication on protected endpoints**
  ```bash
  # Test authentication requirement
  curl https://api.your-domain.com/api/v1/premium/investment-recommendation
  # Should return 401 Unauthorized without token
  ```

### 4. Network Security

- [ ] **HTTPS/TLS**
  ```bash
  # Check SSL certificate
  echo | openssl s_client -connect your-domain.com:443 -servername your-domain.com 2>/dev/null | \
    openssl x509 -noout -dates -subject -issuer

  # Verify HTTPS redirect
  curl -I http://your-domain.com
  # Should return 301/308 redirect to HTTPS
  ```

  - [ ] Valid SSL certificate (Let's Encrypt or commercial)
  - [ ] Certificate expiry > 30 days
  - [ ] TLS 1.2+ only (no TLS 1.0/1.1)
  - [ ] Strong cipher suites
  - [ ] HTTP redirects to HTTPS
  - [ ] HSTS header enabled (max-age=31536000)

- [ ] **Security headers**
  ```bash
  # Check security headers
  curl -I https://your-domain.com | grep -E 'X-|Content-Security|Strict-Transport'
  ```

  Required headers:
  - [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - [ ] `X-Frame-Options: DENY`
  - [ ] `X-Content-Type-Options: nosniff`
  - [ ] `X-XSS-Protection: 1; mode=block`
  - [ ] `Referrer-Policy: strict-origin-when-cross-origin`
  - [ ] `Content-Security-Policy: default-src 'self'`
  - [ ] `Permissions-Policy: geolocation=(), microphone=(), camera=()`

### 5. Database Security

- [ ] **Connection security**
  ```bash
  # Verify SSL connection
  railway run psql $DATABASE_URL -c "SELECT * FROM pg_stat_ssl;"
  ```

  - [ ] Database not publicly accessible
  - [ ] Connections over SSL (sslmode=require)
  - [ ] Connection pooling configured
  - [ ] Max connections limit set
  - [ ] Idle connection timeout configured

- [ ] **Access control**
  ```sql
  -- Verify database permissions
  SELECT grantee, privilege_type
  FROM information_schema.role_table_grants
  WHERE table_schema = 'public';
  ```

  - [ ] Principle of least privilege applied
  - [ ] Separate users for different services
  - [ ] Read-only user for analytics
  - [ ] No superuser access from application

- [ ] **Data encryption**
  - [ ] Sensitive data encrypted at rest
  - [ ] Database backups encrypted
  - [ ] Transparent data encryption (if available)
  - [ ] Column-level encryption for PII

- [ ] **SQL injection prevention**
  ```bash
  # Audit for string concatenation in queries
  grep -r "f\"SELECT" fastapi-backend/
  grep -r '+ "SELECT' fastapi-backend/
  # Should return no results
  ```

  - [ ] All queries use parameterized statements
  - [ ] No dynamic SQL with user input
  - [ ] ORM used correctly (SQLAlchemy)

### 6. Redis Security

- [ ] **Redis hardening**
  ```bash
  # Check Redis security
  redis-cli -h <host> -a <password> INFO server | grep "redis_version"
  redis-cli CONFIG GET requirepass
  ```

  - [ ] Password authentication enabled
  - [ ] Not publicly accessible
  - [ ] Rename dangerous commands (FLUSHDB, FLUSHALL)
  - [ ] Persistence enabled (RDB + AOF)
  - [ ] No sensitive data in cache

### 7. Container Security

- [ ] **Docker best practices**
  ```bash
  # Scan Docker image
  trivy image apt-insights-backend:latest

  # Check Dockerfile
  cat fastapi-backend/Dockerfile
  ```

  - [ ] Using official base images
  - [ ] Multi-stage builds
  - [ ] Non-root user in containers
  - [ ] No secrets in Dockerfile
  - [ ] `.dockerignore` configured
  - [ ] Image scanning for vulnerabilities
  - [ ] Minimal image size

- [ ] **Image security**
  ```bash
  # Verify user
  docker inspect apt-insights-backend:latest | jq '.[0].Config.User'
  # Should return: "appuser" or "1000"
  ```

---

## OWASP Top 10 Verification

### A01:2021 - Broken Access Control

- [ ] Authentication required on protected endpoints
- [ ] Authorization checks on all operations
- [ ] No insecure direct object references
- [ ] User cannot access other users' data
- [ ] Admin functions properly protected

**Test**:
```bash
# Try accessing protected endpoint without auth
curl https://api.your-domain.com/api/v1/premium/investment-recommendation
# Expected: 401 Unauthorized

# Try accessing other user's data
curl -H "Authorization: Bearer <user1-token>" \
  https://api.your-domain.com/api/v1/users/<user2-id>/profile
# Expected: 403 Forbidden
```

### A02:2021 - Cryptographic Failures

- [ ] Sensitive data encrypted in transit (HTTPS)
- [ ] Sensitive data encrypted at rest
- [ ] Strong encryption algorithms (AES-256)
- [ ] Proper key management
- [ ] No weak or deprecated algorithms

**Test**:
```bash
# Check TLS version
nmap --script ssl-enum-ciphers -p 443 your-domain.com

# Verify database encryption
railway run psql $DATABASE_URL -c "SHOW ssl;"
```

### A03:2021 - Injection

- [ ] Parameterized queries used
- [ ] Input validation on all endpoints
- [ ] Output encoding
- [ ] Command injection prevention
- [ ] LDAP/NoSQL injection prevention

**Test**:
```bash
# Test SQL injection
curl "https://api.your-domain.com/api/v1/analysis/basic-stats?region_code=11680' OR '1'='1"
# Should be safely escaped

# Check code for vulnerabilities
bandit -r fastapi-backend/ -ll
```

### A04:2021 - Insecure Design

- [ ] Threat modeling completed
- [ ] Security requirements documented
- [ ] Secure design patterns used
- [ ] Defense in depth implemented
- [ ] Principle of least privilege applied

### A05:2021 - Security Misconfiguration

- [ ] Default passwords changed
- [ ] Unnecessary features disabled
- [ ] Error messages don't leak information
- [ ] Security patches up to date
- [ ] Admin interfaces secured

**Test**:
```bash
# Check for default credentials
# (None should exist)

# Verify error handling
curl https://api.your-domain.com/api/v1/invalid
# Should return generic error, not stack trace

# Check debug mode
railway logs | grep "DEBUG"
# Should not be enabled in production
```

### A06:2021 - Vulnerable and Outdated Components

- [ ] All dependencies up to date
- [ ] Security advisories monitored
- [ ] Automated dependency scanning
- [ ] No known vulnerabilities

**Test**:
```bash
# Python dependencies
safety check -r fastapi-backend/requirements.txt

# Node.js dependencies
cd nextjs-frontend && npm audit

# Docker base image
trivy image python:3.11-slim
```

### A07:2021 - Identification and Authentication Failures

- [ ] Multi-factor authentication available
- [ ] Secure password reset
- [ ] Session management secure
- [ ] Credential stuffing prevention
- [ ] Brute force protection

**Test**:
```bash
# Test rate limiting on login
for i in {1..20}; do
  curl -X POST https://api.your-domain.com/api/auth/login \
    -d '{"email":"test@test.com","password":"wrong"}'
done
# Should be rate limited after 10 attempts
```

### A08:2021 - Software and Data Integrity Failures

- [ ] Code signing implemented
- [ ] Dependency verification
- [ ] CI/CD pipeline secured
- [ ] Automated deployment process
- [ ] Rollback capability

**Test**:
```bash
# Verify CI/CD security
gh api repos/:owner/:repo/actions/secrets

# Check for unsigned commits (optional)
git log --show-signature
```

### A09:2021 - Security Logging and Monitoring Failures

- [ ] All authentication logged
- [ ] All authorization failures logged
- [ ] Input validation failures logged
- [ ] Log tampering prevention
- [ ] Log analysis automated

**Test**:
```bash
# Verify logging
railway logs | grep -E 'login|auth|error'

# Check Sentry integration
curl https://api.your-domain.com/api/v1/test-error
# Should appear in Sentry dashboard
```

### A10:2021 - Server-Side Request Forgery (SSRF)

- [ ] User-controlled URLs validated
- [ ] Internal network access restricted
- [ ] Response filtering implemented
- [ ] URL allowlist used

**Test**:
```bash
# Test SSRF (if URL input exists)
curl -X POST https://api.your-domain.com/api/v1/fetch \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}'
# Should be blocked
```

---

## Infrastructure Security

### Cloud Platform Security

#### Railway

- [ ] Two-factor authentication enabled
- [ ] Team access properly configured
- [ ] Service tokens secured
- [ ] Audit logs reviewed
- [ ] Resource limits configured

#### Vercel

- [ ] Two-factor authentication enabled
- [ ] Team permissions configured
- [ ] Preview deployments secured
- [ ] Environment variables encrypted
- [ ] Custom domains verified

### DNS Security

- [ ] DNSSEC enabled (if supported)
- [ ] CAA records configured
- [ ] SPF record configured (if sending email)
- [ ] DMARC policy configured
- [ ] DNS provider has 2FA

### Firewall Rules

- [ ] Only required ports open
- [ ] Database port not public
- [ ] Redis port not public
- [ ] SSH key-based authentication only
- [ ] IP allowlist configured (if applicable)

---

## Application Security

### Code Security

- [ ] **Security linting**
  ```bash
  # Python
  bandit -r fastapi-backend/ -ll -f json -o bandit-report.json

  # JavaScript/TypeScript
  cd nextjs-frontend && npm audit
  ```

- [ ] **Dependency scanning**
  ```bash
  # Safety check
  safety check -r requirements.txt --json > safety-report.json

  # npm audit
  cd nextjs-frontend && npm audit --json > npm-audit.json
  ```

- [ ] **Code review**
  - [ ] All code reviewed by another developer
  - [ ] Security-focused code review completed
  - [ ] No eval() or exec() usage
  - [ ] No shell command injection
  - [ ] No path traversal vulnerabilities

### Error Handling

- [ ] **Proper error responses**
  ```python
  # Good: Generic error message to user
  return {"error": "Invalid request"}

  # Bad: Leaking sensitive information
  return {"error": f"SQL error: {str(e)}"}
  ```

- [ ] Generic error messages to users
- [ ] Detailed errors in logs only
- [ ] No stack traces exposed
- [ ] No database errors exposed
- [ ] Error codes documented

### Logging Security

- [ ] **Secure logging**
  ```python
  # Good: No sensitive data
  logger.info("User login", user_id=user.id)

  # Bad: Logging sensitive data
  logger.info("User login", password=password)
  ```

- [ ] No passwords in logs
- [ ] No API keys in logs
- [ ] No PII in logs (or masked)
- [ ] Structured logging (JSON)
- [ ] Log retention policy defined

---

## Data Security

### Data Classification

| Classification | Examples | Protection |
|---------------|----------|------------|
| **Public** | Property prices, locations | None required |
| **Internal** | Usage statistics, logs | Access control |
| **Confidential** | User emails, preferences | Encryption + access control |
| **Restricted** | Passwords, payment info | Strong encryption + strict access |

### Data Protection

- [ ] **Encryption at rest**
  - [ ] Database encryption enabled
  - [ ] Backup encryption enabled
  - [ ] File storage encryption enabled

- [ ] **Encryption in transit**
  - [ ] HTTPS for all connections
  - [ ] Database SSL connections
  - [ ] Redis TLS connections (if available)

- [ ] **Data masking**
  ```python
  # Mask sensitive data in logs
  def mask_email(email):
      parts = email.split('@')
      return f"{parts[0][:2]}***@{parts[1]}"
  ```

- [ ] **Data retention**
  - [ ] Retention policy documented
  - [ ] Automated data deletion
  - [ ] User data export available
  - [ ] Right to be forgotten implemented

### Personal Data (GDPR/Privacy)

- [ ] Privacy policy published
- [ ] User consent obtained
- [ ] Data minimization applied
- [ ] Purpose limitation enforced
- [ ] Data subject rights implemented
  - [ ] Right to access
  - [ ] Right to rectification
  - [ ] Right to erasure
  - [ ] Right to data portability

---

## Compliance Requirements

### OWASP ASVS

Application Security Verification Standard Level 1 (minimum):
- [ ] Authentication verification
- [ ] Session management verification
- [ ] Access control verification
- [ ] Input validation verification
- [ ] Cryptography verification

### CWE Top 25

Review: https://cwe.mitre.org/top25/

Key vulnerabilities to check:
- [ ] CWE-79: Cross-site Scripting (XSS)
- [ ] CWE-89: SQL Injection
- [ ] CWE-20: Improper Input Validation
- [ ] CWE-78: OS Command Injection
- [ ] CWE-22: Path Traversal
- [ ] CWE-352: CSRF
- [ ] CWE-434: Unrestricted File Upload
- [ ] CWE-94: Code Injection

### Industry Standards

- [ ] **PCI DSS** (if handling payments)
- [ ] **GDPR** (if serving EU users)
- [ ] **CCPA** (if serving California users)
- [ ] **SOC 2** (if enterprise customers)

---

## Penetration Testing

### Automated Scanning

```bash
# OWASP ZAP API scan
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.your-domain.com/openapi.json \
  -f openapi \
  -r zap-report.html

# Nikto web server scan
nikto -h https://your-domain.com -output nikto-report.html

# SQLMap (SQL injection testing)
sqlmap -u "https://api.your-domain.com/api/v1/analysis/basic-stats?region_code=11680" \
  --batch --random-agent

# Nuclei vulnerability scanner
nuclei -u https://your-domain.com -t cves/ -o nuclei-report.txt
```

### Manual Testing Checklist

#### Authentication Testing

- [ ] Bypass authentication with SQL injection
- [ ] Bypass authentication with NoSQL injection
- [ ] Session fixation
- [ ] Session hijacking
- [ ] Privilege escalation
- [ ] Weak password policy
- [ ] Brute force protection

#### Authorization Testing

- [ ] Horizontal privilege escalation
- [ ] Vertical privilege escalation
- [ ] Insecure direct object references
- [ ] Missing function level access control
- [ ] Forced browsing

#### Input Validation Testing

- [ ] SQL injection (all input fields)
- [ ] XSS (reflected, stored, DOM-based)
- [ ] XXE (XML External Entity)
- [ ] Command injection
- [ ] LDAP injection
- [ ] Template injection
- [ ] Path traversal

#### Business Logic Testing

- [ ] Bypass rate limiting
- [ ] Bypass payment flows
- [ ] Concurrent session issues
- [ ] Race conditions
- [ ] Time-based attacks

### Penetration Testing Report

After testing, generate report:
```markdown
# Penetration Testing Report

**Date**: YYYY-MM-DD
**Tester**: _______
**Scope**: Production application

## Executive Summary
- Total vulnerabilities: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Vulnerabilities Found
1. **[CRITICAL] SQL Injection in...**
   - Description
   - Impact
   - Remediation

## Recommendations
1. ...
2. ...

## Conclusion
Overall security posture: Good/Fair/Poor
```

---

## Security Sign-Off

### Pre-Production Security Audit

Date: _______________

#### Secrets Management
- [x] No hardcoded secrets
- [x] Environment variables secured
- [x] API keys rotated

Auditor: _______________ Date: _______________

#### Authentication & Authorization
- [x] JWT security verified
- [x] Password security verified
- [x] Session management verified

Auditor: _______________ Date: _______________

#### API Security
- [x] Rate limiting configured
- [x] CORS properly restricted
- [x] Input validation implemented

Auditor: _______________ Date: _______________

#### Network Security
- [x] HTTPS enforced
- [x] Security headers configured
- [x] TLS configuration verified

Auditor: _______________ Date: _______________

#### Database Security
- [x] Connection security verified
- [x] Access control configured
- [x] Data encryption enabled

Auditor: _______________ Date: _______________

#### OWASP Top 10
- [x] A01: Broken Access Control - PASSED
- [x] A02: Cryptographic Failures - PASSED
- [x] A03: Injection - PASSED
- [x] A04: Insecure Design - PASSED
- [x] A05: Security Misconfiguration - PASSED
- [x] A06: Vulnerable Components - PASSED
- [x] A07: Authentication Failures - PASSED
- [x] A08: Software Integrity - PASSED
- [x] A09: Logging Failures - PASSED
- [x] A10: SSRF - PASSED

Auditor: _______________ Date: _______________

#### Penetration Testing
- [x] Automated scans completed
- [x] Manual testing completed
- [x] All critical issues resolved
- [x] High-priority issues resolved

Auditor: _______________ Date: _______________

### Final Security Approval

**Security Lead**: _______________ Date: _______________

**CTO/CISO**: _______________ Date: _______________

**Approved for Production Deployment**: YES / NO

**Conditions (if any)**:
- _______________________
- _______________________

---

## Appendix

### Security Tools

```bash
# Install security tools
pip install safety bandit

# Trivy (container scanning)
brew install aquasecurity/trivy/trivy

# git-secrets
brew install git-secrets
git secrets --register-aws --global

# OWASP ZAP
docker pull owasp/zap2docker-stable
```

### Security Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- Security Headers: https://securityheaders.com/

### Incident Response Contacts

See RUNBOOK.md for incident response procedures and contacts.

---

**Last Updated**: 2026-02-08
**Document Version**: 1.0.0
**Next Audit**: 2026-05-08
