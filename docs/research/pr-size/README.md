# AI 리뷰 환경의 PR 크기와 GitHub Flow

PR은 작고 응집된 변경을 기본으로 삼되, 과거의 줄 수 기준을 고정 상한으로 적용하지 않는 것이
적절하다. AI는 큰 diff에도 리뷰 출력을 만들 수 있지만, 변경 사이의 상호작용과 검증 범위,
통합 후 피드백 지연, 되돌리기 비용까지 없애지는 않는다. 반대로 한 기능의 시험·호출부·설명을
인위적으로 분리하면 검토에 필요한 맥락과 중간 상태의 안전성이 나빠질 수 있다.

이 조사는 2026-09-11에 확인한 일차 연구, 공식 운영 지침, 공개 PR 기록을 비교한다. 적용 대상은
사내 동료용 소프트웨어를 개발하며 AI가 구현·리뷰를 돕고 사람이 의도와 위험을 판단하는 팀이다.
최적 줄 수를 추정하는 자체 실험이나 메타분석은 수행하지 않았다. 확인한 연구 중 AI 리뷰의 정확도·
누락률·총비용을 PR 크기별로 비교해 AI 리뷰 환경만의 최적 LOC 임계값을 산출한 연구는 없다.
원문 플레이북은 계획 검토,
독립 작업 분할과 병렬 세션, AI 리뷰와 사람의 통합 판단을 안내하지만 PR 크기나 계획과 PR의
일대일 관계를 고정하지 않는다.[^1]

## 서로 다른 네 가지 질문

AI 작성 PR의 크기와 병합률, AI 리뷰의 결함 발견 능력, 변경 분할의 리뷰 효과, 안전한 통합 단위는
서로 다른 질문이다. 병합됐다는 사실은 결함이 없다는 뜻이 아니고, 댓글이나 수락된 제안이 많다는
사실은 놓친 결함이 적다는 뜻이 아니다. 작성 속도, 첫 리뷰 속도, 전체 리드타임도 별개다.

| 질문 | 필요한 관측 | 이 조사에서 확인한 한계 |
|---|---|---|
| 큰 AI PR이 실패하는가 | 난이도·유형을 맞춘 변경과 후속 결함 | 공개 연구의 미병합에는 방치·중복도 섞임 |
| AI가 큰 PR을 정확히 리뷰하는가 | 정답 결함과 오탐·누락, 크기별 비용 | 벤더 발표와 댓글 관측만으로 recall을 알 수 없음 |
| 나누면 리뷰가 좋아지는가 | 같은 변경을 분할/비분할한 비교 | 작은 통제실험은 모든 지표에서 개선되지 않음 |
| 어느 크기로 통합할 것인가 | 중간 상태·의존성·운영 피드백·복구 | 리뷰 도구 능력만으로 결정할 수 없음 |

## 연구에서 확인한 결과

### DORA: AI와 작은 작업 단위의 관계

2025 DORA 보고서는 4,867명 설문과 78명 인터뷰를 사용했다. 작은 작업 단위는 최근 커밋 줄 수,
릴리스에 담는 변경 수, 작업 완료시간을 묶어 측정하며 PR 줄 수 하나가 아니다. 작은 단위로
일하는 조건에서 AI와 제품 성과의 긍정적 관계가 강화됐지만, 개인 효율성에 대한 효과는 다르게
나타났다. 관찰·자기보고와 통계모형의 결과이므로 특정 PR 크기의 인과 효과로 읽을 수 없다.[^2]

DORA의 실행 지침은 AI가 빠르게 생성한 큰 변경을 검증·통합하는 문제 때문에 작은 작업 단위를
권한다. 이 방향은 채택하되, 지침의 일수나 설문 구간을 이 팀의 PR 차단 기준으로 가져오지 않는다.[^3]

### AI 작성 PR: 병합 여부와 크기는 연관되지만 품질과 같지 않음

Ehsani 등의 연구는 공개 저장소의 AI 작성 PR 33,596건을 분석했다. 미병합 PR은 변경 줄 수와
파일 수가 더 큰 경향이 있었지만 효과크기는 제한적이었다. 전체 병합률은 71.48%였고 에이전트별
차이도 컸다. 수작업으로 본 거절 사유에는 방치·중복·CI 실패가 포함된다.[^4]

이는 무관한 변경을 섞거나 검증을 미루지 않을 이유를 보탠다. 다만 AI 작성 여부를 AI 리뷰 효과로
바꾸어 해석할 수 없고, 과제 난이도가 같은 PR을 크기만 달리한 실험도 아니다. 병합률을 최종 품질이나
최적 크기의 대리값으로 삼지 않는다.

