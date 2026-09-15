# 실행 결과: 문서 추적과 커밋·인계 보완

2026-09-15 (Asia/Seoul). root 판정: **제작용 소스와 제한 인계 확인 통과**.
두 배포판의 정책 차이를 유지하면서 요구·설계·작업을 연결했다. 한 번의 HUMAN 피드백으로
부분 실험의 문서 누락을 보완했다. 전체 제품 SDLC나 에이전트의 무오류를 판정한 결과는 아니다.

## 구현과 검토

새 spec 요구 FR/NFR, 주요 설계 SP, plan 작업 T를 같은 개발건의 안정 ID로 연결했다.
중요 계약·컴포넌트·결정은 한 정본에서 정의하고 plan은 그 의미를 실제 파일·방법·검증·Done·PR로 잇는다.
기존 R/AC/P와 과거 판은 유지했다. intent 양식과 capture-intent 두 판은 기준판과 바이트가 같다.

항상 읽는 프로젝트 정책에는 실제 diff의 의미를 문서와 대조한다는 원칙을 짧게 넣었다.
기존 sdlc-feedback이 커밋의 staged/관련 미포함 범위, 영향 문서의 같은 커밋 포함, 결과 내용,
중단·인계·재개의 현재 plan 요약과 Git·근거를 대조한다. 새 스킬·승인 단계·검사기는 만들지 않았다.
plan 작성은 기존 스킬을 개정했으며 별도 스킬을 중복 설치하지 않는다.

Astra/high가 작성 자산을, Sol/high가 정책·feedback을 구현했다. root가 예시·패키지를 통합했다.
F01은 한 SP/T로 유지했다. M01은 기존 세 설계 정본에 SP를 연결하고 T01–T07을 구분했다.
예시 검토에서 T06 문서 인도와 T07 사본 리허설이 서로를 기다리는 순환을 찾아 정리했다.
Q4 입력 수집·초안은 병행할 수 있고, 확인된 문서 뒤 리허설을 수행하며 그 성공 후 실제 전환한다.
P-C의 코드 통합과 AC7의 실제 운영 검증도 구분했다.

새 문맥 [Astra/high 리뷰](../reviews/astra-high.md)는 제품 소스 60개에서 중요한 발견 없음으로 보고했다.
리뷰 대상 제품 소스의 SHA-256은
`f68443b3c5e6b661c30ba5d892bf37ee1a896e025bf25f98fcaba4b3f36cd65a`이며,
[설치·소스 대조](install-source-comparison.json)가 그 판을 다시 확인했다.
최종 staged 검사에서 새 traceability 두 파일의 끝 빈 줄을 지웠다. 의미 변경은 없으며
최종 소스 해시와 임시 설치본의 같은 수정은 [최종 판 대조](source-final.json)에 보존한다.

## 정적·설치 결과

| 근거 | 실제 결과 | 한계 |
|---|---|---|
| [make check](make-check.txt) | unittest 102개, 1 skip; hooks 28개; eval fixture 8개; managed settings 통과 | semantic 모델 eval이나 제품 실행 아님 |
| [Claude strict](claude-strict.txt) | 두 plugin, 두 edition marketplace, root marketplace 모두 통과 | Claude 세션 행동 아님 |
| [source 확인](source-static.txt) | 두 intent/capture 불변, 0.1.11/0.1.7 다섯 manifest 일치, YAML 10개·Codex TOML 파싱 | ID 의미나 사람 판단의 자동 보장 아님 |
| [임시 설치 manifest](installation-manifest.json) | first OpenCode 131파일, optional OpenCode 136파일, optional Codex 140파일. 각 판의 세 patch를 fuzz=0 dry-run·적용 | 개인 설치·OpenCode 모델 실행 아님 |
| [설치 대조](install-source-comparison.json) | 의도한 runtime 변환 외 파일 불일치 없음. 기존 explicit-only 정책과 verifier 기준 유지 | native named agent 자동 선택 증거 아님 |

skill-creator의 quick_validate는 기본 Python에 PyYAML이 없어 실행할 수 없었다.
실제 패키지는 Claude strict와 Ruby YAML, 번들 Python 3.12의 tomllib으로 확인했다.
제공 patch의 줄 위치를 재생성했고 최종 git diff --cached --check는 통과했다.

