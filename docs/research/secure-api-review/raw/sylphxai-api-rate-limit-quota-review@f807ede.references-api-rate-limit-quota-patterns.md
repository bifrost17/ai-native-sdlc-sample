# API Rate Limit Quota Patterns

## API limit state machine

```text
request_received -> principal_identified -> entitlement_checked -> budget_checked -> allowed -> usage_recorded -> response_returned
       |                    |                    |                 |             |              |
       v                    v                    v                 v             v              v
 unauthenticated       principal_unknown     plan_blocked      throttled   quota_exceeded   abuse_review
```

## Rule IDs

- `api-quota-1` — Identify the limiting principal: API key, user, tenant, app, integration, IP, workspace, model, endpoint, or billing account.
- `api-quota-2` — Separate rate limit, monthly quota, concurrency cap, payload cap, spend cap, and entitlement gate.
- `api-quota-3` — Costly endpoints need cost-weighted units rather than request counts only.
- `api-quota-4` — Public API errors need stable status, machine-readable code, reset time, request ID, and documentation link.
- `api-quota-5` — Return headers should expose limit, remaining, reset, retry-after, and policy name where safe.
- `api-quota-6` — Developer dashboards must show usage, projected exhaustion, recent 429s, and upgrade/override options.
- `api-quota-7` — Enterprise overrides need expiry, owner, support note, and abuse monitoring.
- `api-quota-8` — Usage-priced quotas must reconcile with metering, invoices, credits, refunds, and spend controls.
- `api-quota-9` — Limit changes need versioned docs, changelog, migration window, and affected-customer outreach.
- `api-quota-10` — Abuse controls should degrade fairly before broad outages: targeted throttles, challenge, suspension, or manual review.

## Decision table

| Scenario | Limit type | Unit | Developer UX | Operator control |
| --- | --- | --- | --- | --- |
| Free API tier | Rate plus monthly quota | Requests or cost units | Headers, dashboard, upgrade CTA | Tier config and abuse flag |
| AI inference endpoint | Cost-weighted quota plus spend cap | Tokens, images, seconds, dollars | Projected spend and retry guidance | Emergency cap and model route override |
| Webhook ingestion | Burst plus concurrency | Events and in-flight jobs | Backoff docs and replay window | Queue depth guardrail |
| Enterprise integration | Contract quota plus override | Tenant-level usage units | Named limit and support contact | Expiring override with audit |
| Suspected scraping | Adaptive throttle | Principal/IP/device cluster | Generic throttling copy | Abuse review and suspension |

## API contract checklist

- Limit principal and unit are unambiguous.
- 429/403/402 boundaries are documented.
- Headers and error body are stable across SDKs.
- Dashboard, alerts, and support playbook exist.
- Billing/entitlement/metering reconciliation is defined.
- Limit changes have migration notice and changelog entry.

## Event schema

Track: `api_request_allowed`, `api_request_throttled`, `api_quota_exceeded`, `api_limit_override_created`, `api_limit_override_expired`, `api_usage_alert_sent`, `api_abuse_review_opened`, `api_limit_policy_changed`.

Recommended properties: `principal_type`, `principal_id_hash`, `tenant_id_present`, `endpoint`, `method`, `policy_name`, `limit_unit`, `limit_value`, `remaining_bucket`, `reset_at`, `retry_after_seconds`, `plan`, `cost_units`, `request_id`, `outcome_code`.
