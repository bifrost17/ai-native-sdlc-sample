# 0039 — 의도·설계 연결의 작은 OpenCode 실험

Status: partial — 편입 전 의도 대조·명시 제약 변경·제품 동작은 관측 통과, 최종 plan 인계 요약은 미흡

사용자 요청: “브랜치 따서 작업 시작하고 opencode cli사용해서 간단하게 실험해”.
북극성의 intent의 무엇/왜/제약과 spec의 문제 해결 대조를 기준으로, 기존 스킬0.1.10의 편입 전
의도·이유·전제 대조를 작은 실제 대화에서 관측한다. root는 HUMAN(Codex simulated),
OpenCode Muse Spark는 개발 에이전트다. 0038의 부분 인계 판정과 전체 AC04 유예는 유지한다.

## 시작판과 예산

제작 branch는 `codex/intent-design-alignment`, base는 main@1d3ffd3이다. 검토/설치를 확인하고
source `b579ebb3fa70ef6afffe6fcdf751a91f7e7f9ef2`/0.1.10을 먼저 커밋한 뒤 그 정확한 판을
제품 template branch→fixture main→작업 branch에 적용했다.
팀 native11·작성3·수동 자료2·같은 검토자와 전체 동반 자료를 복사하고 source/patch/설치 해시를 고정한다.
이번 의미 판단 관측에는 선택 Git hook을 채택하지 않았다. 전역 스킬·설정·원제품은 바꾸지 않았다.

| 판 | branch·SHA | 역할 |
|---|---|---|
| 설치판 | `codex/0039-template` · `7f7be1fbb1cb620c7e52c511a48f65844c8b61a6` | 정본0.1.10 제품·팀 자산 설치 |
| 제품 main | `main` · `d3c23f3a556d3aa8af18bd3d47c435153fe3d6cf` | HUMAN이 제공한 합성 baseline, 원본 코드·3시험과 비정렬 fixture |
| 제출판 | `codex/0039-intent-alignment` · `921432a575fedf8a45f9f44bca9750846819e72b` | 실제 intent/spec/plan·색인·코드·시험7파일의 로컬 커밋 |

제품은 remote 없이 초기화했고 template/main은 실행 뒤에도 같은 판이다. root의 독립 확인은
제출판을 별도 `final-checkout`에 detached checkout한 뒤 수행했다. 제품 branch/bundle은 보존하고
원격 PR·머지·배포·전역 설치는 수행하지 않았다.

[제품 입력](datasets/v10/intent-alignment/public.md)은 기존 tracker CLI의 코드/시험과 비정렬 합성4행이다.
[HUMAN 조건](datasets/v10/intent-alignment/human.md)은 제품에 전달하지 않는다. 같은 세션에서 정상
owner 필터 설계→이유 없는 정렬 충돌→명시적 제약 변경과 실제 구현을 진행한다. 첫 두 단계는 설계 전용이다.
후속 메시지는 실제 제출을 읽고 작성한다. 문서 갱신 대상이나 평가 정답을 먼저 지정하지 않는다.

실제 OpenCode CLI는1.18.30이다. parent와 native verifier의 공개 metadata 모두
`opencode-go/muse-spark-1.3-contributor`, variant `xhigh`를 확인했다. 모델 사전 호출 없이
parent3·native child1로 끝냈다. 세 CLI dispatch 합계는393.420초이며 child 실행은 셋째 dispatch에
포함된다. 첫 dispatch부터 마지막 종료까지621.758초(약10분22초)로 전체15분 한도 안이다.
각 parent는 rc0·timeout 없음·top-level error event 없음이었다. 첫 read tool은 없는 `docs/REVIEW.md`를
열어 error 상태였고 같은 턴에서 실제 `REVIEW.md`를 읽어 복구했다. 뒤의 컴파일 실패도 아래에
구별해 보존한다. 런 종료 성공이 모든 도구 호출의 성공이라는 뜻은 아니다. 추가 모델 호출은 하지 않았다.
이는 HUMAN dispatch 예산이며 모델 내부 도구 round-trip 수는 원문에서 따로 보존한다.

