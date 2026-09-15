# 0025 — OpenCode 준비 실험과 전체 개발 실험

2026-09-12. **준비 보완 → 전체 F04 개발 → 최종 인도 → 어댑터 보정 부분 확인까지 완료했다.**
HUMAN(root)은 사람 검토·복구를 포함한 제품 인도를 통과로 판정한다. 협업 과정은 주요 흐름 성공과
최초 실패가 함께 있는 **부분 통과**다. 독립 Astra/high 평가도 이 구분에 동의했다.
설계 정본은 [OpenCode 실험 설계](../research/opencode-compatibility/experiment/README.md)다.

## 실행 방법

먼저 작은 공개 label helper로 스킬 읽기, 제품 질문과 같은 session 재개, 선행 시험/수정,
독립 검증자 전달·대기, 공개 사건 수집을 확인한다. 이것은 부분 준비 실험이다.
F04와 별도의 코드·질문을 쓰며 전체 intent/spec/plan 사슬 생략을 HUMAN이 명시한다.
명시적 tdd/verifier 호출은 기술 경로 검증이며 자연 선택 성공으로 계산하지 않는다.

준비에서 드러난 설치·권한·모드·출력 수집 문제를 수정하고 결과를 남긴 뒤 새 F04 clone/session을 시작한다.
F04는 사용판 d4d2153, 데이터 v6.0.0/seed102, 팀 스킬 원본 0.1.5에 고정한다.
native 14개와 파일 2개를 제공하며 적용할 것은 AGENT가 선택한다.
Codex는 HUMAN, OpenCode는 개발 AGENT다. 고정 대본이나 자동 후속 판단은 없다.
최초 문서 작성/수락 뒤 새 구현 세션, 두 PR의 로컬 통합, 첫 요약 구현 뒤 JSON 요구 추가,
독립 검토·전체 회귀·같은 소스 OFF→ON→OFF와 인도를 관측한다.

## 시작 조건

- 시작: 2026-09-12 01:51:18 UTC. 준비/복구 포함 제안 상한 03:21:18 UTC 또는 HUMAN 16턴.
- OpenCode 1.18.30. 연결된 OpenCode Go를 사용한다. 실제 확인한 모델 목록에서
  `opencode-go/gpt-5.6-luna`가 tool call과 medium/high reasoning을 제공한다.
- 준비 개발 medium, 교차 자료 검토 high. 실제 모델·옵션·결과는 각 turn metadata와 대조한다.
- 개인 영구 설치는 변경하지 않는다. 외부 프로젝트 경로/네트워크와 push/merge는 AGENT에 허용하지 않는다.
  로컬 통합은 HUMAN이 판단해 수행한다. 경로·권한 설정을 OS 격리로 표현하지 않는다.
