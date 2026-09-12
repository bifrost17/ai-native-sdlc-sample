# 영문 커뮤니티: TDD 스킬의 실제 사용과 중단

조회일: 2026-09-12

대상 기간: 2025-02-01~2026-09-12

이번 증분 조사 범위: Reddit `r/codex`의 우선순위 높은 공개 스레드 2개. 최종 보고서의 다른 커뮤니티 사례와 합쳐 3~5개 스레드를 구성하기 위한 작업 노트다.

## 판정 기준

- **프레임워크 설치/호감**만으로 TDD 스킬 채택으로 세지 않았다.
- **TDD 스킬을 쓴다**는 자기보고와, **실제로 실패 테스트를 먼저 실행해 RED를 확인했다**는 실행 묘사를 구분했다.
- Superpowers 전체 워크플로를 시험·삭제한 사례는 TDD 스킬 단독 중단과 구분했다.
- GitHub 별·다운로드 수와 권장 댓글은 사용 증거로 세지 않았다.
- 아래 수는 선별한 질적 사례일 뿐, 커뮤니티 채택률이나 분포 추정치가 아니다.

## 핵심 판독

두 스레드만으로도 네 상태가 함께 보인다. Superpowers에서 RED→구현→GREEN이 지켜진다고 보고하는 지속 사용자가 있고, 반대로 TDD 스킬이 모든 것을 단위 테스트하게 만들어 전체 스킬 묶음을 잠시 끄고 비교하는 사용자도 있다. Superpowers의 brainstorming은 유지하면서 더 가벼운 Matt Pocock TDD 스킬을 쓰는 사용자와, 자체 TDD 스킬에서 “구현 전에 실패 테스트를 실행하고 RED 출력을 보여라”를 강제하는 사용자도 있다. 따라서 질문에 대한 질적 답은 **사용한다. 다만 전체 프레임워크 고정 채택, 경량 스킬로 대체, 자체 guard로 강제, 과잉 테스트 때문에 비활성화가 공존한다**이다.

## 사례 1 — Superpowers 사용 질문: RED 순서 준수 자기보고와 일시 비활성화가 공존

- 스레드: [Superpowers/Planning-focused skills worth using in Codex?](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/)
- 게시: 2026-07-02 02:23:46 UTC, `angry_cactus`, `r/codex`
- 질문 조건: Codex에 계획 중심 스킬이 유용한지 묻는 중립적 질문. 특정 TDD 사용을 전제로 하지 않는다.
- 로컬 선별 사본: [reddit-1ul5hyu-selected.txt](../sources/skills-english/reddit-1ul5hyu-selected.txt)

### `elwutang` — 지속 사용 + 실제 RED 순서 자기보고

- 직접 댓글: [ov1yeqj](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/ov1yeqj/)
- 작성: 2026-07-02 04:10:03 UTC
- 도구/모델 조건: Superpowers; 직장에서는 Claude, 개인적으로 Codex. 정확한 Claude/Codex 모델 버전은 말하지 않았다.
- 채택 상태: **현재 지속 사용**. Claude에서 쓰기 시작해 Codex로 옮겼고, Codex를 Superpowers 없이 써 본 경험은 없다고 한다.
- 실제 행위: Superpowers가 이전 LLM에서는 강제하지 못했던 TDD를 지키게 하며, TDD가 실제 `red - implement - green`이라고 명시했다. 구현 뒤에는 별도로 E2E 테스트도 생성·실행한다고 했다.
- 증거 강도: **강한 자기보고**. 스킬 이름, 두 작업 환경, RED 순서, 사후 E2E를 구체적으로 구분한다.
- 자기보고와 실행 증거 차이: 댓글에 실행 로그·저장소·실패 테스트 출력은 없다. 따라서 RED 실행을 직접 재현한 외부 검증은 아니다.
- 비용/조건: 토큰을 더 태우지만 월 $200 Codex 한도 안에서는 성숙한 프로세스의 비용으로 받아들인다고 했다.

### `soggy_mattress` — TDD 스킬 과잉 때문에 전체 스킬 묶음 비활성화 실험

