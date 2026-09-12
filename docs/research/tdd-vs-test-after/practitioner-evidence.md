# 공개 실험과 실무 경험

## 직접 비교에 가까운 공개 실험

**B3. Bryan Finster의 workflow matrix**는 작은 계산기 과제 4개, 방식별 6회, 최초 구현과 후속 변경 3단계를 비교했다. 모델은 `claude-sonnet-4-6`이다. 아래는 공개 JSONL 672행을 다시 집계한 값이다. 에이전트 실험 자체를 재실행하지 않았다.

| 방식 | 완료 cell의 기록 API 비용 평균(구현+변경 3회) | 초기 생성 테스트 mutation score | 후속 변경당 코드 변경량 | 외부 인수 테스트 |
|---|---:|---:|---:|---:|
| 동작별 구현 → 테스트 → 정리 지시, 단일 에이전트 | $0.993 | 0.863 | 40.03줄 | 모두 통과 |
| 동작별 TDD 지시, 단일 에이전트 | $1.589 | 0.799 | 39.65줄 | 모두 통과 |
| 전체 구현 → 전체 테스트 지시, 단일 에이전트 | $2.089 | 0.934 | 51.49줄 | 모두 통과 |

작게 구현하고 바로 검증하는 대안에 유리한 결과다. 그러나 작은 Python 계산기·단일 모델이며 정확성은 모든 방식에서 포화됐다. 유지보수성은 코드 변경량이라는 대리 지표다. 자체 합성 점수와 ±1 표준오차 구간으로 정한 순위를 보편적 우열로 채택하지 않는다. 숨겨진 테스트를 주입하는 harness는 확인했으나 실행 당시 코드·전체 실행 로그의 재현성까지 확인한 것은 아니다. 비용은 **완료된 cell에 기록된 API 비용**이며 사람 검토 시간은 아니다. 보관 harness는 재시도 전 비용을 합산하지 않고 마지막 응답을 반환하며, 4단계를 끝내야 결과 행을 저장한다. 따라서 재시도·중단 cell의 소비 비용이 빠질 수 있어 실제 전체 지출로 읽을 수 없다. TDD는 프롬프트 지시 조건이며 의도한 RED 실행 준수를 확인하는 센서는 없다.

