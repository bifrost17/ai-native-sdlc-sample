# Intent: agents re-read the whole call history at every repeat call
Author: 박지영 (고객경험팀). Status: accepted.
## Problem
At a repeat call the agent reads the previous transcripts from the start; 1 min 50 s per call goes to reading.
## Proposed outcome
The last three call summaries appear at the top of the agent screen and reading time drops below 40 s per call.
## Affected users and systems
Support agents; the call-history store; the agent screen.
## Constraints
- C1 The raw transcript is never shown on screen.
## Open questions
- Q1 Who approves a summary before it is shown — 고객경험팀장.
