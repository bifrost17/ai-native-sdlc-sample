# 0034 — 문서 표현과 후속 근거 인계

2026-09-13. **문서 부분 검증 통과.** 한 회의 문서 보완·피드백·새 독자 인계로 핵심 조건을 충족했다.
추가 재실험 없이 종료했다. PR3의 제품 수락·통합과 D7·최종 인도는 여전히 미완료다.

[북극성](../verification/north-star-playbook.html)의 설계 이해·대화 없는 인계·실제 피드백에 따른 문서 갱신을
기준으로 [승인된 계획](designs/0034-document-handoff/plan.md)을 실행한다. 핵심 설계는 충분하다는
[0033 문서 검토](reviews/0033-document-quality/README.md)를 바탕으로 안내·표현만 보완한다.
0033의 잔여 제품 구현·D7·최종 인도는 이번 범위 밖이다.

## 제작용 보완

- 두 판의 작성 안내에서 기존 M01 컴포넌트·배포·경합 시퀀스와 W01 사용자 흐름을 직접 연결했다.
  계약이 문장으로 충분해도 여러 경계와 흐름 이해에 도움이 되면 도식을 선택할 수 있게 했다.
  작은 F01의 문장·표 설명과 도식 선택성은 유지한다.
- 두 판의 기존 `sdlc-feedback`에 후속 시험·검토 근거를 받는 이벤트를 연결했다. 남은 작업이 바뀌면
  현재 plan·인계에서 실제 시험 판과 기존 근거를 연결하며, 과거 기록·작성 주체를 보존한다.
  시험 통과와 수락·통합·전체 완료를 구별한다.
- 기본형 **0.1.9**, 선택형 **0.1.5**로 manifest·루트/판별 카탈로그·설치 안내·OpenCode 색인을 맞췄다.
  기존 루트 카탈로그의 선택형0.1.2 표기도 정정했다. 역사적 버전과 과거 실패는 유지한다.
- 제품 양식·정책·검증 전략·verifier 기준은 변경하지 않았다. 선택 Codex와 두 OpenCode feedback patch는
  추가 문단 때문에 이동한 hunk 시작행만 맞췄다. 새로운 검사기·상태 장부·승인 단계는 없다.

제작 후보는 `f89def09c2a00514b31a09b8888e74c3d95e41d7`이다.
[Astra/high 의미 리뷰](designs/0034-document-handoff/review-astra.md)와
[Sol/medium 배포 리뷰](designs/0034-document-handoff/review-sol.md)를 받았다.
배포 리뷰에서 찾은 낡은 색인과 patch backup 생성은 고친 뒤 새 설치본에서 재확인했다.

## 실제 부분 실험

실행기는 **Codex CLI 0.153.4**다. 문서 작성은 **gpt-6-astra/medium**, 새 독자는 **gpt-5.6-sol/high**다.
두 작성 턴과 새 독자의 실제 managed turn_context에서도 모델·추론·권한을 확인했다.
OpenCode와 Claude는 이번 실제 에이전트 실험 대상이 아니다. 해당 배포 경로는 정적으로 확인했다.

root는 HUMAN 제품 오너·엔지니어 역할로 기존 설계를 유지한 인계용 정리를 요청하고 제출을 읽었다.
design-spec·plan·sdlc-feedback은 명시 사용했다. 스킬 자연 선택의 증거로 세지 않는다.
첫 제출 뒤 실제 diff·경계 시험 결과와 E18의 후속 근거를 전달하는 두 번째 대화를 진행했다.
문서 작성자는 수신 시점·작성 주체·대상 코드판과 남은 일을 plan·decisions의 현재 요약에 연결했다.
전역 설치·메모리·외부 스킬 카탈로그를 제외하고 프로젝트별16개 스킬을 설치했다.
작성은 workspace-write/never, 독자는 read-only/never다. 제품 코드·새 시험은 작성하지 않았다.

| 판 | 역할 |
|---|---|
| `3ae564a1e6b8d2d4706d74456de731c76b351e68` | 원0033의 미수락 PR3 보존판. 원래 저장소·평가 입력은 유지 |
| `9babd4b` | 별도 `codex/0034-doc-r01`의 선택형0.1.5 프로젝트 설치 |
| `70c407e21bd07397e6074edf2c9ca12e8ca23af1` | 컴포넌트·변경 시퀀스 각1개, URL 예시와 참조 정리 |
| `cf2d72a14d2c8645eba604096d88aa960750b48d` | E18 후속 근거와 현재 잔여 작업을 연결한 문서 인계판 |
| `aeb2d0c3441faec4e756301d0aa32a5b9f676612` | 새 독자용 독립 Git 스냅샷 |

새 독자에게는 위 인계판의 문서·선언 참조와 최초 JSON CLI baseline
`dcc6663a266cda8c342d609a5f715bda84507c5a`만 전달했다. 입력152파일의 출처·해시를 보존했다.
새 request_service 구현·새 제품 시험·작성 대화·평가 정답표·작성 Git 이력은 제공하지 않았다.
이것은 문서 이해 관측이며 별도의 제품 재구현 시험이 아니다.

## 검증 근거

- `make check`: 102 tests, OK (skipped=1), hooks28/28, eval fixtures8/8, managed-settings PASS.
  마지막 소스 검증은38.081초·종료0이다. semantic model eval은 이 명령의 범위가 아니다.
