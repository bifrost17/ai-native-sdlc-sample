# 독립 근거 검토 기록

검토일: 2026-09-12. 검토자는 보고서 작성자와 별도 에이전트이며, 이 파일 외의 보고서·원문·Git은 수정하지 않았다.

## 범위와 방법

`README.md`, `methodology.md`, `working/reddit.md`, `working/skills-korean.md`의 결론을 보관된 공개 원문과 대조했다. 아래 7개 주요 사례를 직접 읽었고, `raw_anon_1111` HN API 1건을 보조 대조했다. 초기 표본은 보관본으로 대조했고, 영문 증분 2개 스레드는 공개 JSON을 웹 도구로 다시 열어 확인했다. 작성자 실제 작업을 재현한 검토는 아니다. HTML은 script/style을 제외해 본문을 읽었으며 Reddit은 `post_text`, `body_text`와 `body_html`을 함께 확인했다. 스킬 정의를 사용자에게 실행하지 않았다.

중점은 실사용 자기보고와 설치·권장 구분, 프레임워크와 TDD 하위 스킬 구분, 실제 RED 증거의 부재, 프레임워크 중단의 과잉 일반화, 채택률 추정, 과거 버전 소급, 상반된 경험 누락이다. 효과 실험과 템플릿 정책 검토는 범위 밖이다.

## 원문 대조 7건

| 표본 | 대조 원문 | 확인한 맥락과 판정 |
|---|---|---|
| YUL438 | [R06](../sources/reddit/R06-superpowers-relevant.json), 게시글 본문 | Superpowers를 사용해 왔고 brainstorming·TDD·subagent 관련 스킬을 선호한다는 1인칭 진술이 있다. **TDD 관련 스킬 사용 자기보고**라는 README 판정은 타당하다. 호출 로그·정확한 버전·실패 실행은 별도 증명되지 않는다. |
| artofbullshit | [R06](../sources/reddit/R06-superpowers-relevant.json), `p59gg2p`와 `p5c7kss` | TDD 순서 준수를 신뢰하기 위해 계속 사용한다는 댓글 뒤, Superpowers만 필수라는 뜻이 아니라 모든 스킬 제거가 불안하다는 후속 설명이 있다. 두 발언을 함께 제시한 현재 판정에 문제 없음. 실제 준수율이나 도구 효과로 확대하면 안 된다. |
| cartoonist498 | [R06](../sources/reddit/R06-superpowers-relevant.json), `p59ddh8` | 시간·토큰 부담과 적은 결과 개선 때문에 Superpowers를 중단하고 모델 orchestration으로 옮겼다는 진술. **프레임워크 중단**은 확인되지만 TDD 전면 포기나 TDD만의 비용은 확인되지 않는다. README/Reddit 작업 기록이 이 한계를 명시하므로 문제 없음. 같은 스레드의 rubanbhatia도 보조 확인: 작은 변경마다 TDD하는 것을 비판하지만 중단 완료라고 말하지 않는다. |
| Peerless-Paragon | [R01](../sources/reddit/R01-consistent-tdd.json), `no1558i`와 `no1h6yp` | 약 3,000 unit tests의 유지보수 실패를 서술한 뒤 **TDD + Testing Trophy**를 개인 프로젝트에 도입했다고 명시한다. 후속 댓글에도 Green 후 commit, Refactor 후 commit하는 본인 절차가 있다. TDD 유지·전략 수정이라는 보고서 해석은 타당하며 TDD 포기라는 해석은 원문과 반대다. |
| 비브로스 | [보관 HTML](../sources/skills-korean/boostbrothers-tdd-subagent-harness.html), §2·§3·§8·§9 | 한 달 실제 기능 투입, `/tdd-pipeline:install`·`/tdd-pipeline:run` 진입 스킬, 에이전트 역할·게이트가 명시된다. 커스텀 TDD 스킬/하네스 실사용 자기보고로 타당하다. 여러 실패 테스트를 묶는 파이프라인과 선택적 Refactor를 단일 테스트 strict RGR로 바꾸지 않은 구분도 타당하다. **명시 TDD 요청시에만 호출하고 일반 구현·버그 수정·리팩터에 자동 호출하지 않는 정책**이 원문에 있다. 선택적 라우팅의 직접 근거로 보충 가능하며, 실제 모든 호출에서 정책을 지켰다는 독립 증거는 아니다. |
| 햄스터아저씨 | [보관 HTML](../sources/skills-korean/hamster-superpowers-review.html), 종합 비교·결론 | 3개 과제의 Superpowers 유무 비교, CLI 테스트 28개, 합계 토큰 36,975/60,239·시간 179/483초는 원문과 일치한다. 프레임워크 전체 관찰값이며 TDD 하위 스킬 단독 비용·RED 실행은 아니다. **일회성에 과하다는 조건부 판단은 있지만 실제로 계속 생략하며 운영했다는 진술은 없다.** 아래 수정 항목 참조. |
| Tony Cho / Flowkater | [보관 HTML](../sources/skills-korean/flowkater-superpowers.html), 들어가며·나가며 | 직접 만든 커맨드·TDD 스킬, 병렬 작업 중 호출 망각과 환경별 설정 때문에 생략했던 경험, 이후 Superpowers 사용과 스킬 추가 지속이 본문에 있다. 개인 스킬 사용·생략과 프레임워크 전환 자기보고는 타당하다. 제품 소개 부분의 자동 TDD 설명을 특정 작업의 실제 하위 스킬 실행·RED 로그로 올리지 않은 한계 표시도 타당하다. |