- 직접 댓글: [ov1xxug](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/ov1xxug/)
- 작성: 2026-07-02 04:06:57 UTC
- 도구/모델 조건: Codex 5.5라고 작성했고, Superpowers가 curated skill로 포함된 뒤 몇 주의 경험을 비교했다. 제품의 정확한 빌드나 설정은 없다.
- 채택 상태: **사용 후 며칠간 일시 비활성화하여 비교 중**. 영구 중단으로 해석하지 않는다.
- 실제 행위/불만: TDD 스킬이 범위가 너무 넓어 Codex가 모든 것을 단위 테스트하고, 단위 테스트 통과만으로 “작동한다”고 판정하게 만든다고 한다. 현재 모든 스킬을 끄고 이전 Codex 느낌이 돌아오는지 시험 중이다.
- 증거 강도: **중간 이상 자기보고**. TDD 스킬의 구체적 실패 양상과 비활성화 실험을 말하지만 RED 여부나 실제 작업 예시는 없다.
- 한계: 같은 시기에 “5.5 nerfed” 이야기가 있었다는 상관관계를 본인도 추측으로 제시한다. 문제를 TDD 스킬에 단정적으로 귀속할 수 없다.

## 사례 2 — Superpowers 비용 질문: 경량 TDD 대체, RED guard, 전체 묶음 삭제

- 스레드: [Superpowers, is it really worth it ?](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/)
- 게시: 2026-05-26 12:54:13 UTC, `Spirited-Car-3560`, `r/codex`
- 작업 조건: 작성자는 계획·리뷰·거버넌스를 포함한 자체 개발 harness를 이미 쓰고 있었고, Superpowers의 runtime planning·agentic development·TDD를 통합 시험했다. 모델은 특정하지 않았다.
- 로컬 선별 사본: [reddit-1to6329-selected.txt](../sources/skills-english/reddit-1to6329-selected.txt)

### `sarcasmguy1` — Superpowers TDD 대신 Matt Pocock 경량 TDD 스킬 사용

