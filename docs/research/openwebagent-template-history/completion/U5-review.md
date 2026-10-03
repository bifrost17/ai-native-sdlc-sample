# U5 적대적 리뷰 — PR·커밋 전달과 후속 갱신

2026-10-03 Asia/Seoul. 검토 대상은 제작 저장소 `HEAD c3c5a3a9f0aa7da507bdb220601fbf34bbef4490`의
미배포 0.1.9 후보다. 원 후보 직전 기준 `ad98adec5c85ebb969fa394796d388df10303a1f`부터
`HEAD`까지 해당 경로의 실제 diff를 읽었다. `ec476959ca20c2e44fd9d2cbfcbb5b0c7eeffc23`에
전달 정책·PR 양식·feedback이 이미 작성됐고, 그 뒤 U4 수정은 색인 호환과 계약 권한을 다뤘다.
이번 U5 검토 시점에 해당 source의 미커밋 수정은 없다. 저장소의 다른 미커밋·미추적 작업은 이
검토 대상이 아니며 건드리지 않았다.

## 판정

**U5 범위에서 필수 수정 지적 없음.** `CHANGE-DELIVERY.md`는 최종 diff와 검증 대상판,
문서 개정 이유, 남은 일과 사람의 수락을 구분한다. 작은 오탈자에는 짧은 PR·제목만 있는 커밋을
허용하고 merge/revert의 기존 형식을 인정한다. `sdlc-feedback`의 추가 문장은 최종 PR 본문,
선택한 색인, 과거 spec과 현재 계약의 대조를 기존 변경·인계 사건에 붙인다. 새 검사기나 승인
단계를 만들지 않았다. 아래 대조는 정책 문서의 일관성 검토다. 실제 제품 개발에서 이 문장이
자연 선택되거나 전달 오류를 줄이는지는 아직 관측하지 않았다.

## 기대와 실제 대조

사용자 결정과 `intent/0028`의 FR06–08, SP05·SP07, AC06–07은 간결한 PR/커밋 전달,
기존 실행 기록을 복제하지 않는 색인, 여섯 단위의 순차 검토를 요구한다. 북극성의 V3-14는
spec·prompt·skill의 실제 판과 정책 적용, V4-06/08은 계획의 파일·순서·증거와 새 담당자의
인계 이해, V4-11은 계획 이탈 시 같은 커밋의 갱신, V8-02는 작업 중 loop와 끝의 새 문맥
검토를 다룬다. 북극성은 이번 PR 제목·본문의 고정 양식을 정하지 않는다. 따라서 전달 형식은
템플릿 팀 정책으로 판단했다.

`tdd-optional/project/docs/CHANGE-DELIVERY.md` 9–21행과
`tdd-optional/project/.github/pull_request_template.md`의 네 부분은 목적·결과, 해당 개발건과
계획 범위, 실제 검증판·기대·관측·한계, 남은 작업을 서로 맞춘다. 리뷰 후 diff나 시험 대상판이
바뀌면 본문을 갱신하므로 이전 실행을 최신 통과로 표시할 근거가 없다. 본문에 원문 시험 출력을
복제하는 요구도 없다. 25–46행은 일반 커밋의 제목·필요한 본문, 큰 호환 변경, 작은 정리,
merge/revert의 예외와 staged 범위를 구분한다. 같은 커밋에 문서와 코드가 있다는 사실만으로
문서 선행 작성이나 시험 성공을 주장하지 않는 5행은 V4-11의 역사적 실패와 맞는다.

`tdd-optional/project/docs/GIT-WORKFLOW.md`의 시작·계획과 작업·PR 절은 이미 수락된 상류
결정과 현재 허용된 변경을 구분하고, 영향 spec/plan을 다음 의존 작업 전에 갱신하여 관련 구현
커밋에 담도록 한다. 실제 diff에서 계약을 어긴 코드 결함과 의도된 계약 개정을 구분한다.
`tdd-optional/project/docs/PROCESS.md`의 단계 인계와 검증 근거는 plan의 현재 요약·기존 실행
기록에 시험 뒤 남은 일을 연결한다. `changes/README.md`의 현재 개발건 표는 상태·대상판·PR·
다음 일을 찾는 색인이며 과거 spec을 최신 계약으로 자동 승계하지 않는다. 기존 `intent/` 제품은
채택 경로를 유지하고, 색인이 없으면 plan·기존 실행 기록을 쓴다는 U4 수정이 U5 본문과 충돌하지
않는다. `sdlc-feedback`의 마지막 추가 문장은 이 경로를 선택형으로 참조한다.