보조 표본: [raw_anon_1111 HN API](../sources/hn/api/item-47397738.json)를 직접 읽었다. 코드 변경 후 적절한 테스트를 실행시킨다는 진술과 Cognito admin UI에서 코드를 보지 않고 기능·UX를 검토했다는 진술이 있다. `working/hn.md`의 **변경 후 실행 / 테스트 작성 시점 미상** 구분은 정확하다. 구현 후 테스트 *작성* 사례로 재분류하면 안 된다.

## 수정 필요와 전달

1. **중간 수준 — 햄스터 판단을 실제 선택적 운영으로 확대.** 초기 `working/skills-korean.md` 제목의 “선택적으로 생략”, “항상 켜는 사용자는 아니다”, 마지막 종합의 “생략했다”는 원문의 비교 후 판단보다 강하다. “일회성 작업에는 과하다고 판단 / 용도별 사용을 권장”으로 낮춰야 한다. 주 작성자에게 전달했고 주 작성자가 교정 예정이라고 확인했다. 실제 파일 반영은 아래 최종 확인에 기록한다.
2. **보충 권장 — 비브로스 선택적 호출 정책.** 사용 경험과 함께 명시 요청시에만 실행한다는 설계 정책을 제시하면 사용/비사용 선택을 더 직접적으로 답할 수 있다. 주 작성자가 별도로 발견한 동일 대목을 독립 대조해 확인했다. 이를 운영 준수율로 표현하지 않는 조건으로 보충에 동의한다.

## 문제를 발견하지 않은 범위

- README의 결론은 사용 사례의 **존재**를 말하며, 공개 경험 표본의 비중을 전체 채택률로 바꾸지 않는다. 방법론에도 자기선택·검색·로드된 댓글 범위 한계와 설문 미발견의 범위가 있다.
- 현재 정의를 과거 작성자의 스킬 버전으로 소급하지 않는다고 명시했고, 제3자 스킬의 성능 주장을 검증 결과로 취급하지 않는다.
- 지속 사용, 작은 변경에 대한 불만, 프레임워크 중단, TDD 지시와 실행의 차이, 무자동시험 경험을 함께 다뤄 반대 경험을 숨긴 징후는 검토 표본에서 발견하지 못했다. 미열람 댓글 전체의 방향은 검토하지 않았다.
- R06 한 토론의 반복 댓글을 독립 사용자 수로 세지 않으며, SuperClaude와 Superpowers도 구분한다.

## 아카이브와 링크 한계

Reddit JSON/스냅샷 대상 이메일 주소 형식 검색에서는 일치 항목을 발견하지 못했다. 스냅샷의 계정 UI 생략 표시도 확인했다. 이는 전체 아카이브 비밀정보 감사를 통과했다는 뜻은 아니다.

