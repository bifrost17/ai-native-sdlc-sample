# 작성 예시 활성화 기록

후보 source commit `2d3f2dc`의 승인된 F01/B01/F03/M01/W01과 change walkthrough를
`docs/sdlc-authoring/`의 사용 경로로 옮겼다. 이 기록은 소스 전달 범위이며 제품 구현·실행·수락 결과가 아니다.

| 후보 원본 | 활성 경로 | 포장 조정 |
|---|---|---|
| `candidate/examples/F01` | `docs/sdlc-authoring/examples/F01` | 입력 링크, 프로젝트 TDD 정책 링크 |
| `candidate/examples/B01` | `docs/sdlc-authoring/examples/B01` | 입력 링크 |
| `candidate/examples/F03` | `docs/sdlc-authoring/examples/F03` | 입력·공개 정책 링크, 역사 자료를 선택적 provenance로 표기 |
| `candidate/examples/M01` | `docs/sdlc-authoring/examples/M01` | current-contract를 예시 옆에 유지, 과거 maker 경로를 provenance metadata로 표기 |
| `candidate/examples/W01` | `docs/sdlc-authoring/examples/W01` | 공개 정책 링크 |
| `candidate/change-walkthrough.md` | `docs/sdlc-authoring/change-walkthrough.md` | 활성 design-depth/execution-depth reference 링크 |
| `spec-plan-design/inputs/{cases,*.json,baseline/*}` | `docs/sdlc-authoring/inputs/` | 예시가 읽는 최소 입력만 바이트 그대로 복제 |

활성 README는 필요별 진입점, 필수 읽기 경계, source path/commit과 합성 자료의 한계를 설명한다.
예시의 R/AC와 현재 계약은 바꾸지 않았다. `Upstream`의 역사 SHA는 원래 배치를 가리키며 새 경로의
과거 존재나 제품 승인을 뜻하지 않는다고 각 context와 README에 명시했다.

F03의 `f03-spec-historical.md`, `f03-plan-historical.md`와 handoff/실행 기록은 복제하지 않았다.
그 경로와 source commit `f1ba82e`/`5fc8bdc`만 선택적 provenance로 남겼다. M01의 선행 합성 자료도
maker 경로와 source commit `efa7339`만 남겼으며, 필수 현재 계약은 활성 사본 안에서 끝난다.

## 전달 검증

- `docs/sdlc-authoring/**/*.md`의 로컬 Markdown 대상 0건 누락.
- intent/spec/plan과 M01 설계·현재 계약 중 링크·포장 조정이 없는 파일 16/16이 후보와 바이트 동일.
- 다섯 spec의 `Requirements`부터 `Acceptance criteria` 끝까지 후보와 바이트 동일.
- cases, 두 JSON, baseline 코드·시험 5/5가 source commit의 입력과 바이트 동일.
- 활성 문서에서 연구/maker 자료로 향하는 필수 Markdown 링크 0건. 역사 경로는 선택적 provenance metadata로만 남음.
- 신규 패키지·기록 33파일의 trailing whitespace 0건, final newline 누락 0건. `git diff --check`도 rc0.
- `make check` rc0(96 tests, skipped 1; hooks 28/28; eval fixtures 8/8; managed settings PASS).