[원문](https://devteam.bryanfinster.com/docs/experiments/05-final-results/) · [고정판 전체](originals/practitioner/B3-finster-05-final-results.md) · [공개 원자료 전체](originals/practitioner/B3-refactor-workflow-matrix.jsonl) · [7개 방식 재집계](data/finster-recalculation.json) · [재집계 스크립트](working/recalculate-finster.py)

**B2. Dan Luu의 2026-09-07 실험**은 Rust Zstd 구현에서 검증 기법을 지정하는 프롬프트를 비교했다. Codex·GPT-5.6 Sol, 조건·추론 수준마다 80회이며 숨겨진 테스트 전부를 통과한 실행 비율을 측정했다. 원문 연결 차트의 값을 추출했다.

| 추론 수준 | 기본 지시: 완전 통과율 / 평균 비용 | TDD 지시: 완전 통과율 / 평균 비용 |
|---|---:|---:|
| medium | 63.8% / $3.31 | 58.8% / $3.27 |
| xhigh | 81.2% / $5.92 | 73.8% / $5.50 |

이 설정에서는 TDD 지시가 기본 지시보다 개선되지 않았다. 그러나 **TDD를 지시한 효과와 숙련된 TDD를 충실하게 수행한 효과는 다르다.** 기본 조건도 테스트하며 엄격한 test-after 통제군이 아니다. 공개 차트의 집계값을 확인한 것으로, 전체 실행 원자료·숨겨진 채점기의 독립 재현이나 유의성 재검정은 하지 않았다. 몇 개의 명확한 프로토콜 명세 과제를 웹앱 전체로 일반화하지 않는다.

[실험 원문](https://danluu.com/agentic-testing/) · [전체 HTML](originals/practitioner/B2-danluu-agentic-testing.html) · [원본 차트](originals/practitioner/B2-danluu-chart.html) · [차트 값 추출](data/danluu-chart-extract.json)

## 실제 작업을 설명하는 당사자 자료

**B4. thoughtbot의 Louis Antonopoulos(2026-01-12)**는 Rails 예제에서 사람이 선행 테스트를 검토하고 에이전트가 구현하는 과정을 설명한다. 실패·통과 출력이 있는 실무 시연이다. 인간의 검토와 피드백이 포함되므로, 단일 자율 실행 실험과 같은 조건이 아니다. 비용·결함에 관한 통제 비교는 제공하지 않는다. TDD의 실행 가능성과 협업 방식을 보여 주는 근거로 사용한다. [원문](https://thoughtbot.com/blog/prevent-the-robocalypse-with-tdd) · [전체 HTML](originals/practitioner/B4-thoughtbot-tdd.html)

**B1. Kent Beck·Martin Fowler·DHH의 2014년 대화**에서도 자동 테스트를 갖추는 것과 매번 테스트부터 작성하는 것은 분리된다. DHH는 자기 업무의 상당 부분에서 TDD가 맞지 않았다고 설명하고, Beck은 특정 동작을 작은 단계로 구체화하는 가치를 강조한다. 이것은 당사자의 경험과 설계 논쟁이며 Rails 전체의 현재 개발 정책이나 비교 실험이 아니다. [원문 및 회의록](https://martinfowler.com/articles/is-tdd-dead/) · [전체 HTML](originals/practitioner/B1-is-tdd-dead.html)

## 커뮤니티에서 확인한 상반된 경험

아래 주장은 작성자가 공개적으로 설명한 경험이다. 실제 코드·모델 조건·독립 평가를 모두 확보하지 못했으므로 효능의 증명이나 프로젝트 공식 입장으로 취급하지 않는다.

| 출처 | 확인한 주장 | 이 조사에서의 의미 |
|---|---|---|
| HN, `ivanzhaowy123`, 2026-09-08 | Superpowers가 버튼 존재 같은 낮은 가치의 테스트로 TDD 순서만 지켰다는 경험 | 테스트의 의미를 별도로 확인해야 한다는 반론. [댓글](https://news.ycombinator.com/item?id=49606921) |
| HN, `throwatdem12311`, 2026-09-08 | 같은 종류의 작업에서 TDD와 코드 검토가 유용했다는 상반 경험 | 앞 경험을 보편화하지 않게 하는 반례. [댓글](https://news.ycombinator.com/item?id=49609031) |
| HN, `siscia`, 2026-09-08 | 테스트 가능성을 좌우하는 구조와 의존성 분리를 함께 봐야 한다는 지적 | 기법 이름만 비교할 때 놓치는 조건. [댓글](https://news.ycombinator.com/item?id=49608977) |
| HN, `lmeyerov`, 2026-09-08 | GFQL·Louie 경험에서 기능 탐색 뒤 더 무거운 검증을 배치한다고 설명 | 탐색과 최종 품질 검증을 나누는 사례. 역할은 댓글의 자기 보고 수준. [댓글](https://news.ycombinator.com/item?id=49610972) |
| HN, `josephg` | 별도 JMAP 적합성 테스트를 기준으로 에이전트가 구현을 수정한 경험 | 독립된 판정 기준과 수정 루프의 가치. 모든 세부 작업의 TDD 증거는 아님. [댓글](https://news.ycombinator.com/item?id=47332444) |
| Reddit, `RunAI_Coder`·`Stubbby` | 같은 구현 해석에서 테스트가 만들어질 때 외부의 정답 기준이 필요하다는 논의 | 새로운 비교 실험이 아니라 Dan Luu 글에 대한 해석. [스레드](https://www.reddit.com/r/AgentsOfAI/comments/1wd29ns/dan_luu_ran_160_agent_runs_per_testing/) |

실제 브라우저 열람 기록: [HN 첫 스레드](working/aside-hn-49605246-full.txt), [HN 두 번째 스레드](working/aside-hn-47327559-full.txt), [Reddit](working/aside-reddit-1wd29ns-full.txt). Reddit 기록에서 로그인 UI의 계정 정보와 접속용 URL 매개변수는 제거했다. 본문·댓글은 유지했다. 전체 사이트나 각 댓글의 외부 링크까지 재귀적으로 보관한 것은 아니다.

[전체보고서](README.md) · [조사 방법](methodology.md)
