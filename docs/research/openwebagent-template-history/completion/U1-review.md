# U1 review — 중요한 AC의 검증 접근과 plan 인계

검토일: 2026-10-03, Asia/Seoul.
검토 범위: U1 제작 자산 구현. 대상 파일의 전체 내용, 기존 0.1.9 후보 문구와 이번 미커밋 보완을 함께 읽었다.
판정: **이 범위에서 중요한 수정 요구를 발견하지 못했다.** root가 이 보고서의 근거와 범위를 판단한다. 사람의 수락·제품 실행 성공·패키지 완료 판정은 이 보고서에 포함하지 않는다.

## Scope and revision

- 작업 경로: `/Users/jake/Projects/ai-native-sdlc-sample`.
- 읽은 HEAD와 diff base: `e1f6f6fc998bda1ae595605f16ac64fd2c2850f0`.
- `tdd-optional/project/templates/spec.md`: base 대비 3줄 추가, 1줄 삭제. 검토 바이트의 SHA-256은 `d52f4293f164399b6724f37acedc40bc720fa96ac81104112e05d4fd7f18a6ed`.
- `tdd-optional/project/examples/skills/design-spec/references/design-depth.md`: base 대비 6줄 추가. 검토 바이트의 SHA-256은 `1e2e44fd385c200a81f33c2c56f24c3b4833b7a7df37e98642f215a0a52a0c3a`.
- 위 두 파일 이외의 미커밋·미추적 파일도 작업 트리에 있었다. 그 작업을 U1 수정으로 합치지 않았고, 변경하거나 되돌리지 않았다. 리뷰자가 작성한 파일은 이 보고서뿐이다.

현재 작업은 [0028 intent](../../../../intent/0028-openwebagent-history-feedback/intent.md)의 후속 실행 결정과 Constraints, [spec](../../../../intent/0028-openwebagent-history-feedback/spec.md)의 SP06–07·FR08·AC03/07, [plan](../../../../intent/0028-openwebagent-history-feedback/plan.md)의 T06에 해당한다. 중요한 AC의 독립 기대·경계·환경·실패/관측·미정을 plan으로 전달하고 작은 F01·선택형 TDD의 부담을 대조하는 범위다. T07 이후의 UI 설계·초기 통합 계획·정본 관리·전달·패키지 회귀는 각 후속 단위의 책임으로 남긴다.

## Inputs and criteria actually read

제작 지침은 `CLAUDE.md`, root `REVIEW.md`, 0028 intent/spec/plan 전체를 읽었다. 공통 판정 기준은 `/Users/jake/.codex/agents/sdlc-verifier.toml`의 Review criteria를 읽어 적용했다. 이 파일을 읽었다는 사실은 해당 named-agent 런타임 설정을 선택했다는 증거가 아니다. 과업의 명시적 보고서 작성 권한을 사용했으며 source 편집·승인·다른 에이전트/모델 호출은 하지 않았다.

북극성은 `docs/verification/north-star-playbook.html`의 다음 원문 문단과 주석을 대조했다.

- V3-09, 515–524행: spec이 문제를 풀고 미결 질문을 답하거나 이월하는지 사람이 검토한다. 현재 주석도 설계에서 필요한 입력을 plan으로 넘기는 문제와 정본 개정, 실행·수락 구분을 기록한다.
- V4-06, 616–623행: plan은 변경 파일·작업 순서·증명할 시험을 명시한다. TDD 순서를 모든 팀의 보편 의무로 바꾸지 않는다는 주석을 함께 읽었다.
- V8-02, 1130–1137행: 작업 중 피드백과 마지막 새 문맥 검토의 역할을 구분한다. U1의 문서 판정이 실행 피드백을 대신하는지 확인했다.

제품 작성 경로는 다음 전체 파일을 읽었다. 아래 경로는 모두 저장소 루트 기준이다.

- `tdd-optional/project/templates/spec.md`.
- `tdd-optional/project/examples/skills/design-spec/references/design-depth.md`.
- `tdd-optional/project/examples/skills/design-spec/SKILL.md`.
- `tdd-optional/project/templates/plan.md`.
- `tdd-optional/project/docs/TESTING-STRATEGY.md`.
- `tdd-optional/project/REVIEW.md`.
- `tdd-optional/project/docs/sdlc-authoring/examples/F01/spec.md`와 `context.md`.
- `tdd-optional/project/docs/sdlc-authoring/examples/W01/spec.md`와 `context.md`.

