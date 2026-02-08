# Security Review Checklist

Comprehensive security checklist for production deployment.

## Critical Security Items

### 1. Secrets Management

- [ ] **No hardcoded secrets in code**
  ```bash
  # Scan for potential secrets
  git grep -E 'api[_-]?key|secret|password|token' --ignore-case
  ```

- [ ] **Environment variables properly configured**
  - [ ] `.env` files in `.gitignore`
  - [ ] Production secrets in Railway/Vercel dashboard
  - [ ] No secrets in version control history
  - [ ] Separate secrets for dev/staging/production

- [ ] **API keys rotated**
  - [ ] Database credentials changed from defaults
  - [ ] Redis password set
  - [ ] Secret key generated (32+ characters)
  - [ ] Service keys documented

### 2. Authentication & Authorization

- [ ] **API security**
  - [ ] Rate limiting enabled (100 requests/minute)
  - [ ] CORS configured with specific origins
  - [ ] Input validation on all endpoints
  - [ ] SQL injection prevention (parameterized queries)
  - [ ] XSS prevention (sanitized outputs)

- [ ] **Access control**
  - [ ] Principle of least privilege applied
  - [ ] Database users have minimal required permissions
  - [ ] Non-root containers (user: appuser)
  - [ ] File permissions restricted

### 3. Network Security

- [ ] **HTTPS/TLS**
  - [ ] SSL certificate installed
  - [ ] HTTP redirects to HTTPS
  - [ ] TLS 1.2+ only
  - [ ] Strong cipher suites
  - [ ] HSTS header enabled

- [ ] **Security headers**
  - [ ] X-Frame-Options: DENY
  - [ ] X-Content-Type-Options: nosniff
  - [ ] X-XSS-Protection: 1; mode=block
  - [ ] Referrer-Policy: strict-origin-when-cross-origin
  - [ ] Content-Security-Policy configured

### 4. Data Security

- [ ] **Database security**
  - [ ] Database not publicly accessible
  - [ ] Connections over SSL
  - [ ] Regular backups enabled
  - [ ] Backup encryption enabled
  - [ ] Sensitive data encrypted at rest

- [ ] **Redis security**
  - [ ] Password authentication enabled
  - [ ] Not publicly accessible
  - [ ] Persistence enabled
  - [ ] No sensitive data in cache

### 5. Container Security

- [ ] **Docker best practices**
  - [ ] Using official base images
  - [ ] Multi-stage builds for smaller images
  - [ ] Non-root user in containers
  - [ ] No secrets in Dockerfile
  - [ ] .dockerignore configured
  - [ ] Image scanning for vulnerabilities

### 6. Dependency Security

- [ ] **Python dependencies**
  ```bash
  # Check for vulnerabilities
  pip install safety
  safety check -r requirements.txt

  # Update dependencies
  pip list --outdated
  ```

- [ ] **Node.js dependencies**
  ```bash
  # Check for vulnerabilities
  npm audit

  # Fix vulnerabilities
  npm audit fix
  ```

- [ ] **Keep dependencies updated**
  - [ ] Regular dependency updates scheduled
  - [ ] Security advisories monitored
  - [ ] Automated dependency updates (Dependabot)

### 7. Logging & Monitoring

- [ ] **Secure logging**
  - [ ] No passwords in logs
  - [ ] No API keys in logs
  - [ ] No PII in logs
  - [ ] Structured logging (JSON)
  - [ ] Log retention policy defined

- [ ] **Error handling**
  - [ ] Generic error messages to users
  - [ ] Detailed errors in logs only
  - [ ] No stack traces exposed
  - [ ] No database errors exposed

### 8. Infrastructure Security

- [ ] **Railway/Vercel security**
  - [ ] Two-factor authentication enabled
  - [ ] Team access properly configured
  - [ ] Service tokens secured
  - [ ] Audit logs enabled

- [ ] **Firewall rules**
  - [ ] Only required ports open
  - [ ] Database port not public
  - [ ] Redis port not public
  - [ ] SSH key-based authentication only

### 9. Application Security