## 제한 행동 확인

대상은 선택형 0.1.7 후보를 복사하고 Codex patch를 적용한 작은 합성 조회 fixture다.
별도 Git baseline `codex/trace-handoff-fixture@cfc5470`에서
`codex/trace-handoff-probe-01`을 만들었다. maker와 제품의 작업 공간·Git 이력은 분리했다.
[원본 입력](probe-input.json), [첫 요청](probe-prompt.txt), [root 시험](probe-root-check.txt)을 보존한다.

Sol/medium의 새 문맥에 로컬 sdlc-feedback을 **명시 지정**했다. 새 코드 개발 전체 대신,
HUMAN이 제공한 변경 초안의 관련 커밋·인계를 요청했다. 초기 spec은 대소문자 구분,
후속 요청과 staged 초안은 casefold 완전 비교였다. 입력·순서 보존과 trim/부분 검색 금지는 유지했다.
에이전트가 새 세션에서 스킬을 자발적으로 선택했거나 문서를 구현 전에 수정했다고 주장하지 않는다.

| 단계 | 관찰 |
|---|---|
| [최초 제출](probe-response-01.md), 53c60dd | FR01/AC01/SP01과 T01 구현 방법·현재 인계를 갱신하고 코드·시험·execution과 같은 커밋에 포함. intent와 root의 E02 기록을 보존하고 scratch/ 제외. E02의 실제 파일 해시를 재사용하며 새 시험 실행을 주장하지 않음 |
| [새 독자](../reviews/probe-reader-01.md), Sol/medium | 작성 대화·코드/시험 본문 없이 문서·Git으로 계약, FR/NFR→SP→T, 파일·방법과 실제 남은 검토를 설명. plan에서 PR-A/Done이 사라지고 결정 출처가 불명확한 점을 발견 |
| [HUMAN 피드백](probe-feedback-02.txt)과 bc80ef8 | 기존 plan의 Done/PR-A 복원, spec 근거를 기존 실행 기록과 연결, E04에 후속 결정과 현재 인계·미완료 경계 기록. 코드·시험 변경 없음 |
| [독자 재확인](../reviews/probe-reader-02.md) | 두 누락의 해소를 문서에서 확인. 제품 완료·수락으로 확대하지 않음 |

첫 결과는 인계 누락을 포함했다. 새 규칙이나 검사를 추가하지 않고 이미 있는 작성 원칙으로
한 번 보완했다. 최종 결과는 중요한 추적·문서 갱신·인계 목적을 충족한다.
실제 제품 코드의 완결성, 모든 AC의 독립 회귀, TDD 순서, 장시간 재개, 여러 개발건·PR,
복잡한 설계 변경에서의 자연 사용은 이번 확인에 포함하지 않았다. trim 금지의 별도 자동 사례와
독립 제품 검토·PR 통합·배포는 fixture의 다음 담당자에게 남았다.

## 보존과 Git 인계

[최종 snapshot](probe-final.json), [Git bundle](probe-history.bundle), [bundle 확인](probe-bundle-verify.txt)에
초기 baseline, 최초 제출 53c60dd7a7beb509c27ff1d1f07f9933c009fd47,
문서 보완 bc80ef851cd082ffa1b4c1e8bbd265503e4b01f3와 두 branch를 보존했다.
scratch/의 미추적 초안은 입력/최종 snapshot에만 있고 제품 커밋에는 없다.
bundle을 새 디렉터리에 clone하면 임시 작업 공간이 없어도 커밋과 branch를 다시 읽을 수 있다.

제작용 구현 `3f51398`을 `codex/traceable-artifact-handoff`에서 커밋한 뒤 깨끗한 로컬 main에
fast-forward했다. 실제 소스 커밋과 Git 상태는 [Git 인계](git-handoff.md)에 기록한다.
기존 미추적 연구 두 폴더는 보존하며 이번 제품 설치 경로의 의존성으로 만들지 않았다.
개인 스킬 설치본, 별도 제품, 원격 push/PR, 기존 북극성 주석의 과거 판정은 변경하지 않았다.
