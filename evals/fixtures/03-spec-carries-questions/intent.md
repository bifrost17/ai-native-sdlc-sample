# Intent: applicants are not told when their claim status changes
Author: 김민수 (청구운영팀). Status: draft.
## Problem
61 of 214 support calls in August were status inquiries; reading the screen to the caller takes 3 min 20 s. A move to 「보류」 sends nothing.
## Proposed outcome
An applicant is notified within 10 minutes of a status change and status inquiries fall below 20% of calls.
## Affected users and systems
Applicants; support agents; the claims status store; the notification gateway.
## Constraints
- C1 No new personal data is collected.
- C2 The upstream claims system is not called above 50 requests per second.
## Open questions
- Q1 Which status changes besides 「보류」 are notified — 청구운영팀장.
- Q2 Whether night-time (22–08) sending is deferred — 고객경험팀.