### 기업 AI 리뷰 도입: 속도와 사람의 일이 항상 줄어들지는 않음

Beko의 GPT-4 기반 Qodo PR-Agent 사례는 분석 가능한 세 프로젝트의 PR 4,335건을 전후 비교했다.
도입 후 PR은 1,568건이다. 평균 종료시간은 5시간 52분에서 8시간 20분으로 늘었으나 한 프로젝트에서는
줄었다. 사람의 댓글 수 감소는 유의하지 않았다. 봇 댓글의 73.8%가 resolved로 처리됐지만 이는
결함 정확도나 누락률을 뜻하지 않는다.[^5]

논문 당시 평균 사용량은 PR당 3,937토큰과 약 0.48달러였다. 특정 모델·도구·작업 구성의 과거 측정이며
현재 비용 견적이 아니다. 단일 기업의 비무작위 전후 비교여서 계절·프로젝트 차이를 배제할 수 없다.
따라서 AI 리뷰 도입만으로 큰 PR의 전체 비용이 낮아진다고 가정하지 않는다.

### AI가 AI를 리뷰하는 관측도 최적 크기를 알려주지 않음

Selvanayagam과 Ghaleb은 AI 작성과 AI 리뷰가 연결된 PR 248,641건을 조사했다. 같은 제품끼리와
다른 제품끼리의 리뷰에서 댓글 양과 첫 리뷰 지연이 달랐다. 그러나 타임스탬프 보존과 리뷰어 구성이
다르며, 논문이 재는 출력량·범주·지연은 결함 정확성이나 후속 제품 품질이 아니다.[^6]

AI가 리뷰 양쪽에 참여하는 현상은 충분히 관측되지만, 그것만으로 사람이 보던 PR보다 몇 배 큰
PR을 안전하게 통합할 수 있다고 계산할 수 없다.

### 분할의 반례: 모든 리뷰 지표가 좋아지는 것은 아님

di Biase 등의 통제실험에서 28명은 약 100줄·7파일의 Java 변경을 하나로 묶거나 기능과 리팩터링으로
분해한 상태로 검토했다. 분해는 오탐을 줄였지만 발견한 결함 수, 리뷰 시간, 변경 의도 이해 등에서는
유의한 차이가 없었다. 한 시스템의 작은 표본이라 큰 PR이나 현재 AI 리뷰에 일반화할 수 없다.[^7]

이 결과는 분할이 항상 더 빠르고 정확하다는 강한 주장에 제동을 건다. 나누는 목적과 경계가
분명해야 하며, 기능을 설명하는 데 필요한 부분까지 기계적으로 분리할 근거는 약하다.

## 공식 운영과 공개 사례

### Anthropic: 큰 diff를 실제로 다루는 AI 리뷰

Anthropic은 2026-03-09 발표에서 큰 PR에 더 많은 에이전트를 투입한다고 설명했다. 자체 관측상
1,000줄 초과 PR의 84%에 finding이 있었고 평균 7.5건이었다. 50줄 미만은 31%와 0.5건이다.
거의 모든 내부 PR에 사용하며 최종 승인은 사람이 한다고 밝혔다.[^8]

표본 수, 실제 존재한 전체 결함, 크기별 severity·recall은 공개하지 않았다. incorrect로 표시된
finding 비율이 1% 미만이라는 수치도 모든 지적이 독립 검증됐다는 뜻은 아니다. 큰 PR에 유용한
검토를 제공할 수 있다는 근거로 채택하고, 큰 PR의 안전성이나 권장 크기 증명으로 사용하지 않는다.

### TrueNAS: 실제 발견과 초기 무지적이 함께 남은 PR

공개 PR #18291은 암호화 관련 리팩터링으로, 조회 시 9파일·464줄 변경·32커밋이었다. Claude는
영향받은 인접 코드에서 문자열을 사전 목록에 포함 여부로 비교하여 암호화 키 캐시가 항상 비워질 수
있는 문제를 지적했다. 기록에는 앞선 리뷰의 무지적 응답과 후속 리뷰의 구체적인 발견이 함께 남아 있다.[^9]

코드 리뷰가 diff 밖의 중요한 맥락을 찾을 수 있다는 실제 사례다. 동시에 무지적 결과를 완료 증거로
단독 사용해서는 안 된다는 사례다. 이 PR은 1,000줄 초과 사례가 아니며, 재리뷰 사이의 diff·문맥도
동일하게 통제되지 않았다. 단순한 모델 비결정성 실험이나 크기 비교로 해석하지 않는다.

