# 활성 자산 변경의 독립 적대적 검토

Status: initial review complete — 소스 검토, 중요 지적 1건, 행동·설치 검증 미실행

검토자는 `/root/alignment_activation_review`다. root가 지정한 정책·스킬 변경만 읽었으며 제품
source를 고치거나 모델 실험·추가 에이전트·외부 앱·커밋을 실행하지 않았다. 아래 최초 검토는
후속 수정 뒤에도 보존한다. root의 처리 결과와 재검토는 마지막 절에 별도로 추가한다.

## 범위와 기준

- 작업트리: `.local/worktrees/intent-design-alignment`, 브랜치 `codex/intent-design-alignment`.
- 지시된 diff 기준: `1d3ffd3`. 검토 중 관측한 HEAD는 `f41128a6d477dea71d5117cc71b07f93c87be0db`다.
  그 위의 미커밋 활성 source 변경을 읽었다. 제작 intent/spec의 중간 커밋과 maker plan의 진행 상태는
  활성 source 결함으로 판정하지 않았다.
- 기대 기준: [정본 설계](README.md)의 편입 전 대조·큰 설계/새 세션·후속 구현 위치.
  북극성의 [intent 절](../../../verification/north-star-playbook.html#intent-md로-포착하기)과
  [요구·설계 절](../../../verification/north-star-playbook.html#요구사항과-design)을 읽었다.
  특히 요청자의 무엇·왜·제약을 보존하는 V2-03/V2-08과 같은 PO가 spec을 아이디어와 대조하는
  본문을 기준으로 삼았다. 팀의 구체 절차가 모두 북극성 원문의 의무라고 해석하지 않았다.
- 활성 검토 대상: 공통 `sdlc-feedback`, `design-spec`과 기존 예시 README, 제품 PROCESS/REVIEW,
  Claude·Codex·OpenCode verifier, 두 feedback patch, 0.1.10 배포·설치 안내 변경.
- 검토 기준은 현재 제품 verifier의 Review criteria를 적용했다. 제작 저장소 REVIEW의 Bugs,
  Security, Compliance 구분을 사용했다. 과거 기억은 조사 순서와 의미 검토의 한계를 찾는 데만
  사용했으며 현재 판단은 작업트리의 실제 내용을 읽어 내렸다.

최초 읽은 주요 source의 SHA-256:

| 파일 | SHA-256 |
|---|---|
| `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md` | `fe5aecf2d7c7b59cfcfc5d690fc4067818727d8157e4a681f5e01c2a7a273ee5` |
| `tdd-optional/project/examples/skills/design-spec/SKILL.md` | `28169a3c0a9f537247da0f406a81aa8faec78537a0507311bfe1a1b4a2f9aa75` |
| `tdd-optional/org-skills/agents/sdlc-verifier.md` | `913e9f589dcecb435c2c509ac3e7e5923c817f73a0b5da38e39708ecda1c2a2f` |

## 최초 중요 지적

### F1 — [P2][Compliance] 작은 선택의 누적 효과를 기존 설계 인계에 연결해야 한다

위치: `tdd-optional/project/examples/skills/design-spec/SKILL.md:91-93`,
`tdd-optional/org-skills/agents/sdlc-verifier.md:83-87` 및 대응 Codex/OpenCode 기준.

정본 `README.md:115`는 작은 선택이 누적되어 대상·성공의 모습·비용을 바꾸는 경우를 기존 설계
묶음 인계에서 대조하도록 정했다. 현재 작성 지침과 검토 항목은 개별 `material choices`에 초점을
두고 작은 변경의 부담을 줄이지만, 이 누적 판단을 명시하지 않았다. 공통 verifier의 기존
`cumulative behavior`는 릴리스 완료를 주장하는 구현 검토에 붙어 있어 설계 인계의 이 분기를
직접 전달하지 않는다.

반례는 각각 작은 내부 선택으로 처리한 옵션·조회 단계·저장 의존성이 쌓여, 전체 사용 흐름이나
운영 비용을 바꾸는 설계다. 개별 선택마다 큰 목적 변경이 없다고 판단했더라도 묶음 전체의 효과는
달라질 수 있다. 전체 정본을 읽으라는 규칙은 있지만 무엇을 합쳐 다시 판단해야 하는지가 빠져,
작은 변경 예외를 적용한 결과를 그대로 설계 인계로 넘길 여지가 남는다.

최소 보완은 기존 handoff 검토 문장에 “개별적으로 작은 선택도 누적 결과가 대상·성공의 모습·비용을
바꾸는지 대조한다”는 뜻을 덧붙이고 세 verifier에 같은 기준을 전달하는 것이다. 각 편집마다 검토나
승인을 추가하거나 누적 장부를 만들 필요는 없다. 공통 feedback의 기존 인계 안내에서 이 기준을
찾을 수 있으면 충분하다. 이 지적은 정본 구현 누락이며 실제 모델이 누적 효과를 놓쳤다는 관측은 아니다.

## 반례 대조 결과

아래는 문면 검토 결과다. 실제 대화 실험의 성공 기록이 아니다.

| 반례 | 현재 source에서 확인한 처리와 한계 |
|---|---|
| 이유가 명확한 작은 spec-only 수정 | feedback 45-50, 57-58, 69행과 design-spec 33행이 문맥·위임 재사용과 intent 유지 경계를 전달한다. |
| 위임된 내부 구현 방법 선택 | 이미 받은 결정으로 진행하며 선택마다 새 승인/모델 검토를 요구하지 않는다. 일반 내부 분해까지 전수 기록할 의무는 추가하지 않았다. |
| 기존 목표/고정 제약과 충돌하는 추가 요구 | 편입 전에 구체 영향과 빠진 결정만 확인하며 독립 작업을 계속할 수 있다. |
| 사용자가 목적과 제약을 명시적으로 변경 | intent의 해당 산문부터 고치고 하류를 맞추며 같은 결정을 재승인받지 않는다. |
| 문제는 같지만 핵심 배경이 잘못 기록됨 | feedback 57-58행과 verifier 107-108행이 정정을 포함한다. 형식적인 intent 수정과 구분한다. |
| 채택된 추천의 중요한 전제가 반증됨 | feedback 47-50행과 design-spec 25-32행이 반증과 영향·미결을 다룬다. 채택을 목표 변경 권한으로 확대하지 않는다. |
| 추천 전제 반증만 전달되고 새 수정 지시는 없는 대화 | design-spec 본문에는 changed premise가 있다. feedback description에는 독립 사건으로 명시하지 않았지만 중요 설계 검토/개정과 evidence 후 계획 갱신 경로가 있다. 실제 자연 선택 여부는 소스만으로 확정할 수 없으므로 실험 확인 항목으로 남긴다. 자동 누락이라고 단정하지 않는다. |
| 같은 판/결정의 문맥을 이미 읽은 세션 | 재사용을 명시하고 판/결정 변경 또는 문맥 상실 때 새로 확인한다. 전체 파일 재독이나 매번 다른 모델을 호출하는 새 의무는 없다. |
| 정책/기술 제약에서 나온 설계 | design-spec 37-38행이 자체 출처와 사용자 목표 영향을 요구한다. 사용자 발언에서 억지로 이유를 만들지 않는다. |
| 작은 선택이 누적되어 전체 비용이 변함 | F1. 기존 설계 인계의 합산 판단을 활성 source에 명시할 필요가 있다. |
| 합의한 계약과 다르게 구현한 결함 | feedback 68-69행, 마지막 Code alone 문장, verifier 105-108행이 계약 변경과 코드 결함을 구분한다. 정해진 계약을 결과에 맞춰 바꿀 권한은 주지 않는다. |
| 새 세션과 여러 설계 정본 | 현재 intent/정본 전체·실제 판·최신 권한과 인계 기록을 읽는 기존 지침을 유지한다. 문맥 없는 이유 발명도 금지한다. |

## 전달판의 같은 기준과 검증 한계

세 verifier의 `Review criteria`를 추출해 비교했다. OpenCode는 Claude와 정확히 같았다.
Codex의 유일한 차이는 프로젝트 `AGENTS.md`를 읽는 항목이며 이번 의미 기준에는 차이가 없다.
feedback patch는 도구별 호출 경로·모델 설정 부분을 바꾸며 새 편입 전 의미 대조를 덮어쓰지 않는다.
실제 patch 적용·설치 후 파일과 runtime의 읽기 여부는 이번 검토에서 실행하지 않았다.

현재 diff에는 새 스킬·훅·의미 검사기·전수 ID·승인 단계·별도 장부가 없다. 작성 예시는 가정과
실제 합성 입력의 경계를 표시한다. 읽은 범위에서 별도 Bugs/Security 중요 지적은 없으며 nit는 0건이다.
새 판단 규칙의 효과, 자연 선택 성공률, 토큰 절감, 새 세션 행동은 미확인이다. 정적 동일성과
설치 안내의 버전 일치만으로 Claude/Codex/OpenCode 행동 통과를 선언할 수 없다.

`make check`, adapter 적용/strict 확인, OpenCode CLI 실험은 실행하지 않았다. root가 수행할 검사와
실험 뒤의 fresh completion verifier가 별도 증거를 판단한다. maker plan과 연구 README의 진행 중
완료 문구 갱신은 root 소유이며 최초 source 검토의 blocker로 보고하지 않는다.

## Root 후속 처리 및 재검토

아직 기록되지 않았다. 최초 지적·반례·관측을 지우지 말고 처리 내용, 실제 수정판, 검증 근거와
수용/보류 이유를 이 절에 추가한다.

### F1 후속 수정 재확인

root는 F1을 수용하고 제품 design-spec/PROCESS/REVIEW를 수정했다고 전달했다. 공통 feedback과
세 verifier는 별도 worker가 수정했다. 검토자는 그 보고 뒤 현재 파일을 다시 읽었다.

재확인 판은 HEAD `d921985cd50f1094d726a468bcee0171313a5b24` 위의 **미커밋 source diff**다.
다음 실제 문구가 기존 설계 인계에서 작은 선택의 누적 효과를 현재 intent와 대조하도록 연결한다.

- 공통 feedback `SKILL.md:29-31`은 대상·성공의 의미·비용에 중요한 변화가 생긴 경우를 다루며,
  매 선택 검토/기록이나 추가 승인 대신 기존 인계 범위를 사용한다.
- design-spec `SKILL.md:39-40`, PROCESS 48행과 REVIEW 14행에 같은 판단을 전달한다.
- Claude verifier 45-47행, Codex verifier 42-44행, OpenCode verifier 49-51행은 기존 설계/계획
  인계에서 이 판단을 사용한다. 구현 릴리스 완료 주장에만 걸려 있던 최초 공백을 해소했다.

이 수정으로 F1의 **활성 source 누락은 해소**됐다. 최초 지적은 위에 그대로 남긴다. 세 도구의
Review criteria를 다시 추출해 비교했으며 OpenCode와 Claude는 정확히 같고 Codex의 차이는
AGENTS.md 읽기 추가뿐이다. 두 feedback patch의 변경도 hunk 위치 갱신이며 이 문장을 제거하지 않는다.

재확인한 SHA-256은 다음과 같다. 최초 hash와 서로 다른 dirty source 판이다.

| 파일 | SHA-256 |
|---|---|
| `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md` | `c339dfea38c67d96b7daeccaac752a08d5e196a29a75477463130d74bd0ac92f` |
| `tdd-optional/project/examples/skills/design-spec/SKILL.md` | `86335526db20cfec04eb965c1551ae5602446b0168f4689878bbd5dd55b8b628` |
| `tdd-optional/org-skills/agents/sdlc-verifier.md` | `ba09f044a02ad535ad686cdcc405e395b1f0d42fd6d70025bc77c6d9da983547` |

재확인 범위에서 남은 중요 source 지적은 0건이다. 실행한 검사는 파일/diff 읽기, hash 산출,
verifier 기준의 텍스트 비교다. 효과 실험·실제 설치·patch 적용·모델의 자연 선택은 여전히 이
검토의 관측이 아니다. 이 결론은 fresh completion verifier의 실행 증거 검토를 대신하지 않는다.