- 직접 댓글: [onyry7t](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onyry7t/)
- 작성: 2026-05-26 13:01:49 UTC
- 스킬: [Matt Pocock의 `engineering/tdd` SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- 채택 상태: **현재 사용**. Superpowers의 TDD/agentic 스킬은 필요 없고 더 가벼운 버전을 쓸 수 있다며 “I use Matt Pococks”라고 명시한다.
- 증거 강도: **중간 자기보고**. 별·설치가 아니라 현재 사용 표현이지만, 작업 예시·RED 출력·지속 기간은 없다.
- 한계: 같은 사용자가 Superpowers brainstorming은 유지했다고 말한다. 이는 전체 프레임워크를 완전히 버린 사례가 아니라 컴포넌트를 골라 쓰는 사례다.

### `tonyboi76` — 자체 TDD 스킬에서 RED 출력 gate를 실제 유효 요소로 사용

- 자체 버전 맥락의 부모 댓글: [onz74u1](https://www.reddit.com/r/codex/comments/1to6329/comment/onz74u1/).
  [Aside 본문·댓글 사본](../sources/reddit/R08-superpowers-worth.json)에 부모와 후속 댓글을 함께 보관했다.
- 직접 댓글: [onzk3lr](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onzk3lr/)
- 작성: 2026-05-26 15:18:09 UTC
- 스킬/모델 조건: Claude를 대상으로 한 자체 harness/TDD 스킬 맥락. 정확한 Claude 모델 버전은 없다.
- 채택 상태: **자체 TDD 스킬의 RED gate 사용**.
- 실제 행위: 구현 전에 실패 테스트를 먼저 실행하고 RED 출력을 보여 주도록 강제해야 실제로 유용했다고 한다. 그렇지 않으면 Claude가 구현과 테스트를 같은 turn에 쓰고, 잘못된 것을 시험하면서도 GREEN이라고 부르는 경향을 봤다고 한다. 한 turn이 더 들지만 “no-cheating signal”의 가치가 있다고 평가했다.
- 증거 강도: **강한 자기보고**. 요청만 한 사례와 달리 실패 테스트 실행·출력·구현 전 gate를 구체적으로 설명하고, gate가 없을 때의 관찰도 대비한다.
- 자기보고와 실행 증거 차이: 실제 RED 로그, hook 코드, 저장소 링크는 없다. Superpowers 기본 TDD 스킬을 그대로 쓴 사례도 아니다.

### `Spirited-Car-3560` — Superpowers 전체 시험 후 삭제; TDD 단독은 미래 의도

- 원문 게시 및 후속: [게시물](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/), [삭제 확인 댓글 onzgv1h](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onzgv1h/)
- 작성: 게시물 2026-05-26 12:54:13 UTC; 후속 15:03:23 UTC
- 채택 상태: **Superpowers 전체를 시험 후 되돌리고 삭제**. TDD 스킬은 나중에 자체 harness에 구현할 수도 있다는 의도만 있다.
- 실제 행위/불만: agentic development + TDD + dual reviews가 한 작업에도 많은 반복, 토큰, 시간을 요구했고 단순한 `plan > implementation > external review`보다 품질 개선이 불명확했다고 한다. 후속에서 실제로 되돌리고 삭제했다고 확인한다.
- 증거 강도: **전체 묶음 중단은 강한 자기보고; TDD 스킬 단독 실행은 약함**. TDD가 복합 워크플로의 한 요소로 묶여 있어 RED를 실제 실행했는지는 알 수 없다.
- 판정 주의: “TDD skill을 나중에 구현할 수 있다”는 말은 채택으로 세지 않는다.

## 검색 경로와 선택/제외

사용한 검색식:

- `site:reddit.com/r/codex Superpowers TDD skill use disable uninstall`
- `site:reddit.com/r/ClaudeCode Superpowers "TDD" skill`
- `site:reddit.com/r/ClaudeAI "test-driven-development" skill Claude Code`
- `site:reddit.com "TDD skill" coding agent actual use`
- `site:github.com/obra/superpowers/issues "test-driven-development" disable`
- `site:github.com/obra/superpowers/discussions TDD skill use`
- `site:news.ycombinator.com/item Superpowers TDD skill`

선택 게이트는 (1) 1차 커뮤니티 원문, (2) 기간 충족, (3) 스킬/guard를 특정, (4) 실제 사용·비활성화·중단 상태가 드러남, (5) 요청·권장보다 수행 묘사가 우선이었다.

이번 증분에서 제외하거나 넘긴 후보:

- Reddit `1q85tlf`, `1vvgsia`: 상위 조사자가 원문을 별도로 읽고 있어 중복을 피했다.
- Reddit `1tmkyab`: 중립적 TDD 질문과 유용한 custom hook 사례가 있었으나, 우선 스레드 2개의 직접 스킬 채택/중단 근거로 포화되어 시간 제한에 따라 본 사례표에서 제외했다.
- Reddit `1uno1bs`: TDD를 hook+AI judge로 강제한다는 도구 제작자의 자기보고가 있었으나, 제작자 홍보 이해관계와 실행 로그 부재 때문에 보조 후보로만 남겼다.
- HN `48739459`: Superpowers 6 전체 사용·삭제·선택 사용 경험은 풍부하지만, 직접 RED 실행이 확인된 댓글보다 전체 suite 평가가 중심이라 이번 좁은 증분에서 제외했다.
- 별·다운로드·설치 안내·짧은 “추천한다” 댓글: 실제 TDD 스킬 호출이나 RED 실행을 입증하지 않아 제외했다.

## 접근 한계와 보존

- Reddit 공개 JSON은 웹 연구 도구에서 원문을 읽을 수 있었지만, 같은 URL을 비로그인 `curl`로 받으면 HTTP 403이었다.
- 따라서 서버 응답 전체를 byte-for-byte 저장했다고 주장하지 않는다. 필요한 게시물·댓글 레코드를 공개 JSON에서 옮긴 **선별 reading copy**와 출처 URL, 조회일, SHA-256, byte 수를 `sources/skills-english/manifest.tsv`에 기록했다.
- 공개 handle만 기록했고 계정 프로필·개인정보는 수집하지 않았다.
- 댓글은 이후 수정·삭제될 수 있다. 로컬 사본은 2026-09-12 조회 시점의 연구용 스냅샷이다.
- 주 조사자가 Aside Browser로 두 스레드를 추가 열람했다. [R07](../sources/reddit/R07-superpowers-planning.json)은
  17개 표시 중 15개, [R08](../sources/reddit/R08-superpowers-worth.json)은 27개 표시 중 27개 댓글 객체를 저장했다.
  이 사본은 공개 본문과 로드된 댓글의 DOM 텍스트·HTML 조각이며 서버 전체 JSON과 다르다. R08은 선별 사본에서
  생략한 부모 맥락과 추가 문장을 포함하므로 문맥 대조에 우선 사용한다.
