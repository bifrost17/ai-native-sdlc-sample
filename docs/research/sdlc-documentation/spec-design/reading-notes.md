# spec 설계를 위한 재독과 적용 판단

2026-09-11. root가 작성 전에 다시 읽었다. 이 기록은 새 외부 조사를 완료했다는 주장이 아니다.

| 다시 읽은 자료 | 이번 양식에 반영할 판단 | 가져오지 않을 것 |
|---|---|---|
| [설계 방향](../design-approaches.md), [종합 조사](../report.md), [비교표](../comparison.md), [후보](../candidates.md) | 문서별 역할을 기준으로 완성 예시부터 작성하고 핵심·조건부 상세를 도출 | 기존 목차 보존을 목표로 삼거나 모든 원문의 항목 합치기 |
| 북극성 Lesson 3/4의 원문과 관련 주석 | 요구·설계 한 기록, 실제 정책 적용, 질문 처리, 사람의 우려 해소. 계획은 파일·순서·구체적인 검증 | 주석을 Anthropic 요구로 인용, 정책 우려를 맡길 사람만 적고 미해결로 진행 |
| [Fuchsia 분석](../references/fuchsia/README.md)과 [작성 원문](../references/fuchsia/evidence/rfc-best-practices.md) | 승인 판단에 영향을 주는 상세, 약속/예시·현재/목표 구별, 문서 밖 결정 반영 | 전체 RFC 절과 승인 이후 동결 규칙 |
| [TensorFlow 분석](../references/tensorflow/README.md)과 [양식 원문](../references/tensorflow/templates/rfc-template.md) | 처음부터 끝까지 사용 예시, 선택 이유·영향·필요한 상세 확장 | 모든 플랫폼·성능 절과 비적용 사유 작성 의무 |
| [Spec Kit 분석](../references/github-spec-kit/README.md), 원본 spec/plan | 대표 동작과 수용 기준, 기존 시스템 재사용, 요구와 기술 설계의 역할 대응 | 기술을 배제한 spec 한 파일만 우리 combined spec으로 사용 |
| [Kiro 분석](../references/kiro/README.md) | 현재 결함·기대 동작·보존 동작, 변경 뒤 설계/작업 재검토 | EARS만으로 충분성이 증명된다는 판단 |
| [OpenSpec 분석](../references/openspec/README.md), 원본 spec/design, [실제 수정 설계](../case-studies/openspec/artifacts/design.md) | 변경 계약·선택·위험을 분리해서 읽기, 입력 검증 실패 때 기존 데이터 보존 | delta·sync·archive·CLI 상태 체계 |
| [Opentu 사례](../case-studies/opentu/README.md) | 구현·tasks에만 있는 영속성 요구를 spec에서 놓치지 않도록 대조 | 짧은 문서의 존재를 품질 효과로 해석 |
| [MADR 분석](../references/madr/README.md)과 원본 최소 양식 | 실제 중요한 대안·선택 이유·단점을 Design에 짧게 남김 | 형식적인 세 대안과 별도 ADR 의무 |
| [Google 분석](../references/google-engineering/README.md) | 핵심 판단부터 상세로 읽기, 중요한 우려는 앞에서도 보이게 | Google 공통 공식 양식이라는 이름 |
| [BMAD](../references/bmad/README.md)와 원본 spec, [Superpowers](../references/superpowers/README.md)와 reviewer 원문 | 계약과 배경의 구분, 상세도 조절, 계획을 망칠 중요한 누락 중심 리뷰 | 문서 원장·여러 reviewer·고정 세션 구조의 기본 의무화 |
| [GSD](../references/gsd/README.md), [Spec Kitty](../references/spec-kitty/README.md) | 여러 구현자가 공유할 계약과 의존을 보이게 함 | spec 안에 작업자·worktree·진행 상태를 복제 |

현재 templates/spec.md, design-spec과 plan 스킬, /spec 명령, 선택 팀 정책/피드백 스킬,
F01/B01 입력·HUMAN 답변·실제 baseline 코드를 읽었다. Astra의 별도 설계 도전과 Sol의 소비자
감사도 받았다. 원본의 주된 문제와 현재 코드/도구의 결합을 함께 이해하기 위한 작업이다.

현재 spec의 중요한 부족은 Design의 짧은 안내, 정책/보존 조건에서 나온 요구를 Problem에만
연결하는 표현, R/AC의 반복 유도, intent에서 온 질문만을 위한 제목, 정책 충돌로 좁힌 우려다.
가용 스킬 목록과 provenance는 설계를 위한 수단이므로 본문을 압도하지 않게 배치한다.
승인된 과거 intent가 존재한다는 사실과 지금 읽는 판의 승인을 구별하도록 작성 지침도 맞춘다.

실사용 후보는 제작 원본에서 자동 생성되지 않는다. 기존 사용판은 References applied와 선택형
예시 스킬을 쓰므로 그 차이를 유지한 별도 전달·검토가 필요하다. 원본 수정이나 plugin 설치만으로
실사용 템플릿까지 갱신됐다고 보고하지 않는다.

합성 이행 예시의 기술 설명을 쓰며 SQLite 공식 [transaction](https://www.sqlite.org/lang_transaction.html)과
[atomic commit](https://www.sqlite.org/atomiccommit.html)을 2026-09-11에 추가 확인했다.
동시 reader와 단일 writer, 경합·COMMIT 실패, 명시적인 오류 정리와 영속성 전제를 확인한 것이다.
이는 예시의 도메인 정확도를 위한 확인이며 양식 조사 레퍼런스를 하나 더 채택하거나 실제 이행을
검증한 결과가 아니다. 서비스의 5초 상한과 API 상태 코드는 root가 명시한 합성 입력의 값이다.
