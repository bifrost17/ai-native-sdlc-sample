# OpenSpec 자체 적용: 강제 스키마 초기화의 데이터 유실 수정

**분류: 프레임워크 자체 개발(dogfood), 기존 기능의 작은 버그 수정.** OpenSpec은 요구사항과 변경 제안, 설계, 작업 목록을 관리하는 CLI다. 이 사례는 프레임워크 사용법을 설명하는 데모가 아니라 실제 CLI의 `schema init --force` 결함을 고친 변경이다. 사용자가 잘못된 artifact 이름 `task`를 입력하면 오류를 반환하면서도 기존 스키마 디렉터리를 먼저 삭제하는 문제가 있었다. 조사 대상은 이 입력 검증과 파일 변경 순서를 뒤집는 패치이며, 제품 전체의 개발 생산성은 평가하지 않는다.

기준 구현은 [commit 5348da9](https://github.com/Fission-AI/OpenSpec/commit/5348da930c4038ffd5b5a521702b71315dcd0019), 보관 및 현재 명세 반영은 [commit d32d49f](https://github.com/Fission-AI/OpenSpec/commit/d32d49f06698c6ae647dc844ff72c00ac494af42)이다. 전자는 2026-07-27, 후자는 2026-07-28의 기록이다. 현재 README를 수집한 판은 별도로 [sources.json](sources.json)에 기록했다. 최신 소개 문구와 당시 구현을 같은 시점의 증거로 섞지 않는다.

## 채워진 문서에서 구현까지

| 단계 | 실제 산출물 | 확인되는 연결 |
| --- | --- | --- |
| 의도와 범위 | [proposal](artifacts/proposal.md) | 데이터 유실 조건, 영향받는 CLI와 코드·테스트 경로, 의존성 변경 없음 |
| 관찰 가능한 동작 | [변경 명세](artifacts/specs/schema-init-command/spec.md) | 잘못된 ID일 때 기존 내용 보존, Windows 경로, 유효한 입력일 때 정상 교체 |
| 설계 판단 | [design](artifacts/design.md) | 입력 수집·검증·메모리 내 스키마 구성을 먼저 완료하고 파일 삭제를 뒤로 이동 |
| 작업과 검증 계획 | [tasks](artifacts/tasks.md) | 실제 Commander 호출, sentinel 파일, 실패·성공 경로, lint/build와 변경 기록 |
| 구현과 테스트 | [원본 patch](evidence/implementation.patch) | 위 문서들과 `src/commands/schema.ts`, `test/commands/schema.test.ts`가 같은 커밋에 포함 |
| 완료 후 명세 유지 | [archive patch](evidence/archive.patch), [현재 명세](artifacts/canonical-spec-after-archive.md) | 변경 디렉터리 이동과 canonical spec의 요구사항 추가를 함께 확인 |

명세는 단순히 “오류를 고친다”가 아니라 실패 상태에서도 무엇이 보존되어야 하는지 적는다. 설계는 정상 덮어쓰기 동작과 JSON 오류 계약을 유지하고, 검증 이후의 파일시스템 실패까지 트랜잭션으로 처리하는 일은 제외한다. atomic swap을 검토했으나 이번 수정 범위를 넓힌다는 이유로 선택하지 않았다는 설명도 있다. 이 구분 덕분에 검토자는 구현에 없는 원자적 복구까지 요구사항이라고 오해하지 않고, 남은 위험을 별도 작업으로 판단할 수 있다.

작업 목록은 회귀 테스트를 먼저 나열한다. 기존 테스트가 예상 파일을 수동 생성하는 방식이라 명령의 변경 순서를 놓쳤다는 설계 설명에 대응해, 실제 등록된 Commander 명령을 호출하는 보조 함수를 추가한다. 실패 경로에서는 기존 `schema.yaml`과 sentinel 내용을 확인하고, 성공 경로에서는 sentinel 삭제와 생성 파일을 확인한다. 코드 diff에서는 `fs.rmSync()`가 검증 뒤로 이동한 것이 보인다. 다만 하나의 squashed commit에 문서와 코드가 함께 들어 있으므로, 목록 순서가 실제 작성 순서 또는 엄격한 테스트 우선 개발을 입증하지는 않는다.

## 리뷰가 만든 보완과 검증 결과

[PR #1446](https://github.com/Fission-AI/OpenSpec/pull/1446)의 [리뷰 지적](https://github.com/Fission-AI/OpenSpec/pull/1446#discussion_r3652833420)은 성공 응답의 내용뿐 아니라 종료 상태도 확인하라고 요청했다. 후속 [commit dcde974](https://github.com/Fission-AI/OpenSpec/commit/dcde97441df591314eebca65ead2749c4357be4c)의 [보관 patch](evidence/review-amendment.patch)는 `expect(process.exitCode).toBeUndefined()` 한 줄을 추가한다. 코드리뷰 발견이 검증 항목을 실제로 보완한 추적 가능한 사례다. 이 커밋은 테스트 파일만 바꾸므로 요구사항이나 설계가 함께 개정됐다고 주장할 수는 없다. 성공 동작이라는 기존 요구를 더 정밀하게 검증한 것으로 읽는 편이 정확하다.

검증은 체크박스와 실행 기록을 구분했다. 구현 SHA를 가진 [CI run 30300699482](https://github.com/Fission-AI/OpenSpec/actions/runs/30300699482)은 성공이며, [보관한 job metadata](evidence/successful-ci-jobs.json)에서 Linux, macOS, Windows 테스트와 lint/type check의 성공 상태를 확인할 수 있다. 같은 SHA의 다른 CI run은 취소 상태이므로 “모든 실행 성공”이라고 요약하지 않는다. 이 자료는 상류 CI가 보고한 결과이며 이번 조사에서 프로그램을 실행하거나 테스트를 재현한 결과가 아니다. 개별 시나리오마다 실행 로그를 대조한 완전한 추적성 매트릭스도 만들지 않았다.

[PR #1467](https://github.com/Fission-AI/OpenSpec/pull/1467)은 #1446의 완료 변경을 archive로 옮기고 현재 명세에 반영한다고 명시한다. 구현 병합 뒤 별도 PR이 정리를 수행하므로, 코드 병합과 명세 정합성 회복이 서로 다른 완료 조건일 수 있다는 실제 운영 흔적이다. 영구 명세를 누가 갱신하는지 책임을 지정하지 않으면 이 사이가 누락될 수 있다.

## 선택적으로 참고할 점과 한계

팀에는 재현 조건·보존해야 할 계약·제외 범위·성공과 실패 예시를 짧게 남기는 방식을 참고할 만하다. 작업 목록에서 “테스트 추가” 대신 어떤 명령을 호출하고 어떤 상태를 검증할지 적으면 다음 에이전트가 구현 의도를 복원하기 쉽다. 완료 기준에 변경 명세의 현재 명세 반영 여부를 포함하는 것도 유용하다. 반면 작은 버그마다 독립 문서 네 개를 항상 요구할 근거는 이 사례 하나로 충분하지 않다. 우리 팀의 검토 규모에 맞춰 한 문서의 구획으로 합칠 수 있다.

확인 가능한 것은 채워진 문서, 구체적 수정, 리뷰 후 테스트 보완, 상류 CI, 후속 명세 반영의 연결이다. 작성 당시 대화, 최초 요구 승인자, 누가 어느 부분을 생성했는지, 문서가 결함 발견을 앞당겼는지는 확인하지 못했다. 프레임워크 제작자의 숙련된 자체 적용이라는 선택 편향도 있다. 독립 제품의 보편적 성과 증거로 중복 집계하지 않는다.

원본 파일과 patch는 해당 판의 [MIT LICENSE](licenses/LICENSE)를 확인하고 수정 없이 보관했다. GitHub API 자료는 사실 필드만 선별해 JSON으로 다시 직렬화한 `api-metadata`이며 원문 파일로 표시하지 않았다. 리뷰 본문은 별도 이용 허락을 가정하지 않고 링크로 연결한다. 각 자료의 원본 URL, SHA, 조회 시각, 해시와 판 구분은 [출처 색인](sources.json)에 있다.