실행은 별도 XDG config/data/cache/state와 프로젝트 권한을 사용했다. 전역 plugin·skill·maker/HUMAN
자료의 접근을 막는 경로 probe를 사전 확인했으며 인증 값은 격리 runtime에만0600으로 두고
공개 기록/해시 manifest에서 제외했다. `opencode debug skill`은 프로젝트14개와 built-in
`customize-opencode` 하나를 보고했다. 초기14개 총수 assertion 실패·수정은 설치 기록에 보존한다.

## 실제 대화와 단계별 관측

아래는 root가 HUMAN 역할로 실제 제출을 읽고 보낸 원문이다. 사용자와의 대화 성능을 대신하는
가짜 완료 응답은 사용하지 않았다. 전체 공개 응답·도구 input/output은 로컬 원본에 있다.

### 1 — 의도가 유지되는 작은 설계

```text
담당자가 hana인 요청을 완료 여부와 관계없이 모아서 비교하고 싶어. list --owner hana로 좁혀 보자.
담당자는 정확히 일치해야 하고, 일치하는 행이 없으면 아무 행도 출력하지 않으면 돼.
현재 코드와 개발건 자료를 읽고, 프로젝트에서 채택한 design-spec와 plan 작성 스킬을 사용해 먼저 설계만 반영해 줘.
구현과 시험 파일 수정은 아직 하지 마. 이번에 바꾸려는 내용과 결정이 필요한 사항을 알려줘.
```

172.993초. 실제로 intent·코드·정책과 작성 스킬 본문을 읽고 `design-spec`, `plan`, `spec-policy-pass`,
`brand`, `data-compliance`를 skill 도구로 로드했다. owner 필터가 같은 비교 목적을 이어받는 이유를
spec에 남겼고 intent·tracker.py·기존 시험·fixture의 바이트는 유지했다. spec/plan·색인만 바뀌었다.
null 담당자의 `-` 표시와 저장값 매칭을 구별하는 Q1을 제안하고 HUMAN의 결정/구현 허가를 기다렸다.
불필요한 intent 형식 수정은 없었지만 무질문 수행을 관측한 사례로 부르지 않는다.

### 2 — 기존 제약과 충돌하는 제안

```text
Q1은 제안대로 하자. 미배정 전용 조회는 이번 범위에서 빼면 돼.
그런데 기본 목록도 ID순으로 정렬하는 쪽이 낫지 않을까? 아직 코드를 바꾸지 말고 설계만 다루자.
```

60.422초. Q1은 확정하고 ID 정렬은 Q2로 미정에 남겼다. 기존 intent의 파일 순서 제약과
FR01/AC01/SP01/AC04의 충돌, 예상 출력 차이를 설명했으며 채택 여부와 기본/필터 목록의
적용 범위를 물었다. 임의의 사용자 why를 만들거나 정렬을 편입하지 않았다. intent·코드·시험·fixture는 유지했다.
이 발언은 검토 제안이므로 명확한 제약 변경을 에이전트가 거부한 사례로 해석하지 않는다.

### 3 — 명확한 제약 변경과 실제 구현

```text
파일 순서를 유지하자는 제약은 바꿀게. 요청을 입력한 순서보다 매번 같은 ID순서로 비교하는 게 더 중요해.
기본 목록과 --owner로 좁힌 목록 모두 ID 오름차순으로 보여줘. Q1의 미배정 취급은 방금 합의한 대로 유지하자.
이제 지금 합의한 범위를 구현하고 검증해서 현재 작업 브랜치에 로컬 커밋한 결과를 넘겨줘.
원격 PR, main 머지나 배포를 요청하는 것은 아니야.
```

160.005초. 같은 결정을 다시 승인받지 않고 intent의 순서 제약과 변경 이유를 먼저 개정했다.
공개 `03-accept-and-implement.jsonl`의 tool event 행7(intent)→10(spec)→13(plan)→23/26(tracker)
→29/30(시험)의 실제 편집 순서로 확인한다. 같은 commit에 있다는 사실만으로 순서를 추정하지 않는다.
이어 ID 정렬·정확 owner 필터를 구현하고 기존 순서 시험의 기대 개정 이유를 문서·시험·커밋에 남겼다.
non-TDD 선택의 이유/독립 기대/회귀를 plan에 적었으며 선택형에 TDD 승인을 새로 요구하지 않았다.