- [ ] **Input validation**
  ```python
  # Example: Pydantic validation
  from pydantic import BaseModel, validator

  class QueryParams(BaseModel):
      lawd_cd: str
      deal_ymd: str

      @validator('lawd_cd')
      def validate_lawd_cd(cls, v):
          if not v.isdigit() or len(v) != 5:
              raise ValueError('Invalid region code')
          return v
  ```

- [ ] **Output sanitization**
  - [ ] HTML escaped in responses
  - [ ] JSON properly encoded
  - [ ] No eval() or exec() usage

- [ ] **CSRF protection**
  - [ ] SameSite cookies
  - [ ] CSRF tokens for state-changing operations

### 10. Code Security

- [ ] **Secure coding practices**
  - [ ] No SQL string concatenation
  - [ ] No shell command injection
  - [ ] No path traversal vulnerabilities
  - [ ] No code injection

- [ ] **Security linting**
  ```bash
  # Python security linter
  pip install bandit
  bandit -r fastapi-backend/

  # JavaScript security linter
  npm install -g eslint-plugin-security
  eslint --plugin security nextjs-frontend/
  ```

---

## Security Testing

### 1. Automated Scans

```bash
# OWASP ZAP (API security testing)
docker run -t owasp/zap2docker-stable zap-api-scan.py \
    -t https://your-backend.railway.app/openapi.json \
    -f openapi

# Dependency vulnerability scanning
pip install safety
safety check

npm audit
```

### 2. Manual Testing

- [ ] Test for SQL injection
- [ ] Test for XSS vulnerabilities
- [ ] Test for CSRF vulnerabilities
- [ ] Test rate limiting
- [ ] Test authentication bypass
- [ ] Test authorization bypass

### 3. Penetration Testing (Optional)

Consider hiring a security professional for:
- Full application penetration test
- Infrastructure security audit
- Code review
- Social engineering assessment

---

## Security Incident Response Plan

### 1. Detection

- Monitor for:
  - Unusual traffic patterns
  - High error rates
  - Failed authentication attempts
  - Suspicious database queries
  - Unauthorized access attempts

### 2. Response Steps

1. **Identify** the incident
2. **Contain** the breach
3. **Eradicate** the threat
4. **Recover** services
5. **Post-mortem** analysis

### 3. Contact Information

- Security Lead: _______________
- Infrastructure Lead: _______________
- On-call Engineer: _______________
- Emergency Hotline: _______________

---

## Security Compliance

### OWASP Top 10 2021

- [ ] A01:2021 – Broken Access Control
- [ ] A02:2021 – Cryptographic Failures
- [ ] A03:2021 – Injection
- [ ] A04:2021 – Insecure Design
- [ ] A05:2021 – Security Misconfiguration
- [ ] A06:2021 – Vulnerable and Outdated Components
- [ ] A07:2021 – Identification and Authentication Failures
- [ ] A08:2021 – Software and Data Integrity Failures
- [ ] A09:2021 – Security Logging and Monitoring Failures
- [ ] A10:2021 – Server-Side Request Forgery (SSRF)

### CWE Top 25

Review: https://cwe.mitre.org/top25/

---

## Ongoing Security

### Monthly Tasks

- [ ] Review access logs
- [ ] Update dependencies
- [ ] Rotate credentials (quarterly)
- [ ] Review firewall rules
- [ ] Check for security advisories

### Quarterly Tasks

- [ ] Security audit
- [ ] Penetration testing
- [ ] Disaster recovery drill
- [ ] Security training for team
- [ ] Review and update security policies

---

## Security Tools

### Recommended Tools

1. **Safety** - Python dependency vulnerability scanner
2. **npm audit** - Node.js dependency vulnerability scanner
3. **Bandit** - Python security linter
4. **OWASP ZAP** - Web application security scanner
5. **Trivy** - Container image vulnerability scanner
6. **git-secrets** - Prevents committing secrets

### Installation

```bash
# Python tools
pip install safety bandit

# Container scanning
brew install aquasecurity/trivy/trivy

# Secrets detection
brew install git-secrets
git secrets --register-aws --global
```

---

## Security Sign-off

- [ ] All critical security items addressed
- [ ] Security testing completed
- [ ] Security documentation reviewed
- [ ] Incident response plan in place
- [ ] Team security training completed

**Security Reviewer**: _______________

**Date**: _______________

**Signature**: _______________

---

**Last Updated**: 2026-02-07
