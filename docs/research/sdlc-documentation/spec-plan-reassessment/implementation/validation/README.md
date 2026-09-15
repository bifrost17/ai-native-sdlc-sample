# 후보 정적·회귀 검증

기준 후보 `2d3f2dc`. 검사는 제품 구현 성공을 판정하지 않는다. 별도 활성 검사기/CI 규칙을 추가하지 않았다.

| 확인 | 결과와 근거 |
|---|---|
| 현재 후보/입력 SHA | [final-manifest.json](final-manifest.json): 38개 파일, 10개 Upstream 모두 Git 객체로 해소 |
| 상대 파일 링크 | 151개, 없는 대상 0개. 외부 링크의 현재 가용성을 검증한 수치는 아님 |
| Markdown 절 링크 | [anchor-check.json](anchor-check.json): 13개, 없는 anchor 0개 |
| 보존 대조 | c09b5f1 대비 F01/B01, M01 storage/operations/intent, TDD 스킬과 활성 templates/.claude/org-skills/검사/정책/북극성 무변경. F03·M01의 R/AC 본문 동일 |
| 외부 조사자료 | cfb0ec9에 보존한 exemplary-design-and-plans 원문/보고서 무변경 |
| PO 원 프롬프트 | 정책 검토 명령 후보의 영어 원문은 활성 명령과 축자 동일 |
| 스킬 형식 | [skill-format.json](skill-format.json): 4개 SKILL.md 모두 valid. 1500b16 이후 스킬 변경 없음 |
| 도식 | [도식 보고서](diagrams/validation-report.md): Mermaid 6개 구문/렌더 성공, 경계 초과 0, PNG 육안 검사. root도 W01 시퀀스/M01 구조를 확인 |
| 수정 후 도식 재사용 | [diagram-reuse-check.json](diagram-reuse-check.json): 문장 수정 뒤 6개 Mermaid 블록·12개 PNG/SVG 해시 동일. 과거 문서 전체 해시는 초기 렌더 판의 것으로 그대로 보존 |
| 기존 회귀 | [make-check.txt](make-check.txt): exit 0, Python 96개 중 기존 skip 1, hooks 28/28, eval fixture 8/8, managed-settings PASS |

`make check`는 1500b16에서 한 번 실행했다. 그 뒤 수정은 연구 문서뿐이며 실행 코드/시험/정책은 바뀌지 않아
동일 시험을 반복하지 않았다. 이 저장소에 make build/lint 타깃은 없고 CLAUDE.md가 정한 make check를 사용했다.
모델 기반 semantic eval, 제품 예시의 TDD/브라우저 실행, 후보 스킬 설치/자연 호출은 이 결과에 포함되지 않는다.

파일/링크/Upstream/보존 검사는 일회성 Python 표준 라이브러리 조회와 Git 대조다. 의미 판단은 독립 리뷰와
인계 대화에서 수행했다. 과거 r1 manifest·도식·make 출력은 덮어쓰지 않았고 최종 판 해시는 별도로 남겼다.