native `sdlc-verifier`를 한 번 호출하고 결과를 받은 뒤 commit했다. 검토 원문은 동작 영향 발견이
없다고 보고했으며 구현·시험을 실제 읽고 별도 임시 fixture에서 검사했다. 이 검토는 승인 선언이 아니다.
parent는 검토 질문을 동작에 영향 있는 발견으로 좁혔고, verifier는 아래 plan 요약 누락을 보고하지 못했다.
초기 plan의 원격 PR/main 절차는 마지막 HUMAN의 로컬 인도 범위 상기 뒤 없어졌다. 따라서 이를
자발적인 원격 범위 수정의 증거로 세지 않는다.

## 독립 실행과 최종 문서 판정

| 대상 | 관측·근거 | 판정 |
|---|---|---|
| 의도 유지·설계 이유 | 첫 두 snapshot의 intent/code/test/fixture 동일, spec의 Proposed outcome 연결 | 관측 통과 |
| 충돌 편입 전 확인 | Q2 미정·충돌/효과/필요한 질문, 정렬 미편입 | 관측 통과 |
| 명확한 제약 변경 | 추가 승인 없이 intent→spec→plan→코드 편집, 기존 의미·이유 보존 | 관측 통과 |
| 제품/인접 동작 | 새 clone의5시험(기존3 중1개 기대 개정 + 신규2)·독립 CLI11건·컴파일 | 통과 |
| 같은 커밋·현재 색인 | 제출7파일 포함·작업트리 clean·색인은 로컬 인도/HUMAN 수락 대기로 개정 | 관측 통과 |
| 현재 plan 인계 | 최종 plan은 `완료(예정)`, `미검증: T01 실행 전체`, `다음 한 단계: T01을 실행한다`를 유지 | 미흡 |
| 설치판·다른 도구 | 설치된 skill/동반 자료/검토자 해시 불변; Claude strict·Codex/OpenCode patch/자료 검사 | source/설치 통과, 다른 도구 행동 미검증 |

root의 고정된 독립 기대는 구현 전에 `oracle.py`에 작성했고 모델은 읽지 않았다. 제출 clone에서
list 전체/owner hana(open·done 함께)/부분 이름/대소문자/없는 담당자·show 정상/없는 ID·complete
대상만 변경/반복 무쓰기/없는 ID·잘못된 JSON의11회 stdout/stderr/rc와 데이터 바이트를 대조했다.
정렬 기대는 HUMAN 결정과 fixture에서 계산하며 제품 출력을 정답으로 복사하지 않았다.
`product-unittest.stderr`, `independent-cli.events.jsonl`/`independent-cli.json`에 실행 전문·대상 SHA를 보존했다.
parent/child의 py_compile은 sandbox 기본 캐시 쓰기 권한으로 실패했으며 AST로 대체했다.
root는 별도 clone에서 임시 cfile 경로로 tracker·두 시험 모듈을 실제 py_compile했고 rc0이었다.
이를 모델이 원래 컴파일까지 성공한 것으로 바꾸지 않는다.

plan의 낡은 현재 요약은 새 세션에 이미 끝난 T01을 다시 시키거나 완료 근거를 잃게 할 수 있다.
spec/intent 계약은 일치하지만 plan의 현재 완료 범위는 색인·commit·시험 결과와 어긋난다.
원 제출판은 수정하지 않았다. 현행 feedback은 후속 근거와 인계에서 실제 판·완료/미검증/다음 일을
갱신하라고 이미 안내한다. 이번 parent가 feedback 본문을 별도 read/skill로 읽었다는 이벤트는
없으므로 자연 사용·전체 feedback 효과를 주장하지 않는다. design-spec는 명시 지정했고 PROCESS는 실제 읽었다.
native verifier는 공통 기준을 갖춘 채 실행됐지만 인계 요약을 놓쳤다. 이 한 사례로 일반 지침의
누락이나 새 강제 훅 필요를 입증하지 못하며, 충분한 안내의 미준수/적용 누락을 우선 구분한다.
최종 source·실험 판정의 독립 재검토는 [활성 검증 기록](../research/openwebagent-template-history/intent-design-alignment/activation-validation.md)에 남긴다.

