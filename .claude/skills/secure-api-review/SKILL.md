---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
 modifying an external-facing endpoint, reviewing API code, or
 generating an OpenAPI spec.
---
# Secure API review
When you create or change an API endpoint:
1. Authentication: every endpoint requires the gateway JWT;
 no anonymous routes outside /health.
2. Input validation: validate request bodies against the OpenAPI
 schema and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
 actor, action, entity and timestamp.
4. Data classification: fields tagged pii in the schema must never
 appear in logs or error messages.
Run scripts/check-endpoints.sh and include its output in your summary.

<!-- L6 481-499 verbatim: the playbook's only example of a policy skill. L6 503: "A skill is a
control, though an advisory one." This repo has no deterministic backstop behind it. -->