검토용 설치 스킬은 `sdlc-feedback`(설치 표기 0.1.7), `spec-policy-pass`, `brand`, `stop-slop-ko`(각 설치 표기 0.1.6)를 `/Users/jake/.agents/skills/<name>/SKILL.md`에서 읽었다. 설치 표기는 각 파일의 머리말이며 manifest와 실제 설치 바이트의 일치는 별도 검증하지 않았다. 제작 저장소의 실제 지침을 먼저 적용하고, 채택 제품용 예시 정책이나 비어 있는 P1을 제작 저장소의 새 승인 요건으로 옮기지 않았다. 새 endpoint·응답 필드·로그·보존 기간을 설계하는 변경이 아니므로 API 보안·데이터 처리 정책의 전수 감사는 수행하지 않았다. 한국어 보고서는 기술 검토 기록의 형식과 근거를 보존했다.

## Contracts examined and attempted counterexamples

### 독립 기대가 구현 결과를 따라가는 경우

대상 `templates/spec.md` 24–28행은 독립 기대의 출처, 실제 경계, 필요한 입력/환경, 실패 유도와 관측, 가상 경계의 한계를 연결한다. 추가한 26행은 구현이 낸 결과를 그대로 정답으로 쓰지 않도록 명시한다. 연결된 `design-spec/SKILL.md` 43–46행도 오너 결정·정책·프로토콜·고정 기준 데이터·독립 계산을 기대의 근거로 제시한다. `TESTING-STRATEGY.md` 8–19행과 70–83행은 이 출처와 검사 자체의 판별력을 확인한다.

반례 후보는 “테스트 이름을 쓰고 현재 실행 결과를 기대값으로 복사하면 충분하다”는 해석이다. 위 문구에 직접 위배되므로 유효한 충족 경로가 아니다. 독립 fixture를 언급하는 것만으로 기대가 자동으로 옳아진다고 주장하지도 않는다. 기준이 틀리거나 요구가 바뀌면 근거와 영향받는 검증을 함께 수정한다는 기존 전략을 유지한다.

### 가짜 API 응답으로 권한·저장 결과를 입증하는 경우

`design-depth.md` 31–35행은 저장 거절 시 기존 값 유지의 판별 예로 이전 값, 실제 권한 거절 경계를 통과하는 호출, 응답과 저장소 재조회를 연결한다. 가짜 API 응답을 쓴 컴포넌트 시험은 화면 상태의 근거라고 범위를 한정한다.

반례 후보는 “화면에 거절 문구가 보이면 실제 권한·저장도 검증했다”는 해석이다. 33행이 그 확대를 막는다. 실패 입력이나 응답 하나만으로 후속 상태를 추측하지 않고 재조회라는 관측도 연결하므로 SP06의 실패/관측 요구에 맞는다. HTTP 호출의 정확한 명령과 fixture 생성 절차까지 이 범용 예시에 고정할 필요는 없다. 실제 변경의 spec에서 의미와 관측 경계를 정하고 plan에서 작업별 절차로 구체화한다.

인접 사례 W01의 `context.md` 38–49행은 u1/u2/u3, 순서를 구별하는 기준 데이터, 권한·응답 검증의 실제 시험 API/저장소 사본과 화면 상태 시험의 제어 범위를 제공한다. `spec.md` 22–33행의 AC와 70–90행의 API 계약은 세션·공개·쿼리 거절 순서와 저장소 호출 유무를 구별한다. W01은 읽기 전용 사례이므로 저장 변경을 거절하는 위 예시의 실행 성공 사례로 계산하지 않았다.

### 작은 변경에도 HTTP·DB·별도 표를 요구하는 경우

`design-depth.md` 36–37행은 권한/저장 변경 예시의 적용 조건을 밝히고, F01 출력 필터에는 독립 입력·정확 stdout/종료 코드·보존 동작의 기존 시험을 사용할 수 있다고 설명한다. 모든 변경에 HTTP·DB·별도 검증 표를 요구하지 않는다는 문장이 추가됐다. `templates/spec.md` 28행도 작은 변경에 별도 표나 모든 테스트 본문을 요구하지 않는다.

F01 `spec.md` 11–22행은 완료 포함·정확 일치·순서·null 구별·빈 stdout·rc0·파일 바이트 불변·기존 동작과 읽기 실패를 구체적으로 정한다. 30–36행은 JSON 읽기→필터→기존 display라는 좁은 경계와 한 공개 단위를 설명한다. `context.md`에는 격리 입력의 경로와 Python 표준 라이브러리 환경/시험 명령이 있다.

