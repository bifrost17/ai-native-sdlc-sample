# 실제 적용 사례

빈 양식과 실제 사용을 구분하기 위해 공개 저장소의 채워진 문서부터 구현 commit, 테스트 변경, PR, 명세 반영까지 연결했다. 독립 제품 1개와 프레임워크 자체 적용 1개를 선정했다. 모두 소스와 공개 기록 조사이며 프로그램 실행이나 SDD 효과 측정은 하지 않았다.

| 사례 | 분류·변경 규모 | 확보한 연결 | 남은 한계 |
| --- | --- | --- | --- |
| [Opentu](opentu/README.md) | 별도 제품, 기존 플레이어의 작은 기능 확장 | proposal/spec/tasks → 같은 commit의 서비스·UI·테스트 → PR 연계 → archive 및 현재 명세 | 작성 순서·기능별 승인·CI 성공 미확인; proposal의 저장 계약이 delta spec에 없음 |
| [OpenSpec](openspec/README.md) | 프레임워크 자체 개발, 데이터 유실 버그 수정 | proposal/spec/design/tasks → 구현 및 실제 명령 회귀 테스트 → 리뷰 후 테스트 보완 → 성공 CI → 별도 archive PR | 효과 측정 아님; 초안 승인 과정 미확인; 리뷰는 테스트 보완이며 설계 개정 증거는 아님 |

각 사례 폴더의 `artifacts/`는 실제 채워진 원문이다. `evidence/`의 patch는 상류 원문이며 JSON은 선별·재직렬화한 API 사실 metadata다. `sources.json`에서 이 구분과 원본 URL, commit SHA, 조회 시각, SHA-256, 이용 조건을 확인한다. 두 저장소 원문은 MIT를 확인하고 저작권 고지를 함께 보관했다. GitHub 리뷰 본문에는 저장소 라이선스를 일괄 적용하지 않고 원문 discussion URL로 연결했다.

## 후보 선별과 보류

2026-09-11 조회에서 다음 후보를 짧게 살펴봤다. 이는 해당 프로젝트의 SDD 운영 여부에 대한 부정적 평가가 아니라, 이번 제한된 증거 사슬 수집에서 선정하지 않은 이유다. 아래 파일 트리는 commit으로 고정된 링크이며 파일을 복사하지 않았다.

| 후보 | 확인한 판과 보류 이유 |
| --- | --- |
| [The Events Calendar](https://github.com/the-events-calendar/the-events-calendar/tree/202912307c0352634065a8cc4b43d7ae8d71b0d6) | WordPress 제품이지만 조회한 트리의 `openspec/`, `specs/`, `.kiro/specs/`에서 채워진 변경 묶음을 찾지 못함. README 검색 일치만으로 채택하지 않음 |
| [Spectra App](https://github.com/kaochenlong/spectra-app/tree/557eadaa532339814bfcd090cad9cb84f24280e3) | 같은 경로 탐색에서 채워진 명세 묶음 미확보. GitHub가 명확한 라이선스를 반환하지 않아 원문 복사도 보류 |
| [BookWorm](https://github.com/foxminchan/BookWorm/tree/2eaabbc1016a2de2a2af0faee61f2741bba3a851) | Spec Kit 설정·템플릿과 constitution은 있지만 이번 경로 검색에서 `specs/`의 feature spec → plan → tasks 묶음 미확보. 설치 흔적을 적용 증거로 승격하지 않음 |
| [agtx](https://github.com/fynnfluegge/agtx/tree/da4244cf6508a490ca7b15dc1ba43b5731d4419b) | Spec Kit 관련 검색 후보지만 `specs/`, `.specify/`, `.kiro/specs/`에 대응하는 채워진 묶음 미확보. 다른 위치의 문서 사용 가능성은 배제하지 않음 |

Spec Kit의 독립 제품 사례나 공식 데모를 수를 맞추려고 추가하지 않았다. 두 선정 사례 모두 OpenSpec 형식이라는 표본 한계가 있으므로, 다른 프레임워크의 실제 사용 양식까지 검증했다는 근거로 확장하지 않는다. 프레임워크별 배포 양식 비교는 [상위 조사 계획](../plan.md)의 별도 레퍼런스 조사와 함께 읽는다.
