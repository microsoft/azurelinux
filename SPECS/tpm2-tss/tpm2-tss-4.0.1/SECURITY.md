# Security Policy

## Supported Versions

Currently supported versions:

| Version  | Supported          |
| -------- | ------------------ |
| >= 2.4.0 | :white_check_mark: |
|  < 2.4.0 | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.

## Security Reporting Guidelines

### Reporting

Security vulnerabilities *should be emailed* to **all** members of the [MAINTAINERS](MAINTAINERS) file to coordinate the
disclosure of the vulnerability.

### Tracking

When a maintainer is notified of a security vulnerability, they *must* create a GitHub security advisory
per the instructions at:

  - <https://docs.github.com/en/code-security/repository-security-advisories/about-github-security-advisories-for-repositories>

Maintainers *should* use the optional feature through GitHub to request a CVE be issued, alternatively RedHat has provided CVE's
in the past and *may* be used, but preference is on GitHub as the issuing CNA.

### Publishing

Once ready, maintainers should publish the security vulnerability as outlined in:

  - <https://docs.github.com/en/code-security/repository-security-advisories/publishing-a-repository-security-advisory>

As well as ensuring the publishing of the CVE, maintainers *shal*l have new release versions ready to publish at the same time as
the CVE. Maintainers *should* should strive to adhere to a sub 60 say turn around from report to release.
