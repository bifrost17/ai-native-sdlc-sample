# Intent: applicants are not told when their claim status changes
Author: 김민수 (청구운영팀). Status: draft.
## Problem
Last month 61 of 214 support calls were "what is the status of my claim". Reading the screen to the caller takes an agent 3 min 20 s on average. When a claim moves to 「보류」 nothing is sent, and the applicant learns of it days later by phoning in.
## Proposed outcome
An applicant is notified within 10 minutes of a status change, and status-inquiry calls fall.
## Affected users and systems
Applicants; support agents (청구운영팀); the claims system; the notification channel already in use.
## Constraints
- C1 No new contact data is collected — only what is already held (법무팀).
- C2 The claims system is not queried above 50 requests per second (법무팀).
## Open questions
- Q1 Which status changes besides 「보류」 are notified — the team lead decides.
- Q2 Whether to send at night (22:00–08:00) — 고객경험팀.
