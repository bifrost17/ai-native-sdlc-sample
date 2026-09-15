# 선택형 작업 방식 예시

아래 파일은 이 프로젝트가 직접 작성한 절차 예시다. 그대로 사용해야 하는 규칙이나 설치된 기능이 아니다.
팀이 필요한 것만 읽고, 복사·수정·대체하거나 사용하지 않을 수 있다.

| 예시 | 다루는 작업 |
|---|---|
| [의도 기록](skills/capture-intent/SKILL.md) | 제안자의 문제와 기대를 문서로 정리 |
| [요구·설계](skills/design-spec/SKILL.md) | 승인된 의도에서 요구사항, 설계, 정책 우려를 정리 |
| [구현 계획](skills/plan/SKILL.md) | 변경 범위, 작업 순서, 위험, 검증 근거를 정리 |

파일은 `examples/`에만 있으며 자동 발견 경로, 플러그인, 에이전트 설정에 등록하지 않았다.
각 예시는 `disable-model-invocation: true`를 사용한다. 팀이 지원하는 도구의 명시적 호출 경로에
별도로 배치하기로 선택한 경우에만 사용하고, 채택할 때 그 도구의 적용·호출 방식을 확인한다.
이 예시를 채택하지 않아도 [개발 절차](../docs/PROCESS.md)와 [문서 양식](../templates/)을 사용할 수 있다.

요구·설계 예시에는 기능·버그·데이터 이행의 합성 완성 문서와 입력이 들어 있다. 필요한 유형만
읽는다. 실제 프로젝트의 승인·구현·검증 결과가 아니며, 예시에 있는 제약이나 기술을 도입할 의무는 없다.

초기 출처는 원 프로젝트 commit `c9e5747d6b044b7f1cecd8ec2166b501467d61c8`의
`.claude/skills/{capture-intent,design-spec,plan}/SKILL.md`다. 해당 파일들은 프로젝트가 작성한
플레이북 작업 절차이며, 여기서는 제작 이력·고정 브랜치·스킬 간 필수 호출을 제거하고 선택형 예시로
다시 편집했다. 외부 채택 스킬은 포함하지 않았다. 출처와 고지는 [NOTICE](../NOTICE)를 따른다.
의도·요구설계 예시는 이후 제작 사슬 0020·0021의 조사·설계 리뷰를 바탕으로 갱신했다.
구현 계획 예시는 제작 사슬 0022에서 네 절의 파일·작업·검증 연결과 필요한 PR/병렬 상세를 보완했다.
작은 기능·결함·두 PR·이행 계획은 합성 작성 예시이며 실제 실행·승인 기록이 아니다.

최신 spec·plan 양식은 [구체적 작성 예시 세트](../docs/sdlc-authoring/README.md)와 함께 읽는다. 기존 skills 내부의 작은 예시는 이전 판의 최소 설명으로 보존한다. design-spec/plan과 references는 최신 양식에 맞춰 갱신했다.

채택 시 `references/`·`examples/`를 포함한 전체 폴더를 복사하고 명시 사용 정책을 유지한다.
배포 저장소의 [Claude Code 설치 안내](https://github.com/bifrost17/ai-native-sdlc-sample/blob/main/tdd-optional/org-skills/claude/README.md)와
[Codex 설치 안내](https://github.com/bifrost17/ai-native-sdlc-sample/blob/main/tdd-optional/org-skills/codex/README.md)에
복사 전 확인·호출명·로컬 변경을 보존하는 갱신 절차가 있다. 오프라인 배포판에서는 같은 판의
`org-skills/claude/README.md` 또는 `org-skills/codex/README.md`를 읽는다.
양식의 안내 링크는 선택 예시 위치를 참조하므로 스킬 설치 없이도 읽을 수 있다.
