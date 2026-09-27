# Mutual TLS (mTLS) Demo

A small Python project demonstrating **mutual TLS authentication** between two services using a private certificate authority hierarchy.

## What it demonstrates

With standard TLS, the client authenticates the server. With mTLS, **both sides present and verify certificates**, enabling service-to-service identity without relying only on passwords or bearer tokens.

## Components

```text
Private Root CA
      |
      v
Intermediate CA
      |
      +--> Service A certificate
      |
      +--> Service B certificate

Service A <------ mutual TLS ------> Service B
```

## Services

- Service A listens on port `8443`
- Service B listens on port `8444`
- Both require a client certificate
- Both verify certificates against the configured CA chain

## Tech Stack

- Python
- Python `ssl` and `socket`
- OpenSSL-compatible X.509 certificates
- Public Key Infrastructure (PKI)

## Security

Private keys are intentionally excluded from source control. Generate new local keys before running the demo. Never reuse demonstration CA or service keys in production.

Keys that have ever been committed to a public repository must be considered compromised and should be rotated.

## Purpose

This repository is a focused demonstration of **service identity, certificate chains, TLS client authentication, and PKI-based Zero Trust concepts**.