반례 후보는 “stdout와 rc만 보면 F01의 무쓰기 AC도 자동 충족된다”는 해석이다. 대상 문구는 보존 동작의 기존 시험을 함께 요구하고, 직접 연결된 F01은 바이트 불변과 파일 생성 없음을 AC로 유지한다. 새 안내가 이 계약을 삭제하거나 stdout만으로 대체하지 않는다. 모든 범용 예시 문장에 모든 AC를 재기술하라는 수정은 이 범위의 중요한 결함으로 판단하지 않았다.

### 필요한 입력·환경을 이월하고 검증 준비 완료로 처리하는 경우

`templates/spec.md` 27–28행은 없는 입력/환경을 Open questions의 영향·해결 주체·필요 시점과 연결하고, 그 입력에 의존하는 검증의 준비 한계를 밝히게 한다. 같은 양식 64–67행에는 이월한 질문을 두고 지금 인계할 수 있는 이유를 쓰게 한다. `design-spec/SKILL.md` 54–55행은 설계를 무효화할 질문을 단순 담당자 지정으로 넘기지 못하게 하며 의존 인계 전에 해소하도록 한다. `design-depth.md`의 공유 의미와 이월 절도 다음 작업이 의존하는 미결과 실행으로 확인할 결과를 구분한다.

반례 후보는 “실제 경계를 검증할 입력이 없지만 담당자를 적었으므로 제품 완료나 모든 후속 작업 착수가 가능하다”는 해석이다. 새 문장의 준비 한계, 기존 의존 인계 제한과 충돌한다. W01 `spec.md` 150–152행은 운영 명령을 운영 담당이 공개/중단 리허설 전에 확정하며 그 전에는 운영 준비 완료로 표시하지 않는 정당한 이월을 보여 준다. 반대로 제품 설계를 무효화하는 입력을 같은 방식으로 무제한 이월하는 해석은 routing skill이 허용하지 않는다.

### spec과 plan의 책임이 뒤집히는 경우

`templates/spec.md` 24–28행과 `design-depth.md` 34–35행은 검증 의미·입력/환경·경계/관측을 spec에서 찾게 하고, plan에는 실행 순서·파일·명령/절차와 첫 실제 연결 시점을 맡긴다. `design-spec/SKILL.md` 37–39행은 중요한 설계/계약을 plan으로 밀지 못하게 한다.

실제 수신 양식 `templates/plan.md` 39–53행은 Design basis, Input, Strategy, Behavior와 Done에서 관련 AC·독립 기대·실제 명령/관측을 연결한다. 65–78행은 Proof의 한계, 예정 증명과 실제 기록, 계약 변경 시 spec·plan 개정 시점을 구별한다. `TESTING-STRATEGY.md` 43–53행도 이 분담을 유지한다. “spec에는 테스트 종류만 쓰고 의미는 plan 작성자가 나중에 정한다”는 충족 해석은 이 계약과 맞지 않는다. U3에서 다룰 전체 인도 순서의 실효성까지 여기서 완료 판정하지 않았다.

### 중요한 AC를 선택 항목으로 읽어 생략하는 경우

`design-depth.md` 1–5행의 제목과 도입은 필요한 표현 블록을 선택하도록 한다. 이 문맥만 떼어 읽으면 새 검증 접근 절도 생략 가능하다고 읽을 여지가 있다. 그러나 entrypoint `design-spec/SKILL.md` 30–34행이 실제 spec 양식을 사용하게 하고, 그 양식 24–28행은 중요한 AC의 판별 접근을 연결하라고 직접 요구한다. 같은 skill 43–46행의 입력·결과·중요 실패·독립 기대와 71–75행의 전체 설계 검토도 유지된다.

따라서 선택 대상은 표/블록·표현 방식이며 중요한 AC의 판별 근거 자체를 생략할 권한으로 해석할 수 없다. “중요한”을 판단하는 고정 점수표나 모든 AC별 별도 검증 장부를 추가해야 한다는 요구는 현재 intent의 얇은 보완 범위를 넘는다. 임의로 AC를 누락한 미래 실행이 발생할 가능성은 남지만, 그 가능성만으로 이 source에 중요한 계약 공백이 있다고 판단하지 않았다.

### TDD 선택형 회귀와 설계 검토의 실행 성공 오인

두 파일의 U1 변경은 테스트 선작성이나 RED를 요구하지 않는다. `design-spec/SKILL.md` 33–34행은 단일 작성 순서를 처방하지 않는 검증 전략 문서로 직접 연결한다. `TESTING-STRATEGY.md` 21–41행과 `templates/plan.md` 23–26, 47–51행은 TDD·구현 후 시험·기존 시험 활용·혼합과 이미 통과하는 보존 동작을 구분한다. 기대·판별 방법을 먼저 정하는 것과 테스트 코드 작성 순서를 고정하는 것은 이 문서에서 다른 결정이다.

