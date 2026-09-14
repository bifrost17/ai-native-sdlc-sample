# Plan: 공통 보완과 Muse Spark 부분 검증
Upstream: spec.md@4a855c7. Status: draft.
사용자의 구현·실험 요청을 현재 범위의 진행 허가로 사용한다.

## Files that change
- 양판 project/REVIEW.md, docs/PROCESS.md, examples/skills/design-spec/SKILL.md와 references/design-depth.md.
- 양판 org-skills의 sdlc-feedback, sdlc-verifier와 기존 OpenCode·선택형 Codex adapter.
- 패키지·루트/배포판 카탈로그와 설치 안내, 실행 후 관측 범위의 북극성 주석.
- docs/experiments/designs/spec-validation-muse/, 새 부분 실험 기록 및 별도 사용판·실험 브랜치.
원 설계 분석·외부 제품·고정된 역사 입력은 수정하지 않는다.

## Order of work
1. root가 제품 지침을, Astra/high가 feedback/verifier 및 adapter를 병행 보완한다. Sol/medium은 OpenCode 실행 환경을 확인한다.
2. 패키지를 기본형 0.1.10·선택형 0.1.6으로 맞추고 clean 설치·참조·기존 검증을 확인한다.
3. 제품 파일만 포함하는 선택형 사용판에서 사례별 저장소·브랜치를 파생한다. 원본/설치/모델/입력 판을 고정한다.
4. root HUMAN이 Muse Spark 1.3/xhigh를 실행하고 결과를 읽어 후속 답변을 제공한다. 원본 어려운 설계의 기준/개선 검토,
   작은 충분한 사례, 공유 계약·복구가 충분하고 내부/배포 상세만 이월된 사례를 우선한다.
   기본 총 5회·최대 6회/30분의 실험 agent 호출(위임 포함)을 예상하며 실제 runtime에 맞춘 명시적 조정은 실행 전에 기록한다.
   중요한 누락은 템플릿/실험설계/모델 판단 중 근거에 맞게 분류하고, 최소 수정 후 새 브랜치에서 영향 사례를 재시험한다.
5. 새 검토자가 실제 제작 diff와 증거를 검토한다. root가 부분 통과를 판단하고 결과와 한계를 주석에 연결해 로컬 main에 반영한다.
   제품 브랜치·원본 응답은 별도로 보존한다. 원격 push·운영 배포는 하지 않는다.

## Risks
부족한 입력이나 잘린 출력으로 기준 자체를 실패했다고 판단하지 않는다. 원본 과거 리뷰 언급의 노출 한계를 기록한다.
추가 질문마다 규칙을 만들지 않는다. fresh 설계 검토의 선택 활용이 구현 완료 fresh 검토를 대체하지 않아야 한다.

## Proof
문서/스킬 변경은 제품 TDD 실험을 꾸미지 않고 관련 make check와 설치·판별 대조로 회귀를 확인한다.
효과는 실제 CLI의 본문 읽기·발견·근거·이월 판단·결과 대기·HUMAN 후속 응답으로 평가한다.
모델 스스로의 PASS나 정적 검사로 행동 통과를 대신하지 않는다. 설치 자체와 자연 선택을 별도 기록한다.
상세 원본·프롬프트·응답·해시·브랜치·판정은 실행 기록에서 보존하고 계획 변경은 이유와 함께 이 문서에도 반영한다.
