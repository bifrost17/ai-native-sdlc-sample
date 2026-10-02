# 조사 전문과 원본 자료 보존

사용자의 “요약본 아닌 원문으로 저장” 요청에 따라 조사자가 작성한 분석·리뷰 전문과 수집 출처 원문을
각각 보존한다. [README](README.md)와 [보완안](recommendations.md)은 찾기 위한 안내이며 원문을 대신하지 않는다.

## 조사자가 작성한 전문

- [개발건 색인](coverage.md)의 각 링크는 사건 사슬, 당시 지침, 코드·시험·리뷰와 후속 변경,
  원인 판단, 현행판 대조, 근거 부족을 담은 전체 보고서다. `cases/` 아래에 번호30건과 무번호4건의
  보고서 및 0018의 middle·late·authority 후속 보고서를 저장한다.
- [설계 방법 조사](design-methods.md)와 [기록 정책 설계](change-records-design.md)는 원전별 읽은 범위,
  적용 추론, 반론, 한계를 포함한 조사 전문이다. 외부 페이지 원문은 아래 수집 자료에 별도로 둔다.
- [후보 검토](candidate-review.md), [설계 검토](design-review.md), [전달 검토](delivery-review.md),
  [source 검토](source-review.md), [결론 검토](conclusion-review.md)는 독립 검토 내용을 담은 전문이다.
  source 검토 본문은 검토자가 제출한 Markdown 본문을 그대로 추출했다. 보존 당시의 미추적·실험 중단 등
  표현은 그 시점의 기록이며 이후 Git 인도 상태를 소급해 덮어쓰지 않는다.

## 원본 보관소

저장소 아래의 `.local/research/openwebagent-template-history/20261003/`를 사용한다.
이 경로는 Git에서 제외되므로 연구 문서의 커밋·푸시가 원본 보관소까지 전송하지는 않는다.

| 위치 | 보존 내용 | 전문·원문의 의미와 한계 |
|---|---|---|
| `collection/` | GitHub API의 PR·브랜치·이슈·댓글/검토·커밋·diff 수집 응답과 Git 자료 | 당시 수집 응답을 보존한다. API의 과거 편집판까지 복원한 것은 아니다. Git mirror의 부분 clone과 이후 cache 변화는 [수집 감사](collection-originals.md)에서 구분한다. |
| `analysis/<case>/` | 읽은 코드·문서·diff·PR 자료와 사건별 source index/manifest | 저장된 추출본과 읽은 범위를 기록한다. 모든 제품 파일을 읽거나 추출했다고 주장하지 않는다. |
| `research-methods/` | 공식 외부 출처의 HTML, 질의·열람·접근 실패와 manifest | 저장에 성공한 응답의 원문이다. 공개 미리보기·접근 실패·웹 열람만 가능한 자료의 한계를 그대로 남긴다. |
| `baseline/`, `start/` | 기준 SHA, 처음의 미커밋 후보·patch·해시, 패키지 검사 출력 | 당시 기준판과 제작 중 변경을 분리한다. |
| `originals/agent-responses/` | 이 조사에 참여한 에이전트의 최종 응답·공개 진행 응답 전문 | 응답 텍스트를 줄이거나 다시 쓰지 않는다. 세션 ID·행·byte offset·시각·SHA-256을 manifest에 연결한다. 내부 추론이나 무관한 대화는 보관 대상이 아니다. |
| `originals/documents/<sha256>/` | 보고서와 로컬 리뷰의 바이트 단위 스냅샷 | 내용이 달라지면 새 해시의 파일로 보존한다. 원본 스냅샷을 덮어쓰지 않는다. |
| `originals/tool-records/` | 원전 조사·source 검토자의 도구 호출·응답 원문 값 | 웹 도구의 열람 응답과 source 검사 출력을 포함한다. 도구가 당시 잘라 반환한 부분은 복원하지 않고 잘림 표시를 유지한다. |
| `reviews/` | 후속 보존·링크 검토 전문 | 예: `archive-links-review.md`. 공개 보고서와 함께 해시 스냅샷을 남긴다. |
| `runtime/` | 중단 전 준비 자료, 입력·프롬프트·응답·실행 로그·브랜치/설치 해시 | [0037](../../experiments/0037-openwebagent-history-feedback.md)의 실패·부분 실행·중단 기록이다. 완료된 비교 실험의 증거가 아니다. |

## 재작성과 요약의 구분

조사 보고서는 출처를 분석한 저술이며 외부 원문의 전재가 아니다. 반대로 수집 API·HTML·Git 추출본을
보고서의 요약으로 대체하지 않는다. 두 자료를 source index와 SHA로 연결한다. 원문이 없으면 근거 부족으로
남기며 브랜치명·계획된 모델·같은 커밋만으로 실행 순서와 환경을 보충하지 않는다.

`originals/manifest-<UTC시각>.json`에는 원문 응답·보고서 스냅샷의 위치, 길이, SHA-256, 출처와 추출 방법을
기록한다. 갱신 때 새 manifest를 만들고 이전 것은 유지한다. Markdown fence를 제거한 source 검토 본문은
별도 `review-body/`에 두며, 전체 응답은 `agent-responses/`에도 남긴다. 공개 `source-review.md`와 추출 본문의
바이트가 일치하는지 확인한다.

최종 보존 시점의 manifest 위치·해시·개수는 [보존 색인](originals-index.json)에 연결한다. source 검토에서
당시 세션에만 있었다고 기록한 검사 출력도 이번 후속 보존에서 `tool-records/`로 추출했다. 원전의 일부
페이지처럼 HTML을 직접 받지 못한 경우, 웹 열람 도구가 반환한 자료와 실패 응답을 구별해서 보존하며
열람 응답을 완전한 외부 페이지 원문으로 부르지 않는다.

확보하지 못한 Windows 대화, 일부 원 실행 로그, Git mirror에서 받지 않은 제품 blob은 원문 보존을
완료한 대상으로 세지 않는다. 조사 전문과 수집 원문의 파일 보존, 조사 coverage, 제품 실행 검증은 각각
다른 사실이다. 추가 개발 실험은 별도 사용자 지시 전 실행하지 않는다.
