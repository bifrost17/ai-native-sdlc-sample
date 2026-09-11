# Plan: spec 양식의 예시 작성·설계 비교·독립 검토
Upstream: spec.md@1bc0573. Status: draft.
사용자의 root 작성·충분한 설계 검토 위임으로 draft에서 진행한다. 실제 승인은 기존 merge 정책을 따른다.

## Files that change
제작 변경의 기준은 직전 intent 양식 완료 `a734b29`다. main부터 이 기준까지의 조사·intent 양식
변경은 별도 완료 작업으로 구분한다.

- intent/0021-spec-form/{intent,spec,plan}.md: 제작 변경과 실행 근거.
- templates/spec.md, .claude/skills/design-spec/SKILL.md: 공통 양식과 작성 지침.
- CLAUDE.md, .claude/commands/spec.md: R1 검토에서 확인한 양식 위치 설명과 이미 허용된
  초안 작업 예외의 연결 문구를 현행 작성 지침에 맞춘다. 새 절차는 추가하지 않는다.
- .claude/skills/design-spec/examples/**(new): root가 작성한 합성 입력과 완성 예시.
- .claude/skills/design-spec/references/*.md(new): 필요할 때 읽는 작성 상세와 출처 확인 지침.
- evals/cases/03-spec-carries-questions.json, evals/testdata/{03-pass,03-fail-carry}/ws/spec.md:
  새 절 이름/배치에 맞춘 안내. 누락 실패·정책 적용·R/AC 기준은 유지한다.
- docs/research/sdlc-documentation/spec-design/(new): 재독·입력·대안·갱신 사례·리뷰 요청·해시·
  모델 원문 결과·검사 로그·부분 실험·사용판 대응 기록. 비공개 추론은 로그에서 제외한다.
- docs/research/sdlc-documentation/README.md, README.md: 결과 및 사용 후보 색인.
- docs/verification/north-star-playbook.html: 관련 주석에 이번 관측 범위만 추가. 원문·기존 평가 보존.

별도 사용 후보는 codex/use-template-0017@add296d에서 codex/use-template-0021로 파생한다.
그곳의 templates/{intent,spec}.md와 examples/skills/{capture-intent,design-spec}/SKILL.md,
필요한 예시/참조 파일, examples/README.md만 갱신한다. 직전 0020 intent 양식도 이미 검토한
내용을 전달하고 선택 스킬의 선택성을 유지한다. 제품 코드나 제작 검증 자산은 넣지 않는다.
원본과 다른 사용판의 관련 내용은 별도 후보 해시·검토 범위로 기록한다.

## Order of work
1. root가 종합 조사·설계 방향·관련 원문·실제 사례를 재독한다. Astra는 독립 설계 도전,
   Sol은 기존 소비자·배포 경계를 읽고 보고한다. 작성은 root가 한다.
2. 작은 기능·정밀한 버그·데이터 이행 예시와 새로운 발견으로 바뀌는 결정을 작성한다.
   두 가지 정보 배치에 넣어 중복·빠진 계약·상세 확장·갱신 부담을 대조하고 양식을 도출한다.
3. 양식·스킬·필요한 예시/참조와 기존 eval의 안내를 함께 수정한다. 근거와 선택하지 않은
   대안을 기록한다. 문서 의미를 판정하는 새 검증 코드는 만들지 않는다.
4. 후보 해시를 고정하고 Astra/ultra·Claude Code Fable/max에 같은 자료를 읽기 전용으로
   제공한다. 첫 판정에 다른 리뷰어의 결과를 주지 않는다. 중요한 지적을 root가 수정하며,
   변경 범위에 대해 두 리뷰어의 같은 최종본 PASS를 받는다.
5. 사용 후보를 파생해 공통 양식과 선택 예시를 전달한다. 배포 차이의 검토·실제 파일 대응을
   확인한다. 기존 semantic eval을 실행할 수 있으면 실행하고, 그렇지 않으면 환경 한계와 함께
   Claude Code Sonnet의 좁은 Design→Plan 인계·갱신 대화 검토로 관측 범위를 보완한다.
6. 독립 verifier가 make check, 실제 Proof, 인접 0020과 훅 부정 입력을 확인한다. 자료 링크·
   최종 해시·배포 범위·북극성 원문 불변을 확인하고 주석·판정·로컬 커밋으로 보존한다.

## Risks
양식의 항목 수를 개선 성과로 오인, R/AC 반복, 알려지지 않은 사실·수치·정책을 발명,
불확실한 설계를 확정해 인계, 수락된 과거 판을 현재 판 승인으로 오인, 실사용 분기 누락을 본다.
질문 담당 미정은 허용하지만 중요한 정책 충돌의 해소로 취급하지 않는다. 상세를 추가하는 판단은
강한 설계 모델로 검토하되 모든 미래 모델의 실수를 막는 규칙으로 확대하지 않는다.

## Proof
두 독립 리뷰의 같은 후보 PASS, 세 유형의 문서 인계와 결정 변경 전후 대조,
bash tests/test_evals.sh의 03-pass/03-fail-carry 양성·음성 대조,
tests/test_eval_plugin.py의 정책 적용·변경 경로 연결 검사,
tests/test_team_harness.py의 전체 문서 인계 회귀,
make check 전체 로그와 기존 skill quick_validate.py,
가용한 경우 make evals(생성+독립 의미 채점) 또는 명시된 범위의 실제 CLI 대화 결과,
독립 verifier 네 부분 보고. 정적 파싱 통과를 의미·행동 검증 통과로 바꾸어 쓰지 않는다.

## Execution record

root 재독·합성 예시·두 배치 비교 후 R1 후보를 maker 4f52028/adopter 3e2f693에 보존했다.
Astra R1 FAIL의 복구 회귀를 R2에서 고치고 Fable의 필요한 비차단 보완과 실제 대화의 검증 범위
오류도 반영했다. R2 maker efc65d9/adopter ca87cdb의 같은 33파일을 Astra/ultra와 실제
Claude Code Fable/max가 PASS했다. [판정·수정·실행 기록](../../docs/research/sdlc-documentation/spec-design/review-record.md).

Sonnet/medium과 같은 세션에서 여섯 차례 문서 인계·변경·리뷰 대화를 수행했다. 초기 오류를 HUMAN이
고친 최종 문서 인계 통과이며 자율성·제품 구현·전체 SDLC 성능으로 확대하지 않는다. make evals는
키 없음 rc=2 SKIP이다. 독립 verifier의 Codex validator 실패는 Claude 전용 필드와의 도구 범위
차이로 원문 로그를 보존했다. 사용판 옵션을 지우거나 새 검사기를 추가하지 않았다.
최종 독립 검사에서 make check·03 양성/음성·33파일 해시·배포 scope·북극성 원문 불변이 확인됐다.
[최종 verifier 보고](../../docs/research/sdlc-documentation/spec-design/reviews/verifier-final.md)와
[자료 검사](../../docs/research/sdlc-documentation/spec-design/reviews/artifact-checks.json)에 근거를 남겼다.
이후 root는 보고서·로그·완료 링크만 추가했고 R2 핵심 파일은 유지했다. 이 계획의 작업은 로컬 반영까지 완료했다.
