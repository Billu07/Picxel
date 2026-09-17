# Security Policy

## Reporting a vulnerability
Please **do not open a public issue.** Report privately through GitHub instead: on this repository, go to **Security → Report a vulnerability**.

Include what you found, how to reproduce it, and the impact you expect. We aim to:
- acknowledge your report within **3 business days**
- share an assessment and remediation plan within **10 business days**
- credit you in the release notes, unless you prefer to stay anonymous

## Scope
**In scope:** this repository and the hosted service at https://picxel.autolinium.com.

**Out of scope:** volumetric denial-of-service testing against the hosted service, social engineering, physical attacks, and vulnerabilities in third-party services we use (report those to the vendor).

Please test against a local instance (`docker compose up`) whenever possible, and never access data that isn't yours.

## Supported versions
Security fixes land on `main` and ship in the next release. Older releases don't receive patches.

## Our commitments
Uploaded images are processed in memory and never stored (`project.md` §12). If you find a way to make Picxel retain, log, or expose image data, treat it as a high-severity issue.
