# Spec: claim status notifications (from intent 9003-eval-spec-carry)
Upstream: intent.md@0123456789abcdef0123456789abcdef01234567. Status: draft.
Skills applied: secure-api-review.
## Requirements
- R1 A status-change event produces a notification within 10 minutes.
- R2 A failed send is retried three times with exponential backoff.
## Design
The status store's change events go through the existing queue to the notification gateway.
## Constraints
- C1 No new personal data is collected.
- C2 The upstream claims system is not called above 50 requests per second.
- C3 (discovered) The notification gateway allows 600 sends per minute.
## Open questions from intent
- Q1 answered: 「보류」 and 「반려」 are the first-phase transitions — 청구운영팀장, 2026-09-10.
- Q2 carried forward: night-time deferral is not decided in this spec — 고객경험팀 (owner).
## Flagged concerns
- F1 If the notification text lets the claim reason be inferred, it conflicts with C1 — 개인정보보호 담당 decides.
## Out of scope
Additional channels (카카오, app push).
## Acceptance criteria
- AC1 → R1 a send record exists within 10 minutes of the status change.
- AC2 → R2 three retries are recorded after a failed send.
