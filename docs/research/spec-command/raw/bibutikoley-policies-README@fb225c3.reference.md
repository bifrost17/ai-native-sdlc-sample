# Policy skill templates

These five skills are **templates**, not live plugin commands. `/sdlc:setup` copies them into a product repo's
`.claude/skills/` (only when that repo has no skills yet), where each policy owner replaces the `<...>`
placeholders with real policy text and adds the source-of-truth link, owner and last-reviewed date in the header.

Once in the product repo they load automatically whenever Claude does work they describe (writing `spec.md`,
planning an endpoint, producing UI copy, reviewing a PR), and `/sdlc:spec` records which ones it applied.

| Template | Owner | Backed by (deterministic) |
|---|---|---|
| `security-policy` | security lead | `secrets-guard`, `protected-paths` hooks; Security review pass |
| `compliance-policy` | compliance lead | `protected-paths` (migrations/infra tickets), `production-gate`; Compliance review pass |
| `brand-guidelines` | brand / design lead | review Nits (Important when customers could be misled) |
| `ux-standards` | head of design / accessibility | `/sdlc:verify --ui` screenshot loop; Compliance review pass |
| `secure-api-review` | API security owner | Security review pass; `scripts/check-endpoints.sh` if present |

A skill is an advisory control. Where a policy must hold without exception, ask the platform engineer for a hook.
