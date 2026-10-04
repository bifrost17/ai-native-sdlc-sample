# OpenCode 프로젝트별 전달 — tdd-optional

현재 선택판 **intent-sdlc-skills-optional 0.1.10**의 스킬과 native 검증자를 프로젝트 안에 복사한다.
이 폴더의 원본·patch·검증자·색인은 함께 배포한다. 제작 저장소의 Git 이력이나 다른 판을 실행 중
읽을 필요가 없다. 사용자 전역 설정·설치·모델을 자동 변경하지 않는다.

0.1.4의 intent 제약·상위 문서 비교 기준을 검증자에도 동기화했다. 해당 변경의 실제 모델 재실험은
Codex0032이며, 이 OpenCode 전달판은 원본 기준 일치·patch 적용만 정적으로 재확인했다.
0.1.4 OpenCode 실행 검증으로 확대하지 않는다. 0.1.5의 후속 근거 인계 안내도 OpenCode의 실제 행동 통과를 뜻하지 않는다.

0.1.9는 0.1.8의 전달 경로로 개발건 색인·단계 수락·PR/커밋 근거 안내를 제공한다.
원본·patch 확인과 실제 에이전트 행동은 구분하며 설치 확인만으로 이 판의 OpenCode 행동 통과를 주장하지 않는다.
0.1.10은 공통 feedback·작성 예시·검토 기준에서 편입 전 의도·이유·중요 전제 대조와 영향 문서 갱신을 전달한다.
개발건 색인과 PR·커밋 전달 기준은 같은 판의 `project/changes/README.md`와
`project/docs/CHANGE-DELIVERY.md`에 있으며, 이 어댑터는 그 제품 문서를 자동 복사하지 않는다.

선택 [문서 동기화 Git hook](../examples/document-sync-hook/README.md)은 다른 도구와 같은 파일을
별도 채택한다. 스킬 복사로 활성화되지 않고 의미 판단·검토 수행을 인증하지 않는다.
제작 저장소의 [0038](../../../docs/experiments/0038-document-sync-muse.md)은 0.1.9/U7과 Muse Spark/xhigh
한 사례의 계약 문서 갱신·같은 커밋·동작을 확인했으나 최종 plan 요약 누락으로 인계 상태 갱신은 부분이다.
자연 hook 오류 복구·다른 모델·전체 흐름이나
개별 개선 효과를 입증하지 않는다. maker 참고 링크이며 설치 제품의 필수 참조가 아니다.

## 범위와 변환

- `.opencode/skills/`: `brand`, `data-compliance`, `secure-api-review`, `spec-policy-pass`, `tdd`,
  `stop-slop-ko`, `accessibility`, `secrets-scan`, `grilling`, `sdlc-feedback`, `ux-copy`의 11개 폴더.
- `team-resources/skills/`: `to-questionnaire`, `pr-loop`의 2개 폴더. 전자는 명시적 질문지 요청,
  후자는 실제 hosted PR 업무에서 직접 읽는다. 원본 frontmatter를 자동 발견 경로에 두지 않는다.
- `.opencode/agents/sdlc-verifier.md`: 같은 판의 독립 보고 전용 검증자.
- `team-resources/INDEX.md`: 선택할 자료와 경로의 색인.
- 작성 예시는 별도 선택 사항이다. 같은 배포판에서 채택한 제품의 `examples/skills/`를 사용한다.

`SKILL.md`만 떼지 않고 모든 동반 references·plays·templates·CONNECTORS·LICENSE·PROVENANCE를 복사한다.
플랫폼 변환은 `sdlc-feedback`의 검증자 이름/모델 설정 책임, `ux-copy`의 요청 입력/connector 조건,
선택한 작성 예시 3개의 지원되지 않는 `disable-model-invocation` 제거뿐이다.
patch는 각각 복사 대상 디렉터리 기준 `-p1`로 적용한다. Claude용 스킬 원본을 patch하지 않는다.

검증자의 Review criteria는 같은 판 Claude 검증자와 같다. OpenCode frontmatter에는
`mode: subagent`, `steps: 20`, edit/write/task/skill 비활성화를 둔다. `read: allow`나
`bash: allow`로 프로젝트의 비밀 파일·셸 제한을 덮지 않으며 기존 권한을 상속한다.
Bash 사용 가능 여부가 셸 전체의 읽기 전용 집행을 보장하지 않는다. 보고 전용 본문과 프로젝트 권한을
함께 적용한다. 모델/provider/variant는 실제 대상 환경에서 지원되는 식별자로 프로젝트가 정한다.
작업 난도·영향·불확실성과 사용자 한도에 맞추고 설정의 최종값을 확인한다.

## 현재 로컬 배포판 설치

`OC_PACKAGE`는 선택한 배포판의 `org-skills/` 절대 경로다. `OC_TARGET`은 `project/` 내용을
복사해 Git을 초기화한 별도 제품 루트다. 제작 저장소 내부에서 `cd project`만 하는 것은 격리가 아니다.
아래 명령은 깨끗한 대상에서 실행하며 기존 경로가 있으면 중단한다. 기존 설치의 로컬 변경은
먼저 비교·보존하고 필요한 프로젝트 경로만 별도로 갱신한다.

