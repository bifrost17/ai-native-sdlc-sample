---
name: claims-api-security
description: Apply the org's API security standard beyond the four secure-api-review items — upstream call budget (claims-core 50 rps), enumeration prevention, per-role session keys, no secrets in the diff. Use whenever adding, changing, reviewing or writing the spec for a route or handler of the claims status service (customer portal, adjuster, agent paths), when a change calls claims-core or adds caching, and when touching config, environment or credentials.
---
<!-- 예시 — 팀 스킬이 아니다. 플러그인은 org-skills/skills/ 만 로드한다. 이 파일은 청구 상태 서비스를 한 프로젝트로 보고
     PROJECT-POLICY.md(같은 폴더)의 슬롯을 채웠을 때 스킬이 어떤 모습이 되는지 보여 준다. org-skills/examples/README.md -->
# Claims API security — S5 to S8

`policies/api-security.md` v0 is the source of truth; the four playbook items (S1–S4) live in the
`secure-api-review` skill and are not repeated here. Apply this skill together with it. Each item
below quotes its policy clause verbatim (Korean) and then says what to do.

## S5 Upstream call budget
> **S5** 상류 호출 예산: 청구 상태 상류(claims-core)는 50 rps 한도 — 새 경로는 캐시 정책과 호출 수 계산을 spec 에 적는다.

When a new route (or a changed one) calls claims-core:
- Write into `spec.md` a **cache policy** for the route (what is cached, key, TTL, invalidation) and a
  **call-count calculation** (calls to claims-core per request × expected request rate = rps), and
  show that the total stays under the 50 rps budget shared by every route.
- A route that cannot state its call count does not get a spec that says "done".
- Do not add retries or fan-out (one request → many upstream calls) without putting the multiplied
  count in the same calculation.

## S6 Enumeration prevention
> **S6** 열거 방지: 존재하지 않는 청구 번호와 권한 없는 청구 번호는 같은 응답(not_found)과 같은 지연.

For any handler that takes a claim number:
- A claim that does not exist and a claim the caller is not allowed to see return the **same status,
  the same body (`not_found`) and the same latency**. No `forbidden`, no "belongs to another
  customer", no different error shape.
- Do the authorization check and the existence check on the same path so the timing does not
  differ (for example, always look the claim up scoped to the caller's own identity, and treat
  "no row" as the single outcome). Do not return early on one branch and do extra work on the other.
- Do not leak existence through side channels: list endpoints, count endpoints, HEAD responses,
  audit-event wording visible to the caller, or different log lines that surface in error messages.

## S7 Session contract
> **S7** 세션 계약: 역할(customer · adjuster · agent)마다 세션 키 이름이 다르고, 한 핸들러는 자기 역할의 키만 읽는다.

- Every handler belongs to exactly one role — customer, adjuster or agent — and reads **only that
  role's session key**. It does not fall back to another role's key, and it does not accept "any of
  the three".
- Do not introduce a shared key, a merged "user" key, or a helper that resolves "whoever is logged
  in" across roles. A route that must serve two roles is two handlers (or two routes), each reading
  its own key.
- The portal validates the gateway JWT and hands the application the session (the `secure-api-review`
  org note); this skill is about which key a handler reads, not about re-validating the JWT.

## S8 Secrets
> **S8** 비밀값: 코드·설정·diff 에 자격증명 금지(훅 no-secrets 가 뒤를 받친다).

- No credential — API key, token, password, private key, connection string with a password — in
  source, in config files, in test fixtures, in docs or in the diff. Read them from the environment
  or the secret store at runtime and reference the variable name only.
- Placeholders in examples must not match a real secret shape (the `no-secrets` hook blocks writes
  that do; if it fires, change the value, do not bypass the hook).
- If a change needs a new secret, the spec names the variable and where it is provisioned; the
  value never appears in the repo.

## In your summary
List S5, S6, S7 and S8 one by one with what you checked and what you found, next to the four
`secure-api-review` items. If a clause cannot be satisfied or is ambiguous for this change, say so
under "areas of concern" instead of choosing an interpretation — the policy owner decides.
