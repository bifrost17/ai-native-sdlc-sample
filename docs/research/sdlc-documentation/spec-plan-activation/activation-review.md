# 활성화 독립 리뷰와 사용판 조정

2026-09-11. source는 codex/spec-plan-activation의 185dd5e 이후 작업트리,
사용판은 codex/use-template-0024의 787af77 이후 작업트리를 읽기 전용으로 검토했다.
검토자 Astra/high, 작성은 root 및 소유 파일을 나눈 에이전트다. 설치·제품 행동의 리뷰는 아니다.

## 검토 결과

후보 2d3f2dc와 활성 5사례를 대조해 입력 링크·provenance·정책 참조 외 핵심 계약 변경이 없고,
교육 입력 5파일이 바이트 동일함을 확인했다. 원본 candidate/inputs tracked diff 없음.
사용판 상대 Markdown 링크 152개가 실제 대상에 닿으며 자동 로드 .claude 디렉터리가 없다.
M01 현재 계약과 설계 정본, F03 현행 계약을 maker 연구 파일·Git 객체 없이 읽을 수 있다.
다문서 spec·실행 파일/TDD/PR/통합 plan, 기존 수락과 허가된 draft 재사용, 정당한 시험 수정과
종료된 공개 제어 단계의 구별, 선택 설치와 역사 SHA provenance가 일치한다.

유일한 P2는 사용판 B01/plan.md의 maker 전용 INTENT_TASK=fix 안내였다. root가 그 사용판
사본만 실제 프로젝트 보호 방법을 따르는 일반 문구로 바꿨다. 검토자가 수정 파일을 다시 읽고
"P2 해결. 이번 독립 활성화 리뷰 범위에 남은 중요한 발견은 없습니다."라고 회신했다.
maker 사본은 실제 훅을 설명하므로 유지했다. 광역 검사에서 발견한 기존 UX/accessibility 링크
4개는 이번 변경/필수 읽기 밖의 기존 상태이며 이 활성화에서 수정하지 않았다.

## 사용판의 의도적인 차이

- root templates와 교육 README/walkthrough의 지침 링크는 examples/skills로 바꿨다.
  설치 전에도 읽을 수 있고, 자동 로드 스킬을 제품 템플릿 자체에 넣지 않는다.
- 자체 design-spec/plan은 examples/skills에 두고 disable-model-invocation: true를 유지한다.
  팀이 설치 사본의 자동 사용을 선택하면 그 값을 제거하고 선택을 기록하도록 안내한다.
- maker plan의 INTENT_TASK 전용 문단과 B01 예시의 해당 문장만 제품 실제 보호 방법으로 바꿨다.
  도입하지 않은 훅이 작동한다고 주장하지 않는다. 나머지 과거 작은 예시는 보존하고 현행 예시로 연결한다.
- PROJECT-POLICY의 한 행에 새·변경 동작 TDD 방법·근거/예외 책임을 두며 CLAUDE는 그 행을 참조한다.
  코드·CI·제품 스킬·maker 정책 값은 자동 설치하지 않는다.

## 형식 검증

native `claude plugin validate --strict --json ./org-skills` 및 marketplace manifest 검증:
rc0, success true, errors/warnings 없음. manifest 검증을 모든 스킬 행동의 검증으로 세지 않는다.
quick_validate: design-spec, plan, spec-policy-pass, tdd, sdlc-feedback 모두 rc0/Skill is valid.
uv의 임시 PyYAML 환경을 사용했으며 프로젝트나 전역 Python 의존성을 추가하지 않았다.
source/use `git diff --check` rc0. 별도 maker verifier와 제품 실행 결과는 후속 기록에 둔다.