```bash
OC_PACKAGE=/absolute/path/to/tdd-optional/org-skills
OC_TARGET=/absolute/path/to/adopted-product
(
  set -eu
  test -f "$OC_PACKAGE/.claude-plugin/plugin.json"
  test -d "$OC_TARGET"
  test ! -e "$OC_TARGET/.opencode/skills"
  test ! -e "$OC_TARGET/.opencode/agents/sdlc-verifier.md"
  test ! -e "$OC_TARGET/team-resources"
  mkdir -p "$OC_TARGET/.opencode/skills" "$OC_TARGET/.opencode/agents" "$OC_TARGET/team-resources/skills"
  for skill in brand data-compliance secure-api-review spec-policy-pass tdd stop-slop-ko accessibility secrets-scan grilling sdlc-feedback ux-copy; do
    cp -R "$OC_PACKAGE/skills/$skill" "$OC_TARGET/.opencode/skills/$skill"
  done
  for skill in to-questionnaire pr-loop; do
    cp -R "$OC_PACKAGE/skills/$skill" "$OC_TARGET/team-resources/skills/$skill"
  done
  cp "$OC_PACKAGE/opencode/agents/sdlc-verifier.md" "$OC_TARGET/.opencode/agents/sdlc-verifier.md"
  cp "$OC_PACKAGE/opencode/team-resources/INDEX.md" "$OC_TARGET/team-resources/INDEX.md"
  patch --batch -d "$OC_TARGET/.opencode/skills/sdlc-feedback" -p1 < "$OC_PACKAGE/opencode/patches/sdlc-feedback.patch"
  patch --batch -d "$OC_TARGET/.opencode/skills/ux-copy" -p1 < "$OC_PACKAGE/opencode/patches/ux-copy.patch"
)
```

같은 판의 작성 예시까지 **명시적으로 채택할 경우에만** 이어서 실행한다. 프로젝트 상대 링크를
유지하기 위해 제품 루트의 `.claude/skills/`를 사용한다. 작성 예시는 기본 설치 항목이 아니다.

```bash
(
  set -eu
  for skill in capture-intent design-spec plan; do
    test -f "$OC_TARGET/examples/skills/$skill/SKILL.md"
    test ! -e "$OC_TARGET/.claude/skills/$skill"
  done
  mkdir -p "$OC_TARGET/.claude/skills"
  for skill in capture-intent design-spec plan; do
    cp -R "$OC_TARGET/examples/skills/$skill" "$OC_TARGET/.claude/skills/$skill"
  done
  patch --batch -d "$OC_TARGET/.claude/skills" -p1 < "$OC_PACKAGE/opencode/patches/authoring-native.patch"
)
```

## 확인·갱신·제거

팀 절차로 sdlc-feedback을 채택했다면 [프로젝트 지침 예시](../examples/sdlc-feedback-adoption.md)의
OpenCode 경로를 사용해 제품 `CLAUDE.md`에 연결한다. 설치 목록과 팀의 채택 결정을 구분하며,
명시적으로 채택하지 않은 절차를 자동으로 프로젝트에 추가하지 않는다.

설치 원본 manifest 판과 소스 Git SHA(있으면), 로컬 수정 여부, 적용 patch를 기록한다.
대상 프로젝트에서 `opencode --version`, `opencode debug skill`,
`opencode debug agent sdlc-verifier`로 발견 경로와 구성 파싱을 확인한다.
이름뿐 아니라 실제 본문과 경로를 확인한다. 11개 native 팀 스킬(작성 예시를 채택하면 14개)을
예상하되 전역/상위 프로젝트/다른 판의 동명 자료가 함께 보이면 현재 프로젝트 범위에서 충돌을
해결한 뒤 사용한다. 전역 파일을 자동 제거하지 않는다.

갱신은 깨끗한 복사본에 먼저 patch dry-run과 실제 적용을 확인하고 설치본의 로컬 변경을 보존한 뒤
소유 경로별로 진행한다. 기존 세션이 새 본문을 자동 로드했다고 가정하지 않는다.
제거는 위에서 설치한 개별 스킬 폴더·검증자·색인만 대상으로 한다. 다른 자료가 들어 있는
`.opencode/`, `.claude/`, `team-resources/` 상위 폴더를 통째로 삭제하지 않는다.

설치·파싱은 자연어 선택, 실제 적용, 검증자 위임·대기, 권한의 런타임 집행을 증명하지 않는다.
작은 실제 작업에서 해당 판의 선택 규칙과 증거를 별도로 관측한다. 이번 분리 자체로 모델을 실행하거나
전역 설정 격리를 검증했다고 기록하지 않는다.

## 과거 실행 근거

이전 고정 소스 `ece15c449452f6a425d049172e0e71aa94ebc180`(팀 0.1.7),
`84a77b3890cfdc97f3c6603f433e1382453ca261`(사용 템플릿),
`fbe019c6282d6bab056e885632891e8ff6266c9d`(어댑터)는 분리 전 역사적 판이다.
[0025 기록](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0025-opencode.md)의 최초 실패·권한 보완과
[0028 기록](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0028-review-tdd.md)의 실행 한계를 보존한다.
위 과거 SHA를 현재 선택형 설치 소스로 사용하거나 그 실행을 새 판의 통과로 승계하지 않는다.
