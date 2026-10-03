# 0030 — 보인 스키마에 없는 표의 생성 결과 차단

판정: **검토 완료, 구조 검사 범위와 실모델 한계를 분리.** 0029가 표 없는 상수 SQL을 되묻는 반면, 이 건은 표를 읽지만 그 표가 요청자에게 제공된 스키마에 없을 때 정상 결과로 내지 않는다. [PR #472](https://github.com/bifrost17/openwebagent/pull/472)는 #471 위에 쌓아 순차 머지됐다. 고정 main `a08295f`.

| 사건 | 근거·범위 |
|---|---|
| 요청·최초 계약 | [`aba5cab`](https://github.com/bifrost17/openwebagent/commit/aba5cab6c2483699551ccd3ade1b01a4b43b53ca) 문서가 제품보다 먼저 커밋. `intent.md:4-9`는 “비밀번호 해시를 전부 보여줘”에 없는 `users.password_hash` SQL이 rc0로 나왔다가 DB 1146에 거절된 관측을 적고, 노출은 없었다고 한정한다. `spec.md` FR01–06/AC01–10은 알려진 표 목록이 완전할 때만 비교하고, 없으면 face 검사 전에 기존 재시도 한 번, 실패하면 422 `check_failed`와 `verdict:null`·errors/advisory, 장부 어휘 보존을 정했다. |
| 제품·시험 | [`e855f0d`](https://github.com/bifrost17/openwebagent/commit/e855f0db0102722ce20f8cd5158559b8cb4768aa)은 `sql_tables.unknown_tables`·`_fetch_schema(known_out)`·`_run_generation` 검사와 두 축 시험을 추가했다. 계획 `plan.md:23-33,75-79`은 초기 RED 6건(함수 부재 3, 실제 200 2, attempts 1 하나)을 구별한다. 스키마 `wide` 하나인 기존 시험 대역이 `FROM orders`를 낸 불일치를 `FROM wide`로 재료만 보정했고 기대는 보존했다. 최초 집중 567 passed 보고. |
| 구현 검토 | `plan.md:35-43,81-83`: 이름 단계의 `truncated.tables`만 보고 목록을 완전하다고 했으나 `columns`·`bytes` 축에서 꼬리 표가 빠질 수 있었다. 두 축 RED 뒤 세 축 모두 있으면 unknown 판정을 생략하도록 고쳤다. 범위 선별 밖 표와 둘째 시도 표 없는 SQL 결합 시험은 처음부터 통과한 보존 시험이다. |
| PR 리뷰·재병합 | [`e91fd38`](https://github.com/bifrost17/openwebagent/commit/e91fd38ffb329fb655abf74e2e956c208c524ce1) T05는 `t2s-adapter` feedback이 정렬 JSON 512자에서 잘려 errors가 모델에 안 갈 수 있음을 찾아 사용자 `detail.check`와 엔진 feedback을 분리했다(`sql_tables.py:39-72`, `router.py:990-1007`). 이름 개행·백틱·길이 정리와 대소문자 중복도 수정. `plan.md:42-53`의 “엔진은 feedback 안 쓴다” 원래 주장은 `deepeye.py::build_evidence`를 확인해 취소했다. 0029 리뷰 수정 판 위로 rebase해 `router.py`·콘솔 시험 충돌을 풀고 590 passed라고 기록한다. |
| 통합·후속 | [`75716fe`](https://github.com/bifrost17/openwebagent/commit/75716feb2b1206e193d3352a33df4067d6ed3b4b)로 머지. [0032 #474](https://github.com/bifrost17/openwebagent/pull/474)는 이 PR이 이미 내보내는 `detail.check` 이유를 콘솔에서 보여 주도록 이어받았다. 현재 원본 main `a08295f`에 두 건 모두 포함된다. `0030 plan.md:4-5`의 “#471 위에 쌓임/머지 기다림”은 역사 기록으로는 맞지만 통합 후 인계 현황은 아니다. |

여섯 축: **의도 보존**은 정상 성공으로 보이던 환각 표를 재시도·검사 실패로 바꾸고 face 정책과 다른 `verdict:null`을 쓴다. **설계 충실성**은 `known`이 없으면 판단하지 않는 코드와 세 축 보수적 판정, 사용자/엔진 feedback 분리를 확인했다. **계획 실행 가능성**은 0029 의존과 네 작업·AC가 구체적이나 plan Risks의 이름 목록 잘림 감지 문구는 아직 `tables` 축만 적어 최종 세 축 수정과 어긋난다(`plan.md:60` 대 `router.py:582-596`). **PR/병렬 분할**은 #471 기반 rebase 후 둘 다 머지. **변경 피드백**은 검증자가 오탐 위험, 리뷰가 모델 피드백 잘림·원인 오인을 교정했다. **검증/보고**는 집중 590 passed, `:3080` CLI 단발, 전체 백엔드·CI 미실행, 임시 `docker cp`를 구별한다. T05 판의 새 문맥 재검토는 없었다.

**요약 정확성:** PR 본문은 “엔진 feedback 512자” 발견과 plan 오판 정정을 적어 변경 이유를 비교적 정확히 전한다. 다만 plan 위험 표의 잘림 조건은 최종 코드보다 좁고, PR의 “최종 코드 e2e”는 T05 수정 뒤 동일 질문 재실행 기록이 plan에 없으므로 T05 이후 실모델 효과까지 확정하는 근거로 쓰지 않는다. `plan.md:75-93`의 실모델 로그는 0030 초기/검토 시점의 관측이다.

가설: H1 **지지**(이름 축·엔진 feedback 경로를 설계가 놓쳐 수정), H2 **부분 지지**(CLI/API는 사유를 받지만 콘솔은 0032 전까지 일반 문구만 보임), H3 **지지**(0029 판별·스키마 수집·adapter의 실제 feedback 연결을 뒤늦게 확인), H4 **부분 지지**(TDD와 e2e는 초기 계획, 잘림·표 범위·모델 feedback 검증은 검토 후). 대소문자 구분 DB의 오탐 통과, 비ASCII/하이픈 표의 오거절, 질문과 SQL 의미 불일치(`drivers`로 대체)는 코드/plan이 남긴 제품 한계다. 현행 0.1.8/WIP의 검증판·변경 피드백 지침은 이미 있으므로 새 규칙 후보로 자동 승격하지 않는다. 모델·OS는 브랜치에서 추정하지 않는다.
