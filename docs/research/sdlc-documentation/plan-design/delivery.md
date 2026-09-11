# 사용 템플릿 전달

기준 사용판 `codex/use-template-0021@ca87cdb`에서 별도 `codex/use-template-0022`를 만들었다.
R1은 `95c0933`, 최종 R2는 `82d7ad20128399c51492503db0788167cf774a8c`다.
위치는 `/Users/jake/Projects/ai-native-sdlc-use-0022`이며 기존 사용판과 실험은 바꾸지 않았다.

공통 templates/plan.md와 plan의 examples·references는 제작 파일과 동일하다. 선택형
examples/skills/plan/SKILL.md는 maker의 source quote·fix-mode 환경 설정을 제거하고, 명시적으로
선택하는 예시 설명과 disable-model-invocation: true를 유지했다. examples/README.md의 미재설계
문구를 이번 반영으로 갱신했다. 실제 코드·시험·검토 지침은 채택 프로젝트가 정하는 영역이다.

총 변경 경로는 plan 양식 1개, 선택 스킬 본문 1개, 예시 6개, 상세 참조 1개, 예시 색인 1개다.
기존 intent/spec 양식, PR-SIZE와 GIT-WORKFLOW 정책은 유지한다. 제작 전용 verifier·REVIEW·map
정정은 제작 저장소에만 있으며, 사용판의 기존 REVIEW와 정책은 이미 PR 범위·단계 수락을 구분한다.
새 .claude 자동 발견 경로·hook·검사기·CI·플러그인·research·raw 리뷰 로그는 전달하지 않았다.

핵심 파일 대응과 해시는 [R2 manifest](reviews/candidate-r2.json)에 있다. 입력 예시의 SHA는 제작
입력을 보존한 판이며 채택 제품의 승인 SHA가 아니라는 설명을 context에 붙였다. 사용자는 예시를
선택하지 않아도 기본 양식·정책으로 작업할 수 있다. 별도 영구 설치를 수행한 변경은 아니다.

실제 F02 부분 실험은 R1 사용판에서 시작했다. R2의 사용판 변경은 context 출처 경로·예시 pin
설명만이다. 실행에 쓰인 plan 양식과 선택 skill 본문은 바뀌지 않았다. 제작용 consumer 정정은
실험의 제품 지침을 바꾸지 않으므로 실행 관측을 R2 새 런으로 둔갑시키지 않는다.
