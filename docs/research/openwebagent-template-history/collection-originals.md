# 원문 수집물 보존 상태 감사

이 문서는 `bifrost17/openwebagent` 이력 수집의 API 응답, Git 객체 저장소, 추출본과 파생 색인을 구분하고 2026-10-03 현재 로컬 보존 상태를 기록한다. 조사는 기존 파일의 범위·SHA·ref를 확인하는 작업이었다. 제품 코드나 실험은 실행하지 않았다. API 본문이나 대화 원문은 여기에 복사하지 않는다.

조사 전문, 독립 검토자 응답·보고서 snapshot, 웹 조사 응답 및 source-review 도구 기록은 [원본 보존 안내](originals.md)와 그 manifest에 별도 보관한다. 그것들은 이 문서가 다루는 GitHub API/Git 원문 archive와 다른 자료 계층이다. 어느 한쪽도 빠진 Git object, 전체 PR comment stream, 비보존된 제품 실행 로그를 대신하지 않는다.

## 판정

현재 보존본은 페이지가 모두 수집된 API JSON과 선택된 추출본, 그리고 일부 Git 객체를 가진 partial clone이다. 전체 원문 archive라고 부를 수 없다. 원 `manifest.json`은 99개 파일이 보존됐다고 기록하지만, 현재 감사에서 그중 53개만 크기와 SHA-256이 일치했고, Git cache 아래 45개 경로는 사라졌으며 1개는 해시가 달랐다. 25개 API 파일은 모두 manifest와 일치했다. 원 manifest는 수정하지 않았다.