### Google: 줄 수의 경험칙과 개념적 응집성

Google 지침의 중심은 하나의 자기완결적 변경, 관련 시험, 통합 뒤 정상 동작이다. 새 API에는
실제 사용 맥락을 함께 두어 너무 작은 변경도 피한다. 경험적인 줄 수 예를 제시하지만 절대 규칙으로
정하지 않으며 대량 삭제와 신뢰할 수 있는 자동 리팩터링에는 예외를 둔다.[^10]

Google의 별도 사례연구는 약 900만 변경에서 중앙 크기 24줄과 크기별 피드백 시간 차이를 보고했다.
이는 성숙한 단일 조직의 운영 분포이며 AI 시대의 최적값이 아니다. 대규모 삭제·생성 변경이 일반
동작 변경과 다른 분포를 만들 수 있다는 점을 함께 고려해야 한다.[^11]

### GitHub: 독립 작업, 의존 작업, 통합과 노출의 분리

GitHub Flow는 변경 브랜치, 필요하면 Draft PR, 피드백 반영, 검토 후 기본 브랜치 통합과 작업
브랜치 정리라는 가벼운 흐름이다. 서로 무관한 변경 묶음은 별도 브랜치로 둔다. 모든 개발건을
하나의 PR로 만들거나 단계 문서마다 PR을 만들라는 규칙은 아니다.[^12]

GitHub의 2021년 내부 사례는 장기 기능 브랜치 대신 작은 변경과 기능 플래그를 사용하며, 선행
데이터 모델을 기다리는 작업에는 의존 브랜치나 작은 변경 추출을 활용했다. 리뷰·rebase 비용도
인정한다. 머지와 사용자 노출은 다른 결정이라는 원리는 채택하되, 작은 로컬 CLI에 플래그 기반
배포 체계를 의무적으로 추가하지 않는다.[^13]

2026-08-04의 GitHub 글은 1,721줄 쇼핑 검색을 데이터·API·연결·UI의 네 PR로 나누는 예시다.
실제 비교 연구가 아니라 튜토리얼이다. 분할 경계를 설명하는 데 유용하지만 PR 개수의 모범 답안은
아니다. native stacked PR 문서에도 하위 변경의 연쇄 rebase와 계층별 CI 비용이 드러난다.
이 기능의 도입은 필요할 때의 선택이며 템플릿은 stack 도구를 요구하지 않는다.[^14]

## 템플릿에 채택한 판단

작고 응집된 변경을 기본으로 삼는다. 서로 독립적인 가치나 위험은 분리하고, 한 동작을 이해하고
검증하는 구현·관련 시험·설명은 함께 둘 수 있다. generated code, lockfile, fixture, 대량 삭제와
직접 작성한 동작 변경을 구분한다. LLM 생성물이라는 이유만으로 결정적인 기계 변환으로 취급하지 않는다.

| 상황 | 운영 판단 | 남길 근거 |
|---|---|---|
| 작은 기능의 API·CLI·시험 | 하나의 응집된 PR 가능 | 동작·인접 회귀 확인 |
| 두 독립 기능의 사용 시점이 다름 | 먼저 쓸 수 있는 결과부터 분리 | 부분 완료 범위·통합 순서 |
| 기능 추가와 광범위한 코드 이동 | 분리 검토 | 각 목적과 diff |
| 검증 가능한 대량 치환·삭제 | 큰 PR 허용 가능 | 변환 범위·동작 불변 확인 |
| 공유 스키마·API·실행 프로세스 변경 | 중간 호환성부터 판단 | 이전/새 버전 공존과 복구 |
| 검토 계층이 너무 많은 stack | 묶음 재조정 가능 | rebase·CI·재검토 비용 |

AI에 맡기는 작업과 검토의 단위, Git PR의 통합 단위, 실제 배포와 사용자 노출의 단위는 일치할
필요가 없다. 단일 PR도 순차 배포되는 프로세스나 데이터 마이그레이션의 원자성을 보장하지 않는다.
여러 에이전트의 개별 검토가 끝난 뒤에도 경계 사이 동작과 통합 후 회귀를 확인한다.

GitHub Flow의 통합 기준은 제품 main이며 작업은 최신 main에서 시작한다. 단계 문서 수락은
대상 SHA와 사람의 결정 기록으로 남기고 구현 PR 머지와 구분한다. 여러 PR이 공통 plan을
참조할 때 각 PR의 범위를 명시한다. merge commit은 승인 SHA를 보존하기 쉬운 이 템플릿의
기본 선택이며 플레이북이나 GitHub Flow가 유일하게 요구한 방식은 아니다.