- 두 plugin과 두 판별/루트 marketplace strict 검증5개 통과. 각 판의 OpenCode와 선택형 Codex를
  새 대상에 복사·patch 적용해 reject/backup/fuzz 없이 통과했다.
  [정적 설치 명령·판·해시](designs/0034-document-handoff/static-install.json)를 보존했다.
- 두 feedback 스킬의 기존 quick validator 통과. 초기 환경에 PyYAML이 없어 중단된 뒤 실험용 private venv에
  PyYAML6.0.2를 설치해 확인했다. 사용자 전역 Python 환경은 바꾸지 않았다.
- 실제0034 제품 설치67파일은 검증한 설치본과 해시가 일치한다. 변경된 설치 파일은4개이며 나머지는 동일하다.
- 기존 경계/OFF 시험4개를 메모리와 실제 HTTP에서 실행해1.552초 OK를 확인했다.
  ON `/requests/`는404 route_not_found, `/requests/%20`은400 invalid_input이며 OFF는503 feature_disabled다.
- 코드·시험26개 파일의 기존 manifest 해시, 원본 intent·OpenAPI·execution의 바이트를 대조했다.
  제품 동작은 바뀌지 않았고 로컬 문서 링크 대상은 모두 존재한다.
- Mermaid12.0.0·기존 Playwright/Chrome 렌더 방식을 사용해 두 도식 SVG/PNG를 생성했다.
  구문·레이아웃 경계 검사를 통과했고 HUMAN이 실제 이미지의 글자·화살표·잘림을 확인했다.
  최종 storage 문서와 렌더 입력 해시도 일치한다.

E18의77시험·216관찰은 원0033에서 확보한 같은 코드판의 역사적 근거다. 이번에는 경계4시험을 실행했으며,
새77시험·216관찰 재실행이나 PR3 수락으로 표시하지 않는다.

## 판정과 보존

실제 제품 실험은 **3호출·15분26.609초**다. 07:18:56.626Z부터07:34:23.234Z까지이며,
CLI 실행 시간 합계는11분59.964초다. 준비·제작 리뷰와 사후 기록은 구별했다.
예산30분·6호출을 늘리지 않았고, 모든 호출은 종료0으로 끝났다.

새 독자는 구조, 버전 검사 우선순위, no-op 경합, 커밋 후 응답 손실, 기본 OFF, 두 경계 URL을
문서와 맞게 설명했다. E18을 후속 HUMAN 근거로 귀속하고77시험·216관찰은 이미 확보됐으며
PR3는 미수락이고 전용 경합·잠금·UPDATE 실패/영향 행0·최신 검토가 남았다고 판단했다.
따라서 중요 인계 조건을 충족한다. writer 문서는 당시 개발자의 미수신과 현재 수신을 명시적으로 구별한다.
독자가 그 문장을 축자로 반복하지 않은 것은 재실험 사유로 삼지 않았다.

독자는 새 구현·과거 Git 객체가 스냅샷에 없어 실행 이력을 직접 확인할 수 없다고 지적했다.
이는 의도적으로 제한한 읽기 입력의 조건이며 실제 제품 유실이나 템플릿 결함이 아니다.
실제 제품 브랜치에는26파일과 원0033 이력이 있으며, 독자도 보존판 복원과 새 구현의 증거를 구별했다.
과거 draft/대기 표현은 현재 요약과 결정 기록으로 해석해 계약 충돌로 세지 않았다.

원본 입력, 설치 해시, 두 프롬프트·응답, 새 독자 입력·응답, 공개 도구 기록, 실제 실행 결과,
평가 정답표와 HUMAN 판정, 두 도식과 복원 가능한 Git bundle을
[0034 증거 저장소](/Users/jake/Projects/ai-native-sdlc-experiment-records/0034-document-handoff/README.md)에 보존한다.
private reasoning과 managed 원본은 복사하지 않는다. 제작용 계획·리뷰는 위 링크로 이 저장소에서도 읽을 수 있다.
증거 저장소 커밋은 `36c422f94a59aae1138fa6c8b82fe71060a03efc`이며 manifest에147개 산출물의
크기·SHA-256을 기록했다. 제품·독자 Git bundle 두 개의 완전한 이력을 `git bundle verify`로 확인했다.

- [HUMAN 판정과 독자 지적의 처리](/Users/jake/Projects/ai-native-sdlc-experiment-records/0034-document-handoff/validation/human-verdict.md)
- [새 독자 응답 전문](/Users/jake/Projects/ai-native-sdlc-experiment-records/0034-document-handoff/turns/03.result.md)
- [개정 설계 도식](/Users/jake/Projects/ai-native-sdlc-codex-0034/product-r01/intent/0001-shared-requests/design/storage.md)
- [개정 plan의 현재 인계](/Users/jake/Projects/ai-native-sdlc-codex-0034/product-r01/intent/0001-shared-requests/plan.md:49)

명시 스킬·그림 요청·HUMAN 피드백을 포함한 작은 사례이므로 지침만의 인과 효과·자연 선택·일반 성공률을
주장하지 않는다. 문서만 보고 제품을 재구현한 실험, 전체 SDLC·D7 또는 두 TDD 판의 실제 개발 통과도 아니다.
북극성에는 이 범위만 추가하고 기존 실패·부분 판정을 유지한다. 제작용 변경은 main에 반영하고
실험 제품은 `codex/0034-doc-r01`에 보존한다.
