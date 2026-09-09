## 무엇
`intent/0002-claims-status/intent.md` 한 장 — 청구 상태 셀프서비스(플레이북 L2 213~225 의 예시 소재).

## 진입 경로
사람 · 아이디어. 원저자는 클레임 운영팀(비엔지니어)이고, 본문은 원저자의 말(한국어)이다 — L2 198 "No formal language is required". 절 이름·`Status:` 토큰은 `capture-intent` 스킬 템플릿의 고정 토큰 그대로.

## 이 PR 의 머지 = PO 승인
L2 231: 승인·반려는 "recorded as the merge or the closing review". `Status: draft` 는 파일 안에서 바뀌지 않는다 — 머지가 곧 accepted 다.

## 원저자 정정
확인 못 함 — 원저자와의 실제 브레인스토밍 세션은 없었다(소재는 플레이북 예시 + 옛 브랜치 `feat/0002-claims-status` 의 서술). 스킬이 요구하는 「초안을 원저자에게 보여 주고 정정받는」 단계는 이 PR 의 리뷰 코멘트가 그 자리다.

## 검증
- `‹…›` 잔존 0 (`grep -c '‹' intent/0002-claims-status/intent.md` = 0) · 27줄.
- `make check` 기준선 rc=0 (origin/main 72ca0d9, raw `00-baseline-make-check.txt`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NzhLB6C1oHJHu7uAVDe54w