배포 정책은 [PR 크기 가이드](../../PR-SIZE.md)와 [GitHub Flow 정책](../../GIT-WORKFLOW.md)다.
두 파일은 실제 사용 브랜치의 docs/에도 동일하게 배포한다. 자세한 연구나 실험 절차를 제품
템플릿에 복사하지 않고, 기존 지침·계획·리뷰에서 두 문서로 연결한다.

## 검증과 남은 질문

F02 실험은 담당자 조회와 상태 요약을 실제 사용 템플릿에서 개발하여 PR 범위 판단, 두 번의
통합, 중간 정상 상태, 동적 리뷰 수정과 인도를 확인한다. 정해 둔 대사를 재생하지 않는다.
이 실험은 대형 PR과 소형 PR의 품질·비용 우열을 재는 A/B 실험이 아니며 최적 줄 수를 산출하지 않는다.
실제 결과와 한계는 [실험 기록](../../experiments/0016-flow-pilot.md)에 별도로 남긴다.

앞으로 다른 개발건에서도 리뷰·수정 시간, 통합 후 결함과 재작업, 복구 경험, AI 비용을 함께
관찰할 수 있다. 현재는 정량 대시보드나 별도 상한 검사기를 만들지 않는다. AI 작성과 AI 리뷰
조건을 구분하고 작업 난이도·언어·생성 파일 비중을 고려하지 않은 줄 수 비교는 피한다.

## Sources

[^1]: Anthropic, [Claude Code plan mode](https://academy.claude.com/courses/ai-native-sdlc-playbook/plan-mode), [Parallel sessions and subagents](https://academy.claude.com/courses/ai-native-sdlc-playbook/parallel-sessions-and-subagents), [AI in the PR review loop](https://academy.claude.com/courses/ai-native-sdlc-playbook/ai-in-the-pr-review-loop). 게시일 미표기, 2026-09-11 확인.
[^2]: Derek DeBellis, Kevin Storer, Nathen Harvey 외, DORA/Google Cloud, [2025 State of AI-assisted Software Development](https://dora.dev/research/2025/dora-report/), 2025, v2025.2.
[^3]: DORA, [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/), 게시일 미표기, 2026-09-11 확인.
[^4]: Ramtin Ehsani 외, [Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub](https://arxiv.org/abs/2601.15195), 2026-01-21, MSR 2026.
[^5]: Umut Cihan 외, [Automated Code Review in Practice](https://arxiv.org/abs/2412.18531), 2024-12, ICSE-SEIP 2025.
[^6]: Niruthiha Selvanayagam, Taher A. Ghaleb, [AI-to-AI Code Reviews of GitHub Pull Requests](https://arxiv.org/abs/2608.21311), 2026-08-21, ESEM 2026.
[^7]: Marco di Biase 외, [The Effects of Change Decomposition on Code Review—A Controlled Experiment](https://doi.org/10.7717/peerj-cs.193), PeerJ Computer Science, 2019-05-13.
[^8]: Anthropic, [Bringing Code Review to Claude Code](https://claude.com/blog/code-review), 2026-03-09. 수치와 가격은 해당 발표의 자체 관측.
[^9]: TrueNAS, [NAS-139874 PR #18291](https://github.com/truenas/middleware/pull/18291), 2026-02-24~03-03; [PR API record](https://api.github.com/repos/truenas/middleware/pulls/18291), 2026-09-11 조회.
[^10]: Google, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), [본문 변경 커밋](https://github.com/google/eng-practices/commit/fde5fd40e259bb703dec55f17729abe99c17bf73), 2024-04-24.
[^11]: Caitlin Sadowski 외, [Modern Code Review: A Case Study at Google](https://research.google/pubs/modern-code-review-a-case-study-at-google/), ICSE-SEIP 2018.
[^12]: GitHub Docs, [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow), 게시일 미표기, 2026-09-11 확인.
[^13]: Alberto Gimeno, GitHub, [How we ship code faster and safer with feature flags](https://github.blog/engineering/infrastructure/ship-code-faster-safer-feature-flags/), 2021-04-27.
[^14]: Julia Muiruri, GitHub, [Turn one giant AI-generated pull request to a reviewable stack](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/), 2026-08-04; GitHub Docs, [About stacked pull requests](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs), [Optimizing CI for stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests), 2026-09-11 확인. native stack의 현재 제품 상태·제약은 도입 시 다시 확인한다.