Git clone은 `blob:none` 필터와 promisor remote를 쓰며 shallow clone은 아니다. 현재 refs에서 29,145개 commit에 도달할 수 있고, 114개 branch ref와 2개 tag가 있다. main은 `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. 다만 `GIT_NO_LAZY_FETCH=1 git rev-list --objects --all --missing=print`에서 73,949개 object가 로컬에 없었다. 이 수를 모두 blob이라고 단정하지 않는다. commit 그래프를 읽을 수 있다는 사실은 모든 commit의 파일 내용·PR diff·시험·로그가 저장됐다는 뜻이 아니다.

그 시점의 mutable Git cache를 읽기 전용으로 tar/gzip snapshot해 [별도 감사 manifest](../../../.local/research/openwebagent-template-history/20261003/collection/audit/preservation-audit.json)에 기록했다. archive는 147,054,436 bytes, SHA-256 `0c7f98702faa0774b0f369fd2a49c6897e613f8608df14be3982fe3c535ec3e6`이다. [snapshot 파일](../../../.local/research/openwebagent-template-history/20261003/collection/audit/remote.git-observed-20261003.tar.gz)은 이 시점의 143 MiB cache를 고정한 것이며 빠진 promisor object를 다시 받거나 완전한 Git archive로 변환하지 않는다. 원 `collection/manifest.json`의 99개 파일 선언은 초기 기록으로 보존했으며 현재 cache를 검증하는 증거로 재사용하지 않는다.

## 원문 API와 파생 데이터

| 수집물 | 현재 범위 | 보존 판정과 한계 |
|---|---:|---|
| Pull Requests API 목록 | 4 pages: 100/100/100/40, 총 340건 | JSON 전체 페이지를 저장했고 25개 API 파일 검증에서 해시가 일치했다. raw 응답 본문에는 비공개 저장소 정보와 개인 정보가 있을 수 있어 이 보고서에는 본문을 재인쇄하지 않는다. |
| Issues API 목록 | 5 pages: 100/100/100/100/75, 총 475건 | 페이지 집합을 보존했다. Issue/PR metadata 목록은 댓글·이벤트 전체 archive와 다르다. |
| Branch API 목록 | 2 pages: 100/14, 총 114개 | PR, issue와 같은 수집 snapshot 시점의 branch metadata다. branch ref의 모든 파일 blob이 cache에 있다는 증거는 아니다. |
| Repo metadata와 main commit | 각 1개 | repository 응답과 `main@a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e` 응답을 저장했다. HTTP response headers, request IDs, rate-limit headers는 보존하지 않았다. |
| PR detail export | 340개 PR key | `changed_paths`, `checks`, `reviews`와 head 정보의 상세 추출이다. 모든 GitHub 댓글·inline review·commit/status/check-run endpoint를 재귀 수집한 것은 아니다. |
| 선택 PR comment/commit/status | 채택 뒤 미매핑 PR 5건 | #268/#301/#326/#363/#404의 commit, issue-comment, review-comment 응답과 선택 commit status를 저장했다. 이 다섯 건의 캡처를 나머지 PR의 대화 archive로 일반화하지 않는다. |

기존 [수집 manifest](../../../.local/research/openwebagent-template-history/20261003/collection/manifest.json)는 초기 파일별 크기와 SHA-256 기준이다. API 파일별 경로와 SHA-256은 그 manifest와 별도 [보존 감사 manifest](../../../.local/research/openwebagent-template-history/20261003/collection/audit/preservation-audit.json)에서 확인할 수 있다. `.local` 경로의 보존 파일은 private research artifact로 취급한다.

`inventory.json`, `scope.json`, `curated-scope-adjudication.json`, `git/intent-history.txt`, `git/branch-intent-roots.json`은 분류·교차연결·이력 추출을 한 파생물이다. 유용한 lookup 자료지만 API 원문이나 모든 Git tree/blob을 대신하지 않는다. 이번 보고서의 요약 행이나 case 보고서 역시 원문 PR 기록과 구분한다.

## Git과 현재 소스 인덱스의 확인 경계

기존 cache는 `blob:none` partial clone으로 현재 refs 및 접근 가능한 commit graph를 유지한다. 측정 당시 branch refs 114개와 tag 2개, main SHA는 Git ref에서 확인됐다. pack 단위 파일 목록은 manifest 작성 시점 이후 바뀌었다. `objects/info/packs`의 manifest상 SHA-256은 `7570cb3edb35a57ce92cfc2ca8db87c3e76ea69194a1435e05f7a65011ff3b6f`, 재검사 SHA-256은 `6bf386f42eb5d9b1c35630e170208454b6252c222074ad616a15d8ad82e19986`였다. 그에 따라 45개의 과거 pack/index/promisor 경로가 현재는 없었다. 이 변경 원인과 각 object가 언제 어떤 경로로 fetch/repack됐는지는 확정하지 않는다.

case 분석 source-index는 `analysis/<case>/` 아래에 둔다. 0009에는 별도 source-index가 없고 `analysis/0009/intent.md` 추출본만 있다. 0009 보고서의 현재 main 참조 중 표본 세 개를 local cache에 lazy-fetch 없이 조회하고 SHA-256으로 대조했다. `intent/0009-worktree-codex-home-volume-isolation/intent.md`는 Git blob `4a17ea4569c4917f4e3605c449fc235c5318447d`, 3,464 bytes, SHA-256 `9d2eda47a1faf8531af47f80a13b90f04f30415bbe22287c43d598e47dec4e4e`다. 추출본의 SHA-256도 같아 해당 추출본 내용이 원 Git blob과 일치한다. 첫 추가 commit은 `535af674b5b734ebe49d378ad3b133f6804d1edf`다.

같은 frozen main tree에서 case report가 인용한 `deploy/docker-compose.wt.yml`(6,241 bytes, SHA-256 `59415cfd2662bfdf1b05499a16ead36db14dba691676ac065f85d1d68ee674b1`)과 `orchestrator/orchestrator/app.py`(256,499 bytes, SHA-256 `b285410e201e8dd33175383cd4c84c0baf434d122862ac1445c801de62b6b4ee`)의 선택 blob도 읽을 수 있었고 값은 감사 manifest에 기록했다. 이는 표본 source target의 존재 증거다. 모든 analysis source-index 대상이나 모든 역사판이 로컬에 있다는 뜻은 아니다.

## 0009: intent와 작업 산출물을 분리

0009는 “intent가 없다”는 사례가 아니다. inventory와 Git 이력에서 `intent/0009-worktree-codex-home-volume-isolation/intent.md`가 존재하며, 2026-09-22의 `535af674b5b734ebe49d378ad3b133f6804d1edf` commit에서 새로 추가된 점과 current main blob을 확인했다.

그와 별개로, 조사 당시 수집 inventory 및 case report에서 0009에 독립 spec·plan·구현 PR·시험은 확인되지 않았다. #324는 0008 T03–T08 작업으로 연결되고, 그 PR 안에 0009 intent를 추가한 사실만으로 0009 구현으로 세지 않았다. case report는 실제 충돌 사고와 두 레인의 동시 실행도 확인하지 않았다고 명시한다. 따라서 [coverage 행](coverage.md)에는 “intent 존재, 별도 spec/plan/구현 이력은 확인되지 않음”으로 적었다. 이는 접근 가능한 수집판의 결론이지 다른 곳의 비공개 작업이 절대로 없었다는 증명은 아니다.

## 남은 원문 공백

- partial clone에서 보이지 않는 73,949 objects와 cache manifest의 불일치 때문에 전 branch·전 commit의 파일 내용을 완전 보존했다고 주장할 수 없다. Git cache snapshot도 누락 객체를 포함하지 않는다.
- 모든 340 PR에 대한 raw commits, review conversations, inline comments, issue comments, statuses/check-runs의 endpoint별 완전 수집은 없다. 다섯 미매핑 PR의 상세 댓글 수집은 범위를 명시해 제한적으로만 사용한다.
- GitHub 페이지 본문은 보존됐지만 HTTP headers나 수집 transport 기록은 없다. 시간 경과에 따른 이후 GitHub 변경도 이 날짜 snapshot에는 반영되지 않는다.
- 0009의 intent 및 선택된 현재 소스 파일은 blob hash를 검증했다. 그 범위가 0009에 관한 모든 historical file version이나 실행 기록을 대체하지 않으며 analysis source-index 전량을 검증한 것도 아니다.
- 이 보존 감사는 제품을 설치·수정·실행하지 않았다. missing blobs 재수집, 사건 재현, 시험·브라우저/런타임 확인은 범위에 포함하지 않는다.