- 제품 작업 루트: `/Users/jake/Projects/ai-native-sdlc-opencode-20260912/`.
- 진행 중 운영/공개 출력: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0025-opencode/`.
  공개 자료는 마감 때 실험 refs에 보존한다. 비공개 HUMAN 입력은 제품에 넣지 않는다.

[run-opencode.py](../research/opencode-compatibility/experiment/run-opencode.py)는 한 HUMAN 요청을
전달하고 공개 text/tool/result 사건만 보존한다. 다음 응답 선택·검토·수정·채점을 하지 않는다.
reasoning/signature는 쓰기 전 제외한다. 출력 수집 검사는 이 부분을 확인하는 기술 검사다.

## 결과

### 준비 실험과 방법 보완

1. pilot-01은 subprocess cwd만 지정했고 inherited PWD는 maker였다. 실제 도구가 maker를 읽어
   환경 오염으로 판정했다. 중단을 시도할 때는 이미 rc0으로 종료돼 있었다(34.467초).
   원인을 PWD 사용으로 추정하되 내부 구현까지 확인한 것은 아니다. 전달기에 `run --dir` 명시와
   cwd/PWD 일치를 추가하고 새 session에서 재시험했다. rc0만으로 올바른 작업 공간을 판단하지 않는다.
2. 설치 중 ux-copy 초안 patch의 hunk count 오류가 발견됐다. 수정된 patch를 완성된 staging 원본에
   먼저 적용해 검증하고 복사하는 방식으로 보완했다. SKILL과 PROVENANCE를 함께 바꾸는 patch를
   단일 target 파일로 적용하지 않는다. 제작 중인 patch를 동시에 읽었던 준비 문제도 남긴다.
3. pilot-01b는 `ses_f6ca9800fffeEfqaU0HB9HXbaL`에서 실제 native tdd와 올바른 pilot 파일을 읽고
   대소문자 결정을 질문했다(10.947초). pilot-02는 같은 session에서 HUMAN 답을 받고 실제 시험
   1통과/2실패→최소 구현→3통과를 수행했다(91.773초).
4. native task가 `ses_f6ca6bd56ffeODWTH7vgpyPd5f`를 생성해 현재 파일·diff·시험을 확인했고
   부모는 결과를 기다린 뒤 보고했다. 검증자도 과거 test-first 순서는 최종 tree만으로 증명할 수 없다고
   구분했다. HUMAN은 실제 공개 도구 순서와 3시험 재실행을 대조해 이 준비 범위를 통과로 판단했다.
   pilot seed `8c31f97`, HUMAN 수락·보존 커밋 `93852aa`. 모델은 실제 task metadata의 Luna와 일치한다.
5. 큰 session export를 PIPE로 받으면 UTF-8 byte65535에서 잘리는 문제가 재발했다. 원문을 디스크에
   쓰지 않고 PTY에서 메모리로 받아 reasoning/signature를 제거한 공개 JSON만 저장했다.
   child 174290 bytes·parent 117815 bytes를 완전한 JSON으로 받았다. API/프롬프트 실패로 분류하지 않는다.

이 과정은 명시 호출·부분 작업이므로 자연 스킬 선택이나 전체 사슬 통과로 계산하지 않는다.
준비 결과와 수집 오류를 보존하고 F04는 별도 깨끗한 clone·새 session에서 시작한다.
배포 자료는 [org-skills/opencode](../../org-skills/opencode/README.md)에 포함했다.

### F04 작성 단계

제품 seed는 `7f53ac5`, S1은 `ses_f6ca0eb0bfferRB1Oj5bOrjOt9`다.
실제 공개 사실만으로 질문하고 HUMAN이 D1–D6을 답했다. intent `f714c73`, spec `246c85a`를
HUMAN이 읽고 수락했으며, 설정/오류 제안 수락을 `e1a9ae6`에 보존했다.
합의는 `TRACKER_REQUEST_VIEWS=on`만 ON, 나머지 OFF, 거부 rc3와 영어 stderr 한 줄,
기존 명령 유지, 조회 바이트 불변, 두 기능 공동 공개다. 첫 complete 저장의 기존 직렬화는 허용한다.

S1 첫 질문은 capture-intent/brand 파일을 직접 읽었다. intent 작성 때 capture-intent/stop-slop-ko,
spec 작성 때 design-spec/data-compliance/spec-policy-pass/brand를 실제 native skill로 읽었다.
파일 Read·native 호출·산출물 적용을 구별한다. 설계에서 관련 정책을 구체 계약에 적용했고,
해당 없는 API/UI 스킬을 사용하지 않은 것은 결함이 아니다.

작성 당시 독립 실험 설계 검토(Astra/high)는 진행 차단 사유가 없다고 판단했다. 별도 S2,
요구 변경 전후 판·동일 커밋·최신 통합·실제 검증자 완료 근거를 최종 판정에서 확인하도록 했다.
작성 단계만으로 전체 개발·자발적 후속 문서 동기화 통과를 주장하지 않는다.

계획 `918e306`의 사용 설명 파일 부재 주장과 gate 구현/시험 선후는 HUMAN이 실제 파일과 대조해
수정을 요청했다. `15c4831`이 USAGE 갱신과 선행 gate 시험을 반영해 수락됐다.
새 구현 S2 `ses_f6c94bda8ffeJK9OqprfDYTwXu`에는 S1 대화 없이 문서 경로·수락 SHA·이유와
PR1 범위만 전달했다. 초기 native tdd와 sdlc-feedback 읽기를 관측했다.

HUMAN 관측 도구에도 준비 오류가 있었다. 설정 제안 전 작성한 helper가 ON 값을 `1`로 가정했다.
제품 관측 전에 본문을 검토해 발견했고, 공개 수락한 정확한 `on`으로 정정했다. 원본 helper도 보존한다.
이는 제품 실패나 숨겨진 기대 변경이 아니라 아직 미정이던 실행 설정을 합의 값으로 맞춘 것이다.

### PR1 통합과 PR2 첫 구현

S2는 PR1에서 native tdd/feedback 본문을 읽은 뒤 owner와 OFF gate의 의미 있는 실패를 먼저
실행하고 최소 구현했다. native 검증자가 수락 SHA 연결, 기존 show/complete의 명시적 ON/OFF
시험과 없는 파일의 gate 시험을 발견해 개발자가 보완했다. 제품 `8cd46e4`의 9시험과 HUMAN
14관측 통과 뒤 `bdb89f7`에 PR1을 merge하고 통합 판의 9시험을 다시 실행했다.

두 번째 native 검토가 UX U1의 다음 행동 안내와 수락된 한 줄 오류의 충돌을 발견했다.
초기 설계와 HUMAN 수락에서 놓쳤고, AGENT는 D4에서 기존 수락의 적용이라고 해석했다.
HUMAN은 이를 과거 예외 승인으로 인정하지 않고, M1 메시지에 이 합성 로컬 비활성화 오류만의
제한된 예외를 **그 시점에** 명시했다. PR2에서 D4를 AGENT 해석으로 정정하고 실제 결정 D5를
별도로 남겼다. U1 원문 충족이나 처음부터 정책 일치로 세지 않는다.

S2도 USAGE가 없다는 중간 주장을 반복했지만 실제 Git은 기존 문서 수정이고 내용 손실은 없었다.
이는 파일 존재 판단/보고의 부정확성이다. 새 세션 인계 전체 실패로 확대하지 않는다.

PR2는 최신 M1에서 `codex/oc-f04-a-summary`로 분기했다. 첫 요약·gate 실패→최소 구현→16시험,
native 검토 뒤 `3a3817c`와 사용법 단계 표기 정정 `ec3bd41`을 보존했다. 검증자가 PR2 진행 허용
기록과 untracked 시험을 포함한 staged diff 확인도 보완하게 했다. 두 기능은 아직 일반 OFF다.
HUMAN은 실제 코드·시험과 `3a3817c`의 SHA256, 최종 `ec3bd41`의 clean 상태를 기록한 뒤
02:36:58 UTC 이후 처음 JSON 업무 요구를 전달했다. 이 요청에는 문서·스킬·갱신 방법을 넣지 않았다.

### 요구 변경, 최종 통합과 인도

JSON 요청 뒤 spec/plan/결정 기록을 스스로 수정하고 실제 JSON RED→GREEN을 수행했다.
`53afa7a`에 plan·구현·시험을 함께 커밋한 점은 통과다. 그러나 구현 전에 개정 spec의 수락 판을
고정하지 않았고 plan Upstream에 JSON이 없는 `f245d0c`가 남았다. JSON native 검토 3건도 이를
놓쳤다. HUMAN이 실제 spec `53afa7a`를 나중에 읽고 수락한 뒤 `139ef41`로 참조·수락 시점을 복구했다.
처음부터 이 순서를 지킨 것으로 소급하지 않는다. intent는 기본 세 줄 출력을 명시했으며 새 형식을
금지하지 않았고 목적·제약이 유지됐으므로, 미수정 자체를 중요한 실패로 보지 않았다.

`4dc0d48`에서 설정 제거가 범위 밖임과 초기 계획 서술의 시점을 명확히 했다. 이 산문 정정은
HUMAN이 직접 검토해 native 재호출을 생략했다. 반복된 검토 비용을 줄인 개입으로 기록한다.
최종 제품 main은 merge `2ac54ad49c6b4964504099a636e2d7881213e935`다.

- M2와 새 `handoff/` 디렉터리에서 각각 제품 **20시험 OK/rc0**.
- 새 디렉터리에서 HUMAN의 별도 **24/24 CLI 관측** 통과. 원본·소스 hash 유지.
- 별도 로컬 공개 수락 뒤 같은 소스/데이터의 **OFF→ON→OFF 12/12 호출** 통과.
  기본 목록은 유지되고 owner/text-summary/JSON-summary는 함께 닫히거나 열린다.
- 공개 설정을 유지한다. 실제 회사 승인·운영 배포·live 사용자 공개를 수행한 것으로 쓰지 않는다.

### 마감 환경 감사에서 발견한 권한 결함과 부분 보완

원 F04의 resolved verifier 규칙에는 프로젝트의 git push/merge/curl 등의 deny 뒤에
agent의 넓은 `bash: allow`가 합쳐져 있었다. [공식 권한 문서](https://opencode.ai/docs/permissions/)의
마지막 일치 규칙/agent 우선순위에 따라 세부 제한을 덮는 실제 어댑터 결함이다.
원 F04 검증자 8세션의 셸 입력 128건에서 해당 금지 명령의 명시적 호출은 발견하지 못했고
child change summary는 모두 0이었다. 이는 적대적 우회 시험이나 권한 차단 증명은 아니다.

배포판 `90b1a24`에서 넓은 allow 한 줄을 제거해 프로젝트 셸 규칙을 상속하도록 했다.
F04의 고정 설치를 소급 수정하지 않았다. pilot main `93852aa`에서 별도 파생한 `799d5ab`의
부분 probe는 resolved 규칙에 세부 deny가 남는 것과 실제 native 읽기·3시험·clean 상태·부모 대기를
확인했다(22.276초). 금지 명령의 실제 차단 시도나 수정판 전체 F04 재실행은 수행하지 않았다.
따라서 **수정판 설정 상속과 정상 검증 작업의 부분 확인**이며 원 F04 권한 집행 통과가 아니다.

## 전체 평가 범위

| 플레이북 흐름 | 이번 판단과 근거 |
|---|---|
| 2–3: intent·요구/설계·정책 | 실제 질문·SHA 수락·구체 계약 작성. 계획 초안과 U1은 HUMAN/native 리뷰 후 복구. 무오류 작성 아님 |
| 4: 구체 계획·새 문맥·변경 | S1→S2 문서 인계와 TDD, 두 PR, JSON plan+구현 같은 커밋 통과. 개정 수락 판 연결은 최초 실패·HUMAN 복구 |
| 5–6: 프로젝트 지침·스킬 | 14 native+2 파일 제공. 실제 native 9종과 직접 Read·산출물 적용 확인. 전역 aside/customize가 목록에 보이지만 명시 deny·미사용이며 완전 격리로 표현하지 않음 |
| 7–8: 독립 검토·feedback loop | F04 native 8회 모두 child 현재 자료/시험 확인·반환·부모 대기. 실제 보완과 놓친 수락 판을 함께 기록. 준비/후속 probe의 2회는 별도 명시 호출 |
| 9: 지속 eval | 이번 제품 CI의 지속 eval은 미관측. maker make check를 제품 CI·의미 eval로 세지 않음 |
| 10: 리뷰·통합 | 로컬 PR 범위 2개와 실제 merge·회귀·HUMAN 판단. hosted PR·댓글·외부 CI는 미관측 |
| 11–12: approval/배포 | HUMAN 단계·통합·로컬 공개 판단은 관측. hook 강제·조직 승인·운영 CI/CD는 미관측. verifier 권한 원 결함/보완을 별도 평가 |
| 13: 지표·피드백 | 이번 실행 시간·호출·실패/복구 기록. 장기 지표·운영 feedback 효과는 미관측 |

고정 북극성 원문·역할 소유 원칙·변경 없는 양식의 정보 역할·지표 정의는 정적 근거를 재사용했다.
플랫폼을 바꾼 지침·발견·권한·실제 호출은 새로 관측했다. API/DB/UI/병렬 제품 구현은 이 작은 CLI에
해당 없거나 미관측이다. 교육 예시가 포함된 동일 합성 사례 1회이며 무힌트 실험·일반 성공률이나
Claude/OpenCode의 인과적 성능 비교가 아니다. 파일 조건 B로 전환할 차단은 없었다.

## 자원과 보존

OpenCode 개발 호출 **14회**: 준비 3회(오염 1회 포함), F04 10회, 권한 부분 확인 1회.
CLI 호출 소요 합계 **2,215.549초(약 36분 56초)**는 native 대기 시간을 이미 포함한다.
준비·HUMAN 리뷰·기록 작업을 포함한 wall time과 다르다. 60분 점검에서 제품 인도 검증 완료와
잔여 보존 작업을 기록했으며 90분/16호출 상한을 변경하지 않았다.
개발은 Luna medium, 설계·중요한 변경은 high를 요청했다. 검증자는 실제 modelID Luna,
resolved agent options의 reasoningEffort=high를 확인했다(session variant 표시는 default).

CLI step 보고 비용 합계는 부모 **0.64382609**, 별도 child session 보고 합계는 **0.25166750**이다.
청구 통화/실제 계정 청구는 독립 확인하지 않았으며 부모·자식을 임의 합산하지 않는다.
Codex root·협업 에이전트 비용은 이 값에 포함하지 않는다. 세부 값은 보존한 `raw/run-metrics.json`에 있다.

- 사용판: `codex/use-template-0024-r2@d4d2153`; 제품 seed `7f53ac5`; v6.0.0/seed102.
- 작업 refs: `codex/oc-f04-a-owner@8cd46e4`, `codex/oc-f04-a-summary@4dc0d48`.
- 제품 M1 `bdb89f7`, M2 `2ac54ad`. 제품 이력을 maker main으로 합치지 않는다.
- 준비 기록: `codex/experiment-2026-09-12-oc-pilot-r01@6caba1d`.
- 전체 기록: `codex/experiment-2026-09-12-oc-f04-a-r01@a524d27`.
- 권한 보완 기준: `codex/experiment-2026-09-12-oc-permission-r01@799d5ab`.

전체 기록 worktree는 `/Users/jake/Projects/ai-native-sdlc-exp-0025-record/`다. `EXPERIMENT.md`,
독립 평가, 공개 대화·도구 결과·metadata·hash manifest를 함께 보존한다. HUMAN 입력과 관측기는
실험 종료 후 `human/`에 별도로 보존하며 진행 중 제품/AGENT에는 전달하지 않았다.
스킬 전달·설치·갱신·제거 안내는 [OpenCode 어댑터](../../org-skills/opencode/README.md)에 있다.
새 의미 검사기나 자동 후속 대화기는 추가하지 않았다.

마감 제작판 `make check`는 Python 96시험(기존 skip 1), hook 28/28, eval harness 8/8,
managed-settings 계약을 통과했다. [실행 출력](../research/opencode-compatibility/experiment/final-check.txt)을
보존했다. 로컬 문서 링크, 북극성 179개 항목의 기존 등급·ID 유지, 기록 manifest의 97파일 hash도
확인했다. 이 제작판 검사는 제품 CI나 플레이북 의미 준수의 증거와 구분한다.
