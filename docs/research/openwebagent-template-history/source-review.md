# 0.1.9 source 구현 검토

## 범위

검토 대상은 `ad98adec5c85ebb969fa394796d388df10303a1f..ec476959ca20c2e44fd9d2cbfcbb5b0c7eeffc23`의 0028 source 구현이다.

- SP05 / T03b: 개발건 색인, 과거 spec의 현재 정본 오인 방지, PR·커밋 전달 정책
- SP06 / T03c: 중요한 AC의 검증 경계, 실제 UI·앱 셸 탐색, 위험한 실제 연결의 조기 인도
- 기존 WIP5: 5개 파일, 32 additions / 3 deletions
- 패키지 판: `intent-sdlc-skills-optional` 0.1.9
- 후속 수정: `74e1148ece6e38c929b6aa7e98208d8fbf3f477c`

현재 사용자 범위는 조사와 보완안이다. 개발 실험은 중단됐으며 이 검토는 실험 재개, 구현 추가, 배포 또는 설치를 포함하지 않는다.

## 결론과 발견

`ec47695`의 source 의미는 0028 spec·plan과 대체로 일치한다.

- C1은 `templates/spec.md`와 `design-spec/references/design-depth.md`에서 독립 기대, 실제 경계, 입력·환경, 실패 유도와 관측, 가상화 한계를 plan에 넘기도록 구현됐다.
- C2는 `design-depth.md`와 `disposable-ui-exploration.md`에서 정적 배치 탐색과 실제 컴포넌트·앱 셸 탐색을 질문에 따라 선택하도록 구현됐다.
- C3는 `plan/references/execution-depth.md`에서 가장 위험한 실제 연결을 통과하는 작은 사용자 경로를 일찍 배치하고, 연결을 늦출 때 가상 경계·실제 연결 시점·남은 위험을 밝히도록 구현됐다.
- SP05는 `changes/README.md`, `docs/CHANGE-DELIVERY.md`, 기본 PR 양식, Git 정책과 작성·feedback 지침에 연결됐다. 기존 채택 제품의 `intent/` 경로와 maker 이력은 자동 이동하지 않는다.
- Codex와 OpenCode patch를 적용한 뒤에도 새 `sdlc-feedback` 의미가 유지됐다. Claude/Codex/OpenCode 안내는 설치·파싱과 실제 모델 행동을 구분한다.
- 초기 WIP5는 `.local/research/openwebagent-template-history/20261003/baseline/candidate-wip/`에 별도 보존됐다. source에는 원래 계획 구체성 의미를 유지하면서 이번 changes·검증·조기 연결 안내가 더해졌다.

최초 검토에서 버전 정합성 누락 한 건을 발견했다. `ec47695`는 manifest와 설치 안내를 0.1.9로 올렸지만 루트 `README.md`와 `docs/decisions/single-template.md`는 현재 패키지를 0.1.8로 안내했다.

`74e1148`에서 이를 수정했다.

- `README.md`는 현재 팀 스킬 패키지를 0.1.9로 바꿨다.
- `single-template.md`는 단일 배포 전환 당시 0.1.8과 현재 0.1.9를 구분했다.
- 커밋 parent는 정확히 `ec47695`다.
- README의 기존 별도 WIP는 unstaged 상태로 보존됐고 버전 한 줄만 해당 커밋에 포함됐다.
- 제품 source인 `tdd-optional/`은 이 수정에서 바뀌지 않았다.

이 수정 뒤 남은 material source 불일치는 찾지 못했다. 이는 사람의 수락이나 전체 조사·실험 완료 판정이 아니다.

## 실행한 source 검사

정확한 `ec47695` archive에서 다음을 직접 실행했다.

- `make check`: Python 103 tests 통과, 1 skipped
- hook suite: 28 passed, 0 failed
- eval harness shell suite: 8 passed, 0 failed
- managed-settings 검사: PASS
- Claude strict validation:
  - `tdd-optional/org-skills`
  - `tdd-optional/.claude-plugin/marketplace.json`
  - `.claude-plugin/marketplace.json`
- Codex patch 네 개의 dry-run과 임시 사본 적용:
  - `explicit-only`
  - `sdlc-feedback`
  - `ux-copy`
  - `pr-loop`
- OpenCode patch 세 개의 dry-run과 임시 사본 적용:
  - `sdlc-feedback`
  - `ux-copy`
  - `authoring-native`
- `git diff --check ad98adec..ec47695`

모두 최종 성공했다. 첫 archive 검사 시 `/tmp`에서 Git 명령을 호출해 저장소를 찾지 못했지만 시험 실행 전의 작업 위치 오류였다. 저장소에서 정확한 archive를 다시 만들고 위 결과를 확인했다.

`74e1148`은 두 문서의 버전 표현만 고쳤으므로 source 전체 검사와 adapter 검사를 반복하지 않았다. 두 파일의 commit diff, parent, 현재 dirty 범위와 0.1.9 manifest·설치 안내의 일치만 재확인했다.

## 근거 위치와 보존 한계

작성자가 남긴 지속 가능한 정적 검사 자료는 다음 위치에 있다.

`.local/research/openwebagent-template-history/20261003/baseline/candidate-package-checks/`

여기에는 다음이 있다.

- Claude plugin/marketplace strict 출력
- Codex/OpenCode patch dry-run·apply 출력
- `patch-summary.log`
- 검사 대상 일부와 로그의 `hashes.sha256`
- README link 검사 결과
- 검사 범위와 한계를 설명한 `README.md`

독립 검토자가 정확한 `ec47695` archive에서 다시 실행한 `make check`, Claude strict, patch 적용의 전체 출력은 도구 세션에서 확인했으며 저장소의 새 영구 로그로 쓰지 않았다. 당시 임시 트리는 `/tmp/owa-source-review.ELvVFh`, `/tmp/owa-adapter-review.MBQFoN`에 남아 있었지만 `/tmp` 자료이므로 지속 근거로 간주하지 않는다.

현재 작업트리에는 root 문서 WIP와 연구·실험 자료가 staged되지 않은 상태로 남아 있다. `tdd-optional/` source에는 `ec47695` 이후의 미커밋 수정이 없었다. 이 검토는 무관한 WIP를 source commit의 일부로 간주하지 않았다.

## 확인하지 않은 범위

다음은 실행하거나 완료로 판정하지 않았다.

- OpenWebAgent 제품 runtime
- 계획됐던 두 사례의 전후 비교와 다른 도구 전이
- 실제 모델의 자연스러운 스킬 선택과 지침 적용 효과
- GitHub에서 PR 양식이 실제 표시되는지
- 기존 설치의 0.1.9 업그레이드
- 실제 브라우저·서비스 통합
- 전역 설치, 원제품 변경, 배포
- 모든 역사 사례의 원시 코드·실행 로그 전면 재감사

개발 실험은 사용자 범위 변경으로 중단됐다. 따라서 source의 적용 효과, 인접 회귀, 도구 일반성은 미입증으로 유지한다.
