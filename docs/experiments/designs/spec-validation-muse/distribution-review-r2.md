# 0035 r2 배포·정적 검토 — Sol/medium

2026-09-14. 이 검토자는 변경을 설계하거나 구현하지 않았다. r2 기능 후보는
`976c0c23b499b43bbe1211abf6d229f917e78909`, 마지막 표현 일반화는 `58891ec`이다.

## 판정

현재 배포·정적 범위에 미해결 finding은 없다. 기본형 0.1.10과 선택형 0.1.6의 manifest,
root/edition marketplace, 설치 안내·색인과 Claude/OpenCode/Codex adapter가 일치한다. `976c0c2`의
활성 변경은 9개 파일이며, 보존 계약을 고정 정본에서 다시 쓰게 하지 않되 새 전달·변환 경계와 새 protocol의
지원 동작별 입력·결과·오류를 확인하고, AC가 약속한 독립 장애는 각 failing actor를 따로 추적하며,
근거 부재를 미실행 증명으로 바꾸지 않게 한다.

`58891ec`은 다섯 verifier의 특정 opcode/manifest 예시를 `generated implementation artifacts`로 일반화했다.
다섯 파일에서 같은 의미로 바뀌었고 절차·권한·합격 조건은 추가하지 않았다.

기본형의 자동 재현 RED와 test-first 요구, 선택형의 작업별 검증 전략 선택과 non-TDD 자체를 finding으로
삼지 않는 조건은 유지된다. 양판의 feedback과 verifier는 design-only 이름이나 앞선 design PASS가 실제
구현을 포함한 완료 시점의 fresh implementation-completion review를 대체하지 못한다고 계속 명시한다.

이 판정은 배포·정적 maker 검토에 한정한다. 05의 중요한 실패와 진행 중이던 07을 포함한 모델 응답·평가
근거를 아직 종합하지 않았으므로 행동 전체 통과나 목표 달성을 판정하지 않는다.

## 검증

`976c0c2` 상태에서 `make check`를 한 번 실행해 exit 0을 얻었다. Python test 102개 중 1개 skip,
hook 28/28, eval fixture 8/8, managed settings 검사가 통과했다. 전체 출력은
[make-check-r2.txt](make-check-r2.txt)에 보존했다. `58891ec` 후에는 전체 검사를 반복하지 않고
`claude plugin validate --strict`를 다음 다섯 대상에 실행했으며 모두 exit 0이었다.

- `tdd-first/org-skills`
- `tdd-optional/org-skills`
- `tdd-first`
- `tdd-optional`
- `.`

새 `/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse/validation-install-r2-final`
아래에 README 명령대로 기본형 OpenCode, 선택형 OpenCode, 선택형 Codex 제품을 다시 설치했다. 두 OpenCode
제품은 native skill 11개, 직접 읽는 resource 2개, authoring skill 3개와 모든 reference를 포함한다.
Codex 제품은 팀 skill 13개와 authoring skill 3개, verifier TOML과 `AGENTS.md`를 포함한다.

아홉 patch 적용은 모두 exit 0이었다. fuzz/offset 출력과 `.orig`·`.rej`는 없었다. 설치 소스와 설치본의
소유 파일은 각각 기본형 OpenCode 59개, 선택형 OpenCode 61개, 선택형 Codex 65개를 빠짐없이 해시했다.
OpenCode verifier 본문은 각 판 Claude 본문과 동일하고, Codex 본문은 선택형 Claude 본문에서 프로젝트
진입 목록에 `AGENTS.md`만 추가된다.

실험 고정 제품 `/Users/jake/Projects/ai-native-sdlc-spec-validation-muse-20260914/improved-r2`와
`976c0c2` 재설치본의 소유 payload 61개는 해시가 모두 같았다. `58891ec` 최종 재설치본과는 예상대로
`.opencode/agents/sdlc-verifier.md` 한 파일만 일반화 문구로 다르다. 이는 실행 중 고정 제품을 사후 변경하지
않고 후보 당시 입력을 보존한 결과다.

명령·exit, version map, patch hash, source/installed 파일별 SHA-256과 두 제품 비교는
[static-install-r2.json](static-install-r2.json)에 있다. 후보가 바꾼 9개 파일에서 기존 Git 참조가
제거된 경우는 0개다.

## 한계

공유 runtime DB를 사용하는 root 실험과 충돌하지 않도록 OpenCode CLI, debug, export와 모델 추론은
실행하지 않았다. 전역 설치도 하지 않았다. 파일 설치·patch·hash·manifest validation은 자연 선택,
검증자 위임, 런타임 권한 집행이나 행동 수용을 증명하지 않는다. r2 모델·평가 기록이 닫힌 뒤 05 실패를
그대로 포함해 별도의 독립 closing review가 필요하다.
