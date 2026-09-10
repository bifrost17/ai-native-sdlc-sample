# 팀 스킬 설치와 사용

이 폴더는 우리 팀의 선택 가능한 기본 스킬 예시를 Claude Code 플러그인으로 배포한다.
사용 템플릿에 내장되는 필수 스킬이 아니다. 팀이 채택한 스킬과 프로젝트 정책을 함께 사용한다.

## 설치·갱신

이 저장소를 받은 뒤 루트 디렉터리에서 실행한다. Claude Code 로그인이 필요하다.

```bash
claude plugin validate --strict ./org-skills
claude plugin marketplace add . --scope user
claude plugin install intent-sdlc-skills@intent-sdlc-skills --scope user
```

이미 이 마켓플레이스와 플러그인을 설치했다면 소스를 갱신한 뒤 다음을 실행한다.

```bash
claude plugin marketplace update intent-sdlc-skills
claude plugin update intent-sdlc-skills@intent-sdlc-skills --scope user
claude plugin list --json
```

새 Claude Code 세션을 열어 새 판을 사용한다. 설치 판과 실제 로드 경로를 함께 확인한다.
로컬 마켓플레이스에서는 세션이 소스 경로를 사용할 수도 있어 캐시 메타데이터만으로 독립된
복사본을 읽었다고 판단하지 않는다. 소스 폴더 수정만으로 기존 세션이 갱신됐다고 쓰지 않는다.
플러그인 배포/갱신은 [공식 문서](https://code.claude.com/docs/en/plugin-marketplaces)를 따른다.

## sdlc-feedback

일반 `claude` 세션에서 관련 업무를 요청하면 에이전트가 스킬 설명으로 사용을 판단한다.
명시적으로 사용하려면 `/intent-sdlc-skills:sdlc-feedback`도 가능하다. 명시 호출과 자연스러운
업무 요청에서의 자동 사용은 실험에서 구분한다.

| 이벤트 | 수행 |
|---|---|
| 요구·설계 변경, 계획 이탈, 새 수락 판 | 필요한 spec/plan과 하위 참조를 갱신 |
| 관련 커밋 준비 | 실제 포함 파일을 확인하고 바뀐 계획과 구현을 함께 기록 |
| 구현 완료 보고 전 | 새 문맥의 검증자로 현재 결과를 확인하고 중요한 발견을 보완 |
| PR의 변경 검토 | 제출 diff와 spec/plan 대조; 댓글·CI·push는 기존 PR 도구가 담당 |
| 현황·질문·단순 산문 정정 | 불필요한 문서 변경·독립 구현 검토를 하지 않음 |

원본은 [SKILL.md](skills/sdlc-feedback/SKILL.md), 공통 판단 기준은
[sdlc-verifier.md의 Review criteria](agents/sdlc-verifier.md#review-criteria)다.
[sdlc-verifier](agents/sdlc-verifier.md)는 동등한 프로젝트 검증자가 없을 때 쓸 기본 예시다.
업무 대화는 주 세션에 유지하고 필요한 합의·수락·기준·증거를 검증자에게 전달한다.
기본 검증자는 자신의 정의에 공통 판단 기준을 함께 받는다. 별도 기준 파일을 찾거나 그 경로를
전달할 필요가 없다. 다른 프로젝트 검증자를 쓰면 동등한 기준을 확인·인계한다.

일반적인 작은 구현은 Sonnet과 적정 추론을 사용한다. 기본 검증자는 여러 문서의 중요한 합의를
대조하므로 Opus/high로 설정했다. 팀은 난도·영향·불확실성과 사용자 한도에 맞게 조정한다.
더 강한 모델이 모든 오류를 없애지는 않으며, 검증자에게 Bash가 있다는 것은 셸 전체가 읽기
전용이라는 뜻이 아니다. 프로젝트 권한과 보고 전용 지침을 함께 적용한다.

스킬은 에이전트가 사용을 판단하는 지침이다. 매 응답 실행이나 강제 승인 장치가 아니다.
0018의 [sdlc-claude](../team-harness/README.md)는 별도 실행·기록 실험 도구로 남으며 일반 스킬
경로에서 호출하지 않는다. 그 CLI 전용 프롬프트는 0018 실험판으로 유지하고 새 스킬의 기준은
위 공통 파일에서 관리한다. 설치와 호출의 실제 근거는 [0019 기록](../docs/experiments/0019-event-review-skill.md)에 둔다.
