# spec 양식 설계와 최종 판단

2026-09-11. 작성·수정·최종 판단: Codex root. **R2 문서 설계 통과.**
북극성의 요구·설계 통합과 사람/에이전트의 인계를 지원하는 수준으로 판단했다. 모든 후속 에이전트의
실수를 막거나 플레이북 전체를 자동 재현했다는 뜻은 아니다. 상태는 draft로 유지한다.

## 선택한 형태

관련 조사 12개 분석과 설계 방향, 원본 양식·작성 지침, 실제 적용 사례, 북극성 Lesson 3/4를
다시 읽고 [판단 근거](reading-notes.md)를 썼다. root가 기능·버그·이행의 합성 완성 예시를 작성한 뒤
[두 배치](alternatives.md)를 대조해 기본 여섯 구획과 필요한 Design 상세를 도출했다.

요구에는 바뀔 동작뿐 아니라 유지할 계약을 담고 AC는 여러 R을 연결해 대표 성공·실패·회귀를 확인한다.
설계에는 기존 구조와의 연결·선택 이유·중요한 계약을 남기며 실행 파일·순서·명령은 plan에 둔다.
제약/제외 범위를 합치고 질문은 intent 출처에 한정하지 않는다. 중요한 미결은 담당자 이름만으로
해소되지 않으며, 결정이 바뀌면 해당 계약과 영향받는 기존 계획을 갱신한다.

양식은 [templates/spec.md](../../../../templates/spec.md), 작성 과정은
[design-spec](../../../../.claude/skills/design-spec/SKILL.md), 상황별 깊이와 판 확인은 필요할 때
읽는 참조에 둔다. 새 문서 상태 원장·의미 검사기·CLI·플러그인·필수 승인 단계를 만들지 않았다.
기존 plan 양식과 정책 플러그인을 수정하지 않았다.

## 같은 후보를 검토한 두 모델

R1 첫 판정 전에는 서로의 보고서를 제공하지 않았다. root만 작성했고 리뷰어는 읽기 전용이었다.
R2에서는 각자의 R1 맥락과 root의 변경 설명을 재사용하되 서로의 보고서는 읽지 않았다.

| 리뷰어 | 설정 / 실제 모델 | R1 | R2 |
|---|---|---|---|
| Astra subagent | gpt-6-astra / ultra | [FAIL](reviews/astra-r1.md): 복구 후 쓰기 재개 회귀 | [PASS](reviews/astra-r2.md): 중요 발견 해소 |
| 실제 Claude Code CLI | fable / max, 실제 claude-fable-5-1 | [PASS](reviews/fable-r1.md), 비차단 보완 | [PASS](reviews/fable-r2.md), 중요 모순 없음 |

두 최종 보고의 후보는 [R2 영수증](reviews/candidate-r2.json)의 33파일이다.

```text
f4b37b76c06a28360bdf6bce56f2ebd3289b905b88d5135011ac6c43e337de02
```

Astra와 독립 verifier는 실제 파일 해시를 재계산했다. Fable은 Read/Glob/Grep만 있어 해시를
재계산하지 못했고 실제 본문과 영수증에 제공된 값의 대조로 검토했다.
R1 후보는 maker 4f52028/adopter 3e2f693, R2는 efc65d9/ca87cdb에 남겼다.

root는 R1의 PASS를 다수결로 채택하지 않았다. 최신 JSON으로 돌아가도 동시 쓰기 결함이 다시
생길 수 있다는 Astra의 구체적 지적을 받아, 합성 입력의 운영 결정과 R4·AC4·Design·Q2를
함께 고쳤다. 사본 검증, 쓰기 여부 미확인 처리와 제공되지 않은 백업의 사실 구별도 보완했다.
[수정 내역](reviews/r2-changes.md)에 각 반영 범위가 있다.

Fable R2의 읽기 전용 운영 같은 대안이나 추가 설명 권고는 비차단 의견으로 보존했다. 사례의
명시적 중지 선택을 다른 운영 방식으로 확대하지 않았으며, 실제 복구 명령·시험 환경은 plan에 남겼다.
스타일이나 가능한 모든 상황을 수용하려 최종 후보를 계속 늘리지 않았다.

Fable CLI의 두 호출은 rc=0, 합산 약 962초, list 기준 비용 추정 약 $9.21였다. 실제 청구액이나
HUMAN 검토 시간을 뜻하지 않는다. 호출 프롬프트·모델·사용량·도구 기록을 reviews에 보존하고,
각 export.json에 원시/저장 해시와 비공개 추론 제외 수를 남겼다. 추론 내용은 저장본에 없다.

## 독자 인계와 실제 대화

두 리뷰어는 세 예시에서 변화·보존·선택 이유·수용 근거·미결을 다시 설명했다. M01은 보고서 소비자
발견과 복구 판단이 같은 spec의 현재 계약에 반영되는지 대조했다. 이는 문서 인계 검토이며 실제 이행은 아니다.

[Sonnet/medium과의 6회 대화](probe/README.md)는 별도 사용 파생 브랜치에 보존했다.
spec 작성·리뷰·계획 인계, 후속 동작 변경에 따른 spec/plan·상류 SHA 갱신, 오류 리뷰·복구를
실제로 관측했다. 초기 I/O 검증 과장과 빈 문자열 계획 오류를 숨기지 않고 기록했다. 기존 시험은
통과했고 코드·데이터·원래 intent는 보존했다. 새 기능 구현·시험, 문서 언급 없는 자율 갱신 성능,
자연 질문·자동 스킬 발견·전체 SDLC를 검증한 것은 아니다. 최종 인계 수락은 simulated HUMAN의 결정이다.

## 검사와 전달

독립 verifier의 [초기 보고](reviews/verifier-initial.md)와 [전체 make check 출력](reviews/make-check.log)을
보존했다. Python 96개 중 1 환경 skip, hooks 28, deterministic evals 8, managed settings가 통과했다.
Q1 누락 음성은 실제 실패했고 정책·문서 인계 관련 20개 Proof도 통과했다. R2의 fixture 이동 뒤에도
기존 eval 검사는 통과했다. 최종 해시·scope·링크·주석 원문 대조는 별도 검사 기록에 남긴다.
최종 변경 뒤 [독립 verifier](reviews/verifier-final.md)가 make check와 양성·음성 대조를 다시
실행해 같은 결과를 확인했다. 33파일 해시·12개 대응·scope가 일치하고 북극성 원문·179개 ID/판정은
보존됐다. root의 [자료 검사](reviews/artifact-checks.json)에는 로컬 링크와 CLI 로그 추론 제외 확인도 있다.

Codex quick_validate는 maker skill에서 통과했지만 Claude Code의 disable-model-invocation 키는
지원하지 않아 adopter에서 실패했다. [공식 Claude 필드 확인과 로그](reviews/verifier-initial.md)를
근거로 플랫폼 범위 차이를 구별했다. 옵션이나 검사 코드를 지워 가짜 통과를 만들지 않았다.
make evals는 API key 없음으로 rc=2 SKIP이며 semantic PASS가 아니다.

[사용판 대응](delivery.md)에 따라 실제 후보 ca87cdb에도 intent·spec 양식과 선택 지침을 전달했다.
References applied, 선택형 examples/skills, 제작 자산 제외를 유지하며 새 설치 의무는 없다.
북극성은 관련 세 주석에 관측만 추가하고 기존 판정·ID·원문을 보존한다. 호스티드 PR·merge·배포는 미수행이다.
