# examples — 팀 채택과 프로젝트 적용 예시

[sdlc-feedback 채택 안내](sdlc-feedback-adoption.md)는 팀이 선택한 절차를 제품 `CLAUDE.md`에
연결하는 짧은 예시다. 아래 청구 도메인 예시는 팀 정책의 프로젝트 적용 모습을 보여준다.

여기 있는 것은 **팀 스킬이 아니다.** 플러그인은 `org-skills/skills/` 만 로드하므로 이 폴더의 스킬은 세션에 뜨지 않는다.

`claims-status/` 는 플레이북의 worked example(청구 상태 조회 서비스)을 한 프로젝트로 보고 동봉한 [PROJECT-POLICY.md](claims-status/PROJECT-POLICY.md)의 슬롯을 채웠을 때 스킬이 어떤 모습이 되는지 보여 준다 — 팀 조항은 그대로 인용하고, 프로젝트 값(상태 어휘 다섯 · 역할 셋 · 상류 예산 · 보존 기간)은 그 프로젝트가 정한 것으로 적혀 있다.

채택하는 팀은 이 폴더를 **읽고 버린다.** 자기 프로젝트의 `PROJECT-POLICY.md` 를 채우고, 필요하면 같은 꼴로 자기 스킬을 `skills/` 에 둔다.

조사·판정은 [제작 저장소의 보존 기록](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/research/)이며 실행 의존성이 아니다.

이 예시 본문에서 `policies/*.md`라 부르는 것은 당시 청구 도메인 정책의 역사적 출처다.
필요한 조항은 각 예시에 전사되어 있으며 현재 제품의 정책을 대신하지 않는다. 실행 채택 시에는
제품의 실제 PROJECT-POLICY와 정책 정본으로 바꾼다. 다른 저장소의 정책 파일을 필수로 읽지 않는다.