`design-depth.md` 38–39행은 설계에서 기대/관측을 정한 사실과 실제 시험 확인을 구별하고 환경·성능·경합 결과를 설계 검토만으로 통과 처리하지 않도록 한다. 실제 완료 전 검사는 `TESTING-STRATEGY.md` 100–105행이 계속 요구한다. V8-02의 작업 중 피드백과 최종 검토 분리도 유지된다. 반례 후보였던 “문서 리뷰 통과로 실제 검증을 갈음한다”는 해석은 성립하지 않는다.

## Findings by pass

- Bugs: U1 문구를 따르면서 상충하는 검증 결과를 허용하는 중요한 누락을 찾지 못했다. 위 반례는 서로 연결된 실제 작성 지침과 대조해 기각했다.
- Security: 변경 diff에 credential·PII·새 외부 전송 또는 endpoint를 추가한 내용은 없었다. 권한/저장 예시는 mock 근거를 실제 권한 근거로 확대하지 못하게 한다. 제품 보안 실행 시험을 수행한 판정은 아니다.
- Compliance / policy and scope: SP06–07과 T06의 검증 접근·미정·작은 변경·TDD 선택형 요구와 충돌하는 변경을 찾지 못했다. 기존 0.1.9 U1 내용과 새 보완을 합쳐 판정했다. 스타일 취향이나 모든 상태의 선행 확정 요구를 finding으로 만들지 않았다.

요구할 source 수정, unresolved important finding, U1 내 보류할 결함은 없다. 이 결론은 검토한 해시의 두 제작 파일과 명시한 필수 인접 계약에 한정된다.

## Command evidence

검사 명령은 모두 정적 읽기·차이/파일 확인이다. 처음의 큰 출력에서 잘린 부분은 작은 범위로 다시 읽었다. command exit code는 모두 0이었다.

```text
pwd
/Users/jake/Projects/ai-native-sdlc-sample

git rev-parse HEAD
e1f6f6fc998bda1ae595605f16ac64fd2c2850f0

git diff --numstat e1f6f6f -- tdd-optional/project/templates/spec.md tdd-optional/project/examples/skills/design-spec/references/design-depth.md
6  0  tdd-optional/project/examples/skills/design-spec/references/design-depth.md
3  1  tdd-optional/project/templates/spec.md

git diff --check e1f6f6f -- tdd-optional/project/templates/spec.md tdd-optional/project/examples/skills/design-spec/references/design-depth.md
(output empty; exit 0)

shasum -a 256 tdd-optional/project/templates/spec.md tdd-optional/project/examples/skills/design-spec/references/design-depth.md
d52f4293f164399b6724f37acedc40bc720fa96ac81104112e05d4fd7f18a6ed  tdd-optional/project/templates/spec.md
1e2e44fd385c200a81f33c2c56f24c3b4833b7a7df37e98642f215a0a52a0c3a  tdd-optional/project/examples/skills/design-spec/references/design-depth.md
```

`python3 -c`의 `pathlib.Path.resolve()/is_file()`로 `design-spec/SKILL.md` 기준 spec 양식, design-depth, TESTING-STRATEGY, 제품 REVIEW, F01/spec, W01/spec의 6개 상대 경로를 확인했다. 모두 의도한 `tdd-optional/project/` 아래 파일로 해소됐고 `exists=True`였다. 이는 읽기 경로의 확인이며 자연 스킬 선택·설치 경로·전달 adapter 실행 검사가 아니다.

## Limits and handoff

제품 구현·개발 실험·모델 CLI 호출·브라우저·전역 설치·publication을 실행하지 않았다. F01/W01을 제품으로 실행하지 않았으며, F01 기준 코드/시험과 입력 파일을 실행하거나 전체 제품 회귀를 감사하지 않았다. 예시 spec/context의 계약을 기준으로 비례성과 검증 경계만 대조했다. 이 정적 검토가 실제 에이전트의 자연 선택·작성 품질·개발 효과를 입증하지 않는다.

`make check`, Claude strict 검사, Codex patch/패키지 전체 검증과 마지막 독립 완료 검토는 U1 단위 리뷰로 반복하지 않았다. T11과 최종 제작 검증의 책임이다. 기존 WIP의 의미와 전체 branch/PR는 이번 판정 범위 밖이다. 후속 source 변경이 위 해시의 의미를 바꾸면 해당 범위는 다시 검토해야 한다.