초기 검토 시 README가 참조하는 `working/skills-english.md`, `sources/README.md`, `sources/manifest.json`, `review.md`, `artifact-check.json`은 아직 생성되지 않았다. 작성 중 산출물임을 전제로 주 작성자에게 전달했다. 최종 생성 뒤 링크 검사가 필요하다. 국내 원문 경로와 Reddit 표본 JSON 경로는 존재했다.

## 최종 확인 상태

- 햄스터의 제목·사용 상태·본문·종합이 **조건부 판단/권고**로 교정된 것을 `README.md`와 `working/skills-korean.md`에서 확인했다. 이 지적은 해결됐다.
- 비브로스의 명시 요청 라우팅 정책이 README 사례 행과 국내 종합에 보충됐다. 자기보고와 정책을 실제 준수 로그로 확대하지 않아 보충 적절하다.
- 보관된 Superpowers/Matt TDD 정의도 읽었다. 예외에서 사람과 상의, Matt의 합의된 경계·한 테스트 단위 진행·Refactor의 별도 리뷰 단계 구분은 README와 일치한다.
- 영문 작업 기록 도착 후 추가 대조를 아래와 같이 완료했다. 모든 최종 링크·해시의 재검사는 주 작성자의 산출물 검증 범위다.

## 영문 증분 추가 대조

`working/skills-english.md`와 선별 사본 2개를 읽고, [7월 스레드 공개 API](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/.json?raw_json=1) 및 [5월 스레드 공개 API](https://www.reddit.com/comments/1to6329.json?raw_json=1)를 검토자가 웹 도구로 독립 열람했다. 아래 핵심 발언은 선별 사본과 API에서 일치했다.

- **sarcasmguy1**: [onyry7t](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onyry7t/)의 Matt Pocock TDD 스킬 링크와 현재 사용 진술은 명확하다. 반면 brainstorming은 유지했고 추후 제거할 계획이다. **영문 핵심 판독의 “Superpowers를 삭제한 뒤 … Matt … 쓰는 사용자”는 이 사람과 다른 작성자의 삭제 행동을 합친 과장이다.** “일부 스킬을 유지하면서 Matt TDD로 대체”로 교정하도록 주 작성자에게 전달했다. 상세 사례 본문은 이미 올바르게 구분한다.
- **soggy_mattress**: [ov1xxug](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/ov1xxug/)은 TDD 적용 범위·단위 테스트 통과 의존을 비판하고 모든 스킬 없이 며칠 시험 중이라고 말한다. 영구 중단·TDD 전체 포기로 읽지 않은 판정이 정확하다. 모델 변화와의 상관은 본인 추측이라는 한계도 정확하다.
- 보조 대조 **elwutang**: [ov1yeqj](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/ov1yeqj/)은 직장 Claude/개인 Codex, Red→구현→Green 준수, 구현 뒤 E2E 생성·실행을 말한다. 실행 순서 자기보고는 강하지만 로그 자체는 없다. 영문 사례1 제목의 “실제 RED 실행”은 “RED 순서 준수 자기보고”로 낮추도록 전달했다.
- 보조 대조 **Spirited-Car-3560**: [onzgv1h](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onzgv1h/)은 되돌리고 삭제했다는 완료형과, 나중에 자체 하네스에 TDD를 넣을 수 있다는 미래형을 구분한다. 현재 판정에 문제 없음.
- 보조 대조 **tonyboi76**: [onzk3lr](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onzk3lr/)의 구현 전 실패 테스트 실행·RED 출력 강제 진술을 확인했다. 자체 버전이라는 맥락은 같은 작성자의 [onz74u1](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/onz74u1/)에서 확인된다. 초기 선별 사본은 이 부모 발언을 생략했으므로 부모 보관/링크 보충을 전달했다. actual gate 코드·RED 로그는 확인되지 않는다.

영문 교정 1건과 제목 정밀화·부모 보충의 반영 여부는 주 작성자가 최종 확인한다. 위 증분 외에 새로운 유의한 오분류는 발견하지 못했다.
