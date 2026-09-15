# 배포판 분리 독립 구현 검토

2026-09-12. 기준 HEAD `13376e8049c5650c0fe3a8a258a6595f8d3ada8f` 이후의 작업 트리를 읽었다.
이 검토는 구현 담당과 분리된 문맥에서 수행했으며, 아래 보고서 외의 제품·코드 파일은 수정하지 않았다.

## 발견

### 해결됨: P2 — 선택형 평가가 기본형 플러그인의 스킬 이름을 요청한다

위치: `evals/cases/04-org-policy-application.json:4`.

최초 검토의 공유 prompt는 `intent-sdlc-skills:spec-policy-pass` 호출을 명시했지만, `SDLC_EDITION=tdd-optional`에서는
`tdd-optional/org-skills/.claude-plugin/plugin.json:2`의 `intent-sdlc-skills-optional` 패키지가 로드된다.
`evals/run.sh:68`의 경로 치환과 `evals/grade_assertions.py`의 `resolve_case`는 플러그인 namespace를
바꾸지 않았다. 선택형 평가에서 제공하지 않은 스킬을 요청하여 호출 실패 또는 잘못된 출처 선택을
유도하고, 실제 정책 적용을 평가하려는 사례에 불필요한 상충 입력을 준다.

생성 prompt와 채점 packet 모두 선택한 manifest의 namespace를 사용하도록 해석해야 하는 문제였다.
당시 mock 시험은 `--plugin-dir`와 제품 경로를 확인하지만 이 요청 이름을 확인하지 않아 통과했다.
실제 Claude API 호출 실패는 관측하지 않았으며, 이 발견의 근거는 요청된 식별자와 로드 대상의 불일치다.

같은 날 수정 후 집중 재검토했다. case 04는 `SDLC_PLUGIN_NAME`을 사용하고, 생성기와 채점기는
선택한 manifest의 `name`으로 이를 치환한다. 두 판에 대해 실제 jq 생성 prompt와 Python
`resolve_case` 결과를 직접 비교하여 동일한 namespace와 제품 경로가 들어감을 확인했다.
추가된 optional 생성 prompt 검사와 양판 채점 packet/source hash 검사 2건을 직접 실행해 통과했다.

`--bare`가 두 생성 경로와 채점기 모두에 전달되고 각 mock 검사에도 포함됨을 확인했다.
로컬 `claude --help`는 이 옵션이 CLAUDE.md 자동 탐색 등을 건너뛰고 명시적 `--plugin-dir`를 지원하며,
Anthropic 인증에 API key 또는 명시적 apiKeyHelper를 사용한다고 안내한다. 실행기의 기존 API key
선확인 조건과 맞는다. 유료 모델 실행이나 사용자 설정 전체의 런타임 격리를 시험한 것은 아니다.

집중 재검토 범위에서 미해결 P1/P2는 없다. 최초 발견과 보완 경위를 보존하며, 아래 초기 검토의
정적·mock·실행 한계는 유지한다.

## 확인한 보존 범위

- `84a77b3890cfdc97f3c6603f433e1382453ca261`의 71개 제품 파일과 `tdd-first/project/`의 71개 파일을
  Git 원본 바이트로 대조했다. 누락·추가·내용 차이는 없었다.
- 기본형 팀 패키지의 TDD·feedback·Claude/OpenCode 검증자 본문은 기존 기준
  `ece15c449452f6a425d049172e0e71aa94ebc180`과 유지된다. 배포 위치·동봉 자료 링크·어댑터 안내의
  개정은 제품 방식의 변경과 구별했다.
- 선택형 프로젝트 정책, 계획 양식·작성 스킬·예시, TDD/feedback, 두 검증자의 적용 조건을 읽었다.
  TDD 미사용만을 결함으로 판정하거나 새 예외 승인을 요구하는 현행 공통 규칙은 발견하지 못했다.
  TDD 예시의 선행 시험 및 실제 프로젝트가 채택한 보호 경계는 명시된 범위에 한정된다.
- intent/spec 양식, 인수 조건·독립 기대·회귀 보호·영향 문서 갱신과 기존 사람 결정 구조가 유지된다.
  기존 연구·실험·북극성 주석의 경로는 역사적 근거이며 현행 필수 실행 경로로 취급하지 않았다.

## 직접 실행한 확인

| 확인 | 결과 | 범위 |
|---|---|---|
| `python3 -m unittest discover -s tests -p 'test_template_editions.py'` | 3 tests 통과 | 두 제품을 임시 독립 폴더로 복사한 링크 폐쇄성·배포 패키지·공통 양식 |
| `python3 -m unittest discover -s tests -p 'test_eval_plugin.py'` | 7 tests 통과 | fake CLI 기반 선택판·생성 경로와 기존 결정론 검사 |
| `python3 -m unittest discover -s tests -p 'test_eval_semantic_runner.py'` | 8 tests 통과 | fake 생성/채점 기반 rc·출력 분리·호출 옵션 |
| 두 판의 OpenCode `sdlc-feedback`, `ux-copy`, `authoring-native` patch dry-run | 6건 모두 rc 0 | 독립 임시 복사본의 해당 파일에 `--batch --dry-run -p1` 적용 가능 |

## 한계

새 제품을 실제 모델로 개발하는 TDD·non-TDD 행동 시험, Claude/OpenCode 자연 호출·검증자 위임,
사용자 전역 설정과의 런타임 충돌, 유료 생성/의미 평가, 실제 플러그인 설치·갱신은 실행하지 않았다.
패키지 발견·정적 검토·mock 통과를 이 행동들의 성공으로 확장하지 않는다. OpenCode patch는 이 검토에서
dry-run만 수행했다. 이 보고서는 전체 북극성 준수 또는 모든 문서·연구 원문의 전수 검증이 아니다.

검토 중 구현 담당이 별도 작업 중인 검증 기록의 미생성 상태는 제품 결함으로 판정하지 않았다.
CodeRabbit CLI 실행·전역 설치는 하지 않았으며, 결과는 소스 직접 검토와 위 로컬 검사에 근거한다.
