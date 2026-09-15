---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
 modifying an external-facing endpoint, reviewing API code, or
 generating an OpenAPI spec.
---
<!-- TEAM: replace with the org's real API security standard — docs/ADOPTING.md · L12 -->
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
Include what you checked, item by item, in your summary.

Org note on item 1 (answered the same way twice — 0002 F3, 0008 F4): the portal validates the
gateway JWT and hands the application a session; code that reads only the session satisfies
item 1. Do not flag this again unless the session contract itself changes.

<!-- L6 481-498 verbatim except the last line: the playbook's example ends "Run
scripts/check-endpoints.sh and include its output in your summary." — this repo has no such script
and, by the product owner's decision, no code backstop. L6 503: "A skill is a control, though an
advisory one." -->