반례를 직접 대조했다. 리뷰 수정 후 PR 본문이 그대로인 경우는 최종 diff/검증판 재대조 문구가
막도록 안내한다. spec/plan 갱신을 최종 완료까지 미루거나 코드 결함을 계약 개정으로 합리화할
근거는 Git 정책·색인·feedback에 없다. 뒤늦은 시험과 리뷰가 남은 작업을 바꾸면 현재 plan·
인계를 갱신하되 시험 전문은 기존 근거에 둔다. 작은 오탈자에 세 문서를 요구하지 않으며, PR 생성·
검사 통과·에이전트 리뷰를 사람의 승인이나 전체 개발건 완료로 부르지 않는다. 권한은 기존
`PROJECT-POLICY.md`와 `REVIEW.md`의 담당자·머지 절차에 남아 있다. 형식이나 예시를 더 보태야
해결되는 중요 누락은 찾지 못했다.

## 확인과 한계

`git diff ad98adec..HEAD --`로 위 여섯 경로를 확인했고, `ec476959..HEAD`의 차이는 U4의
색인·계약 문구에만 있었다. 해당 여섯 경로의 `git diff --check`는 종료 코드 0이었다.
전달 정책·Git 절차·프로세스·changes 색인·feedback의 Markdown 상대 링크를 파일 위치에서
확인한 결과 끊긴 경로가 없었다(종료 코드 0). 이는 문서 링크와 diff 공백 확인이다. 패키지
전체 검사, Claude/Codex 전달본·strict 검증, 실제 PR 작성 및 제품 실행은 U6와 별도 제품
실험의 범위다. 사람의 수락·통합·배포는 이 리뷰로 성립하지 않는다.

검토 입력의 SHA-256은 다음과 같다. 경로는 모두 이 저장소 기준이며, 해시는 위 `HEAD`의
검토 시점 파일 바이트를 가리킨다. `CLAUDE.md`의 작업 중 수정은 현재 파일로 읽었으며
`HEAD`의 내용이었다고 소급하지 않는다.

| 입력 | SHA-256 |
|---|---|
| `CLAUDE.md` | `ca5a6758b93491b6407eb5a7d6da6bc6ccc1819897653e4cbe767d42a1c08f0b` |
| `.claude/agents/verifier.md` | `de01e577a0cdaacda538c0197adff6e11eaaec32561011f13717911ac3a1b395` |
| `tdd-optional/org-skills/agents/sdlc-verifier.md` | `6011efd7c8de0ad092db19751364d890dafbca6d390560aaeae3c1855e1e617a` |
| `intent/0028-openwebagent-history-feedback/intent.md` | `56c380d188c3eeff0b6c30951d831159fc32db27f781680caa13200235cd9106` |
| `intent/0028-openwebagent-history-feedback/spec.md` | `ff36f8b563e39326cc161fee680b7bbdeb728eb8659cf0943618229209ab0905` |
| `intent/0028-openwebagent-history-feedback/plan.md` | `16e20b67481a60eca32061c69bae8a34b4ca166db6267f8c4d684712ae46ac4a` |
| `docs/research/openwebagent-template-history/completion/README.md` | `cd63eb9cc43895a34dd1f2088d13f7e135d3d25878ea05fbaab1e0f9a73f76de` |
| `docs/verification/north-star-playbook.html` | `e11f73355e5b2ec329f6d485487341ebc6d15aa7a54c4d4a5a7ef4f17329ca50` |
| `tdd-optional/project/REVIEW.md` | `7587cae2849954087a28da9d5258373416e27075041d06d7c5ee1bca1180f2a2` |
| `tdd-optional/project/PROJECT-POLICY.md` | `97ef9153885472dae3e564f5914172e1a70c156db33f184f7ced97e1e0ef31ac` |
| `tdd-optional/project/docs/CHANGE-DELIVERY.md` | `274c1d8766e79c49b563172059baa356ae34ac199828d4aaafffe36dc01372a3` |
| `tdd-optional/project/.github/pull_request_template.md` | `01e54f5f921293e680f3773e669691b2f132e08f8d9bb9134a9eddf3dc19fe98` |
| `tdd-optional/project/docs/GIT-WORKFLOW.md` | `e2bb249d930ffef7a187c67210b1b0e6ac22ff25f0390a189ce7faa74da60e7d` |
| `tdd-optional/project/docs/PROCESS.md` | `dd811217033a866c3d6502d7dae2d5a68a775a090cf8b8e43ec56792cd586da1` |
| `tdd-optional/project/changes/README.md` | `47237bcd01ebcfe6dcd2d23bf8e940011cb575eb776464a8c90c9274cbf6d1f6` |
| `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md` | `f9f3c509c95196b1b349242d9dd29c3957020eeb3c0113a7686a659ad8342bfb` |