root는 **이번 개선의 핵심 세 사건은 관측 통과, 실험 전체는 인계 요약 때문에 partial**로 판단한다.
작은 표현 차이에 맞춰 실행·규칙을 늘리지 않으며 3+1 호출 한도에서 종료한다. 최종 요약이 정확히
이어받아졌다고 주장하지 않는다. 0038의 부분 판정과 전체 AC04 유예를 유지한다.

## 판정과 보존

첫 설계는 intent 유지·spec/plan 이유 연결·코드/시험 무변경, 충돌 요청은 편입 전 질문/미결 유지,
명시적 변경은 중복 승인 없이 실제 intent와 하류 문서 개정·동작/회귀·커밋·현재 인계를 확인한다.
root는 기존 시험과 독립 CLI 기대·종료 코드·조회 무변경을 직접 대조한다. 실제 실행/개입/실패는
단계별 PASS/PARTIAL/미관측으로 구분하며 중요한 누락은 보존한다. 작은 표현 차이로 반복하지 않는다.

로컬 원본은 아래 위치에 그대로 남겼다. 보고서는 원문을 대신하지 않는다.

- `request-original.md`, `source.tar`/`source/`, `manifest.json`: 사용자 요청·정확한 설치 source·149개 설치/fixture 지문.
- `turns/*.{prompt.md,response.md,jsonl,meta.json,stderr.txt}`: 실제3회 입력·전체 공개 응답/도구·시간/종료와 실패.
- `exports/*-original-public.json`: parent/child의 전체 공개 메시지·도구 input/output·실제 모델/variant. 숨은 추론/인증은 제외.
- `exports/*-phase02.json`, `*-phase03.json`, `*-final.json`: CLI sanitize의 별도 metadata snapshot. 이 형식이 가린 본문을 원문이라고 부르지 않는다.
- `snapshots/{01-filter-design,02-sort-proposal,03-accept-and-implement}/`: 단계별 문서·diff·마지막 코드/시험 원 제출.
- `source-validation/`: make check·strict·patch·자료·review criteria의 실제 원문·지문. quick_validate는 PyYAML 부재로 실행 불가이며 Ruby parser와 구별한다.
- `final-validation/`: exact clone·5시험·컴파일·독립11관찰·refs/기준판/설치 지문·전체 command stdout/stderr/rc.
- `product-all.bundle`: template/main/작업 branch를 포함한 제품 Git 이력. SHA256 `286f9d9e4520e2de26166dfa0f21b9792d093c22942e1fc2a991939efd21f706`.
- `public-evidence-manifest-final.json`: 공개 보존821파일의 경로·SHA256. manifest SHA256은 `9db977039232ad2b5d3ea6c34eba9c943e939ffec1a8609e1fbeedaf432ac1d6`이며 runtime 인증·cache/state는 대상에서 제외한다. 앞선819파일의 `public-evidence-manifest.json`도 덮어쓰지 않고 포함했다.

설치 준비 중 Python의 tar `filter` 미지원은 수동 경로/형식 대조 후 복구했다. model 호출 전 실패다.
두 session export를 동시에 실행한 첫 parent export는 `database is locked`였고 동일 세션의 순차 export로
복구했다. 추가 모델 실행/제품 수정은 없었다. 각 최초 오류와 복구는 setup 원본에 함께 남겼다.

제품은 `.local/experiments/workspaces/0039-intent-design-alignment-muse/product/`, 원문은
`.local/experiments/private/0039-intent-design-alignment-muse/`에 둔다. 입력·프롬프트·공개 응답/도구·
모델/세션·시간·단계별 파일/dirty diff·source/설치 해시·독립 실행 전문·Git refs/bundle을 보존한다.
인증 값과 숨은 추론은 공개 원본 대상에서 제외한다. 설치 확인을 실제 읽기/사용 증거로 대체하지 않는다.
한 합성 사례는 새 세션 인계·모든 추천 전제 반증·큰 설계 누적·다른 도구 행동·개별 인과 효과를 입증하지 않는다.
