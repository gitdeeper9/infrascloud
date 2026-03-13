# Security Policy for INFRAS-CLOUD

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of INFRAS-CLOUD seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

**gitdeeper@gmail.com**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Preferred Languages

We prefer all communications to be in English.

## Policy

We follow the principle of [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).

## Security Considerations for Deployment

When deploying INFRAS-CLOUD in production, please consider the following security measures:

### 1. Environment Variables
- Never commit `.env` files to version control
- Use strong passwords for database connections
- Rotate API keys regularly
- Use secrets management services in production

### 2. Network Security
- Run services behind a firewall
- Use HTTPS/TLS for all web interfaces
- Restrict database access to localhost when possible
- Use VPN for remote sensor connections

### 3. Authentication
- Change default passwords immediately
- Use strong password policies
- Enable 2FA for administrative access
- Implement rate limiting for API endpoints

### 4. Data Security
- Encrypt sensitive data at rest
- Use secure backup strategies
- Implement data retention policies
- Anonymize data when sharing publicly

### 5. Sensor Security
- Physically secure sensor installations
- Use encrypted communication channels
- Regularly update firmware
- Monitor for tampering

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Updates will be announced via:

- GitHub releases
- PyPI package updates
- Project website announcements
- Direct email to registered users (optional)

## Acknowledgments

We thank the security researchers and users who report vulnerabilities to us responsibly.
