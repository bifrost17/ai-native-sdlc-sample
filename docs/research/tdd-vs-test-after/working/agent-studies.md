# 코딩 에이전트의 TDD와 사후 테스트: 논문 근거 카드

확인 기준일: 2026-09-12. 수치는 저자 보고이며 자체 벤치마크를 수행하지 않았다. PDF 쪽수는 로컬 PDF의 첫 장을 1로 센다. 원본은 `../originals/studies-agent/`, 서지·버전·해시는 `../data/agent-studies-sources.json`에 있다. 프리프린트의 출판 확정 여부는 별도 확인 없이는 추정하지 않는다.

## 판정 기준

**직접 순서 비교**는 테스트 작성 시점만 바뀌고 구현·테스트·수정 기회가 같은 조건이다. **근접 비교**는 테스트를 구현 전에 보여주는지 비교하지만 미리 존재하는 인간 테스트를 사용한다. **묶음 비교**는 테스트·도구·반복·문맥선택이 함께 바뀐다. **인접 근거**는 테스트 오라클 품질, 작성량, 인간 피드백을 다룬다. 네 종류를 한 효과크기로 합치지 않는다.

## A1. TENET — 가장 유용한 테스트 사용 시점 비교

Yiran Hu, Shanchao Liang, Nan Jiang, Yi Wu, Lin Tan. *TENET: One Step Toward Test-Driven Development for Repository-Level Code Generation*, arXiv:2509.24148v4, 2026-08-13; 최초 2025-09-29. [원문 §V-E, Table VI, PDF p.10](https://arxiv.org/html/2509.24148v4).

- **근접 비교.** DeepSeek-V3, RepoCod 980개 누락 함수 구현, 평균 수정 38.18 LOC. 기존 인간 테스트 중 최대 3개를 선택하고 나머지는 최종 평가까지 감춘다.
- Pass@1: 테스트 없음 29.90%, 구현 전만 36.93%, 구현 후 수정에만 42.65%, 양쪽 모두 49.18%. 양쪽 대 사후 차이는 **+6.53%p**. plotly.py에서는 사후 조건이 더 좋았다.
- 평균 입력/출력 토큰은 사후 138,330/4,710, 양쪽 147,968/4,645; API 호출 8.91/8.28. 토큰 합 증가율은 **6.7%**(표에서 계산).
- **한계:** 이미 작성된 테스트의 정보 제공 시점이지 새 테스트의 RED-GREEN 순서가 아니다. temperature 0, 작업별 1패치, 반복실험 부재. 테스트는 기존 구현을 알고 작성됐으며 평가에 노출된 일부 테스트도 포함된다. 시스템 간 큰 개선폭보다 이 내부 비교가 질문에 가깝다.
- **재현:** 논문·PDF 확보. 본문에서 실행 가능한 공식 저장소 링크는 확인하지 못했다.

## A2. TDD-Agent — 단순 test-first 효과와 전체 루프 효과가 다름

Hongyue Yu 외 6인. *TDD-Agent: Test-Driven Reasoning for Code Generation*, arXiv:2608.16742v1, 2026-08-17. [원문 Tables 2–4, Appendix B Table 6](https://arxiv.org/html/2608.16742v1).

- **근접·묶음 비교.** GPT-5-mini-2025-08-07(minimal), DeepSeek-V3.2, Qwen3-Coder-30B-A3B. LiveCodeBench 224문제×10샘플에서 테스트 생성 지시 제거 대비 +1.65/+0.58/+1.03%p(PDF p.11). 테스트 사후 작성 대조군은 없다.
- RepoEval은 8개 저장소의 **455개 함수 완성**이며 전체 앱 구현이 아니다. 원래 테스트를 감추고 최종 판정에 사용한다. GPT에서 1회 test-first 69.89%, 같은 도구의 Vanilla 68.35%; 전체 공동수정 78.24%, 코드만 반성 72.09%, 테스트 고정 70.11%(Table4,p.7).
- Qwen의 5회 루프는 mini-SWE-agent 대비 58.46% 대 52.97%, 42.47초 대 26.71초(Table2,p.4; Table10,p.13).
- **한계:** 순서·실행피드백·테스트 수정이 결합된다. 자기 테스트를 통과해도 숨긴 테스트에 실패하는 사례가 주요 실패 유형이다. 토큰 비용은 Table3, 세부 Appendix C; 반복 통계는 제한적.
- **재현:** 익명 [저장소](https://anonymous.4open.science/r/TDD-Agent-Framework-6370/) 제시; 본 조사에서는 내용 접근을 확인하지 못했다.

## A3. TDAD — 절차 지시만으로 회귀가 악화된 반례

Pepe Alonso, Sergio Yovine, Victor A. Braberman. *TDAD: Test-Driven Agentic Development*, arXiv:2603.17973v2, 2026-03-19. [원문 Table4–6, PDF pp.4–5](https://arxiv.org/html/2603.17973v2).

- **프롬프트·문맥 묶음 비교.** SWE-bench Verified 첫 100건, Qwen3-Coder30B Q4_K_M, 32K 문맥, 15분 한도. Vanilla/TDD지시/GraphRAG+TDD의 해결률은 31/31/29%; P2P 테스트 실패율은 **6.08/9.94/1.82%**.
- 개선은 테스트 영향 범위 지도를 추가한 조건에 있다. 이는 엄격 TDD의 순서 효과가 아니다. 최종 간단 스킬은 구현→관련 테스트 검색→실행이다.
- **중요 분모:** 빈 패치를 제외해 테스트 풀은 9,245/8,040/8,536으로 다르다. 회귀 패치 비율은 30.2/33.3/33.3%로 GraphRAG가 낮지 않다. 많은 테스트를 한꺼번에 깨는 일부 사례가 합계에 크게 기여한다.
- 별도 25건 Qwen3.5/OpenCode 실험 해결률은 24→32%, 양쪽 회귀 0%. 2건 차이에 불과하며 유의성 검정이 없다. Table6의 generated17 대 해결분모13도 불일치한다.
- **재현:** [공식 저장소](https://github.com/pepealonso95/TDAD), README 보관. 원본 보고된 결과를 재실행하지 않았다. 시간·토큰의 동등 비용 비교는 충분하지 않다.

## A4. Agent-generated tests — 테스트 작성량을 늘리는 것의 낮은 한계효용

Zhi Chen 외 6인. *Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents*, arXiv:2602.07900v2, 2026-04-09. [원문 Tables7–8, PDF pp.8–9](https://arxiv.org/html/2602.07900v2).

- **인접 통제개입.** mini-SWE-agent, SWE-bench Verified 500건, 6모델 관찰 및 4모델 프롬프트 개입. 원래 테스트 실행은 금지하지 않는다.
- GPT-5.2에 새 테스트 작성을 권해도 해결 359/500으로 동일, 입력 +9.0%, 출력 +19.8%. Kimi K2 Thinking에 새 테스트를 억제하면 해결 63.4→60.8%, 입력 −49.0%, 호출 −35.4%.
- 네 해결률 변화는 exact McNemar에서 유의하지 않다(GPT p=1.000; Kimi p=.228). 주요 비용 변화는 paired Wilcoxon p<.001, 부트스트랩 신뢰구간도 보고한다.
- **한계:** 비유의성은 동등성 증명이 아니다. 새 테스트 파일에는 assertion보다 관찰용 print가 흔하다. 생성 파일 작성 유무를 조작했으므로 품질 높은 TDD나 사후 독립검증을 반박하지 않는다. 모델·작업당 단일 trajectory라 변동성이 남는다.
- **재현:** [Zenodo19251470](https://doi.org/10.5281/zenodo.19251470) 메타데이터 확인: 약235MB 자료·스크립트 zip. 원본 논문/메타데이터 보관, zip 재실행 없음. OpenReview 유사 제목은 별도 버전으로 혼합하지 않았다.

## A5. 구현을 본 테스트의 오류 전파

Michael Konstantinou, Florian Tambon, Mike Papadakis. *On the risk of coding before testing: An empirical study on LLM-based test generation workflow*, arXiv:2607.05139v1, 2026-07-06. [원문 §IV–VII, Figures2–4/TablesII–VI](https://arxiv.org/html/2607.05139v1).

- **인접 순서·독립성 근거.** HumanEval+, MBPP, BigCodeBench에서 GPT-5-mini, GPT-4.1-mini, Haiku4.5, DeepSeek-V4-Flash, Llama3.3-70B 비교. 초록의 평균 오류 검출은 구현 노출 후 **14%**, 요구사항만 제공 **25%**.
- 잘못된 코드에서 실패하고 기준 구현에서 통과해야 결함 검출로 센다. 동일 대화에서 구현 후 테스트와, 새 대화에서 요구사항만으로 테스트하는 비교도 후자를 지지한다(§VI-C, TableIV, p.8). CoT·요약·검증 프롬프트도 차이를 없애지 못했다.
- **선택편향:** 정상 코드·런타임 오류를 제외하고, 기준 테스트 절반 이하가 실패하는 어려운 의미 결함 중 작업별 가장 어려운 것을 선택한다. 전체 작업의 출시 결함률이나 전체 TDD 생산성 수치가 아니다.
- **판정:** 구현 노출과 작성 순서를 구분해야 한다. §VI-C는 코드 생성 뒤 같은 대화에서 시험을 만드는 조건과, 이전 코드를 제공하지 않고 요구사항만 넣은 새 대화에서 시험을 만드는 조건을 직접 비교했다. 선택된 의미 결함에서 후자의 검출 이점을 관찰했지만, 실제 저장소의 전체 개발·최종 독립 리뷰·다른 모델 사용의 효과로 일반화하지 않는다. 비용 비교·최종 수리 품질은 보고 대상 밖이다. 공개 재현 패키지 링크는 확인하지 못했다.

## A6. TDDev — 웹앱 결과와 보고 불일치

Yuxuan Wan 외 5인. arXiv:2605.17242v1, 2026-05-17. 초록 제목은 *From Runnable to Shippable: Multi-Agent…*, 본문 제목은 *From Runnable Code to Shippable Applications…*. [원문 §3.4, Table5–7, PDF pp.5–10](https://arxiv.org/html/2605.17242v1).

- **묶음 비교.** Sonnet4.6/ClaudeSDK의 baseline31.3%, incremental31.5%, whole-project49.1%, agentic65.8%; Qwen3.5는 각각23.3/71.4/51.4/41.0%(Table5,p.8).
- baseline에 배포·테스트 도구와 재시도 루프가 없다. whole-project는 전체 구현 후 테스트·수정한다. 따라서 큰 개선은 test-first만의 효과가 아니다.
- **독립평가 문제:** 생성·브라우저 판정에 같은 모델. acc@k는 각 테스트의 여러 시도 중 최고 판정을 모으므로 최종 단일 앱의 완전 통과율이 아니다.
- **신뢰도 하향:** 설정 Table2는 OpenCode+Sonnet인데 Table5는 OpenCode+Qwen. 본문50사례와 Table6의5사례, Table5와 비용 Table7의 정확도가 일치하지 않는다. 25배는 §6.2의 서로 다른 모델 최적조건의 토큰/%p 효율비이며 단순 TDD 비용배수로 읽으면 안 된다.
- **재현:** [Zenodo19251377](https://doi.org/10.5281/zenodo.19251377) 메타데이터와 약1.6MB artifact.zip 확보. ZIP 정적열람에서 지표 계산을 확인했고 RQ2 스크립트 기본값은 첫10개 중5개다. 실행하지 않았다. 표본 정의는 추가 해명이 필요하다.

## A7. ClassEval-TDD — 클래스 수준의 강한 테스트 감독

Yunhao Liang, Ruixuan Ying, Shiwen Ni, Zhe Cui. *Scaling Test-Driven Code Generation from Functions to Classes: An Empirical Study*, arXiv:2602.03557v1, 2026-02-03. [원문 Tables4/6, PDF pp.13–15](https://arxiv.org/html/2602.03557v1).

- **묶음 비교.** 정비된 ClassEval 100클래스·412메서드, 8모델. 공개 메서드 테스트+의존성 순서+최대3회 수리를 결합하고 비공개 테스트로 평가한다.
- 최선 직접생성 방식 대비 클래스 완전 성공 **+12~26%p**. GPT-oss120B45→71%, Gemini3-Flash59→71%; Qwen2.5-Coder7B33→46%(Table4).
- 평균 수리는 메서드당0.06~0.62회(Table6). 이는 총시간·토큰·인간 테스트 준비비용이 아니다. 공개 테스트 평균 line coverage98.7%라는 강한 감독조건이다.
- **한계:** 테스트를 에이전트가 작성하지 않는다. 순서만 바꾼 test-after+동일 수리 예산 대조군도 없다. 벤치마크 명세와 테스트를 연구자가 정비한 영향, 공개/비공개 테스트의 의미적 중복을 고려해야 한다.
- **재현:** [익명 저장소](https://anonymous.4open.science/r/ClassEval-TDD-C4C9/)가 제시되지만 본 조사에서 내용 접근을 확인하지 못했다. 논문·전체 PDF 확보.

## A8. TGen — 미리 제공된 인간 테스트의 함수·알고리즘 근거

Noble Saji Mathews, Meiyappan Nagappan. *Test-Driven Development for Code Generation*, arXiv:2402.13521v2, 2024-06-11. [원문 Table1, PDF p.8; §3.2](https://arxiv.org/html/2402.13521v2).

- **근접·묶음 비교.** GPT-4-Turbo1106; MBPP399, HumanEval164, CodeChef1,100. 인간 공개 테스트를 추가하고 실패하면 수리한다. 확장 EvalPlus 및 CodeChef 비공개 테스트는 생성에 노출하지 않는다.
- 비공개 판정에서 MBPP는 코드만69.67%, 테스트 제공82.45%, 수리 포함87.71%; HumanEval78.66→87.81→93.30%; CodeChef23.00→26.09→30.27%.
- **한계:** 단일 함수/경쟁프로그래밍이며 에이전트의 테스트 작성순서 비교가 아니다. baseline 실패→테스트→수리의 추가 기회도 생긴다. 현대 repository agent로 그대로 외삽할 수 없다. 테스트가 많아져 이미 성공한 문제가 실패하는 경우도 관찰된다(§5.2).
- Llama3-70B-Instruct에서도 방향이 같았으나 낮은 초기성능과 긴 비용회계 부재를 함께 보아야 한다. 저자는 replication package와 runtime 정보를 언급하지만 본 조사에서 연결된 공개 URL은 찾지 못했다.

## A9. TDFlow — 좋은 재현 테스트를 푸는 능력의 상한에 가까움

Kevin Han 외 5인. *TDFlow: Agentic Workflows for Test Driven Development*, EACL2026 pp.1511–1527; arXiv2510.23761v2. [정식 논문 Table1–2, AppendixA–B](https://aclanthology.org/2026.eacl-long.70.pdf).

- **인접 워크플로 비교.** Lite에서 모든 시스템에 일반적으로 숨겨진 인간 재현 테스트를 제공, GPT-4.1로 비교: TDFlow88.8%/$1.51, Agentless61.0%/$0.53(Table1, PDF p.5).
- **분모:** TDFlow는22건을 제외한278건; OpenHands는201건(App.A,p.11). 동일300건의 표준 리더보드 비교로 읽을 수 없다.
- Verified에서 GPT-5 solver/Sonnet4 test generator: 인간 테스트94.3%, 자기 생성 테스트68.0%(Table2,p.7).45건은 인프라 제약으로 제외(App.B). 제공된 테스트 품질의 중요성을 보여주지만, 독립 숨김평가를 통한 TDD 순서의 효과는 아니다.
- **재현:** [공식 저장소](https://github.com/AegisIK/TDFlow)는 확인일 README만 있으며 코드 공개가 진행 중이라고 적혀 있다. 따라서 논문의 detailed settings와 실제 재실행 가능성을 구분한다. 테스트 해킹7건을 실패 처리한 인간 검토는 긍정적이지만 장기 유지보수·생산성을 측정하지 않았다.

## A10. LLM4TDD — TDD가 가능하다는 초기 사례, 비교효과 아님

Sanyogita Piya, Allison Sullivan. *LLM4TDD: Best Practices for Test Driven Development Using Large Language Models*, arXiv2312.04687v1, 2023-12-07. [원문 §4.3.1, PDF p.4](https://arxiv.org/html/2312.04687v1).

- **기술적 사례연구.** ChatGPT/GPT3.5 계열과 LeetCode Python70문제. 사람의 입력공간 분할 테스트를 한 개씩 전달하고 실패·정체 시 힌트를 준다. LeetCode의 별도 oracle로62/70 성공, 테스트:프롬프트 비율5:8.
- 27문제에서 같은 잘못된 코드를 반복했고 수동 개입이 필요했다. 테스트를 통과해도 최종 oracle에 실패한 사례가 있다.
- **한계:** 코드 먼저+같은 수준의 인간 개입 대조군이 없어88.5%를 TDD 개선효과로 부를 수 없다. 함수 수준이며 모델 snapshot·총 작업시간·비용도 부족하다.
- **재현:** [공식 자료](https://github.com/SanyogitaPiya/LLM4TDD)와 README 확보. 사람의 힌트 내용과 테스트 품질이 결과의 일부다.

## 참고 A11. TiCoder — 사람의 의도 확인은 유용하지만 다른 개입

Sarah Fakhoury 외 4인. *LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation*, IEEE TSE50(9):2254–2268; arXiv2404.10100v2, 2024-10-02. [원문 TableIII–IV, PDF pp.8/11](https://arxiv.org/html/2404.10100v2).

15명 사용자 실험에서는 테스트로 의도를 확인해 코드 판단 정확도와 인지부하를 개선했으나 시간 차이는 유의하지 않았다. 대규모 실험은100개 코드 후보·50개 테스트를 만들고 기준 구현이 모의 사용자로 답하여 후보를 제거/순위화한다. 따라서 초록의 큰 pass@1 개선은 **자율 에이전트의 엄격 TDD 효과나 단일 생성의 효율**이 아니다. [공식 코드](https://github.com/microsoft/TiCoder)와 README를 확보했다.

## 종합 해석에 필요한 경계

1. 테스트를 미리 본 이점, 실패를 실행으로 확인하는 이점, 작은 구현단위, 코드 구조 개선, 독립 오라클을 별개로 다뤄야 한다. 이를 분리하지 않은 논문 제목의 TDD를 엄격한 RED-GREEN-REFACTOR와 등치하면 과장된다.
2. 자기 테스트의 녹색은 자기일관성 증거일 수 있다. 새 기능의 기대행동은 요구사항·인간 확인·독립 평가에서 나오고, 기존 동작의 회귀검사는 repository 테스트에서 나온다.
3. repository-level이라는 명칭도 함수 완성, 버그패치, 전체 앱 생성으로 나뉜다. 크고 장기적인 제품 개발·팀 유지보수의 근거는 이 목록만으로 채워지지 않는다.
4. 테스트 작성 제한의 비유의한 해결률 차이는 테스트 무가치의 증명이 아니다. 반대로 테스트를 더 써서 특정 benchmark가 올랐다는 것은 총 비용이나 출시 후 품질의 개선 증명이 아니다.
5. 메타분석식 합산은 부적절하다. 비교조건·정보량·공개 테스트 여부·과제·모델·판정 기준의 차이가 효과크기 차이보다 크다.
