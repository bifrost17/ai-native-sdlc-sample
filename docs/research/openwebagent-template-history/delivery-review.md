# PR·커밋 전달 정책 독립 검토

판정: **제안 판에서 중요한 설계 충돌·누락은 찾지 못했다. 실제 적용 효과는 미검증.** 이 검토는 사용자 허가로 추가한 전달 정책이 역사에서 확인된 보고 오류를 얼마나 직접 다루는지 본다. 정책의 존재를 과거 문제의 원인 증명이나 이후 PR 작성 성공으로 바꾸지 않는다. 제품·템플릿 수정, Git commit, 실제 PR 발행은 이 검토에서 하지 않았다.

## 검토 대상과 계약

제작 저장소의 미커밋 후보 `tdd-optional/project/docs/CHANGE-DELIVERY.md:1-49`, `.github/pull_request_template.md:1-17`, `docs/GIT-WORKFLOW.md:29-44,53-84`, `PROJECT-POLICY.md:17-19`, `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md:129-135`를 읽었다. 이 파일들은 배포 0.1.8의 기존 Git 절차와 구분해야 한다([기준판](baseline.md)). 0028 연구 chain의 `intent/0028-openwebagent-history-feedback/spec.md` FR06·FR07, SP05, AC06 및 `plan.md` T03b는 **간결한 PR/커밋 인계와 개발건 색인**, 기존 intent 경로 호환, 별도 승인·검사기 부재를 요구한다. 사용자 정책 요청이 이 WIP의 근거다. 기존 사용자 수락·머지 결정 권한을 PR 양식에 위임하지 않는다.

후보의 주 내용은 네 부분이다. (1) 목적과 실제 결과, (2) 이번 변경의 정본·base·의존 범위, (3) 실제 검증판·기대/관측·실패/미실행, (4) 남은 일과 인계. 커밋은 `type(scope): 결과`에 중요한 변경의 이유·관련 문서·실제 검증을 짧게 더한다. `type` 목록과 `!`/`BREAKING CHANGE:`는 팀 형식으로 제안하며 북극성 자체의 필수 양식으로 주장하지 않는다. 작은 오탈자에는 제목만으로 충분한 예외가 있다(`CHANGE-DELIVERY.md:29-46`). PR 기본 양식도 작은 정리의 단축을 허용한다. `changes/README.md`는 plan/PR/실행 원문을 복제하지 않는 현재 개발건 색인이다.

## 네 역사 사례와 맞는 판단

| 역사 관측 | 후보 문구가 주는 실제 판단 | 남는 경계 |
|---|---|---|
| [#272](https://github.com/bifrost17/openwebagent/pull/272)의 “모든 mutation 재킬” | [0001 사례](cases/0001-project-structure.md)의 `M:I/plan.md:274-279`에는 한 mutant 생존과 SIGTERM 미측정이 남는다. `CHANGE-DELIVERY.md:12-17`의 대상판·기대/관측·실패·미실행, `:20`의 최종 diff 정합을 적용하면 “모든” 대신 실제 판별 범위를 PR에 적어야 한다. | plan 기록과 API body snapshot의 모순은 확인했으나 원 mutation 로그·PR body 편집 시각을 재현하지 않았다. 이는 제품의 손실 재현 판정이 아니다. |
| [#471](https://github.com/bifrost17/openwebagent/pull/471)의 `SHOW TABLES` 되묻기 한계 | [0029 사례](cases/0029-text2sql-no-table-clarification.md)의 리뷰 수정 후 `727d56e:sql_tables.py:40-43`은 비조회에 `None`, `router.py:965-975`는 `[]`에만 422를 준다. 최종 본문의 행동 설명·한계가 코드/최신 spec과 일치해야 한다는 `CHANGE-DELIVERY.md:20`, `GIT-WORKFLOW.md:56-57`, `sdlc-feedback:132-135`가 바로 이 오기를 다룬다. | 정본 문구를 고치는 일은 리뷰/구현자가 실제 diff를 다시 읽어야 한다. 양식 설치만으로 자동 검출되지 않는다. 실행기의 별도 파서 거절 추정은 422 되묻기 증거가 아니다. |
| [#382](https://github.com/bifrost17/openwebagent/pull/382)의 변경 파일 설명 | 본문은 `CodexDesktopChat.svelte`를 안 바꿨다고 했으나 최종 main 머지 [`25c81e0`](https://github.com/bifrost17/openwebagent/commit/25c81e0bb1d8)의 diff는 그 파일 `:314-323,464-496`에서 scroll-follow 조건을 바꿨다([0018 후반 사례](cases/0018-followups-late.md)). `CHANGE-DELIVERY.md:9-10,20`의 **이번 diff**와 리뷰 뒤 재대조가 적용된다. | 그 설명이 어느 중간 판에서는 맞았는지는 현재 mutable body만으로 확정 못 한다. 본문 오류를 제품 결함과 혼동하지 않는다. |
| 열린 [#435](https://github.com/bifrost17/openwebagent/pull/435)의 대상 HEAD | 수집 API head는 `824332017802c7daa98bd4b29b8e7455b92aac12`인데 본문은 `2528f598…`를 “대상 HEAD”로 적는다([0018 후반 사례](cases/0018-followups-late.md)). `CHANGE-DELIVERY.md:13-17`은 실행판과 최신 결과의 연결을, `sdlc-feedback:132`는 리뷰 수정 뒤 PR 본문 갱신을 요구한다. Draft에서 다음 push/인계 때 대상과 시험 판을 다시 맞추는 것이 유용하다. | 오래된 본문 수치가 R의 실제 제품 결과를 대표한다고 보지 않는다. #435 자체는 미병합·미완료이고, 새 정책으로 완료 상태가 바뀌지 않는다. |

## 비례성과 정본 검토

정책은 작은 수정의 목적·변경·확인만 남기는 예외를 명시하고, 커밋 본문도 중요한 동작/설계/계획 변경에만 길게 요구한다. `CHANGE-DELIVERY.md:21-25,29-46`은 상세 시험 출력의 복제, 무관한 위험 채우기, commitlint·hook·고정 글자 수·자동 릴리스를 피한다. `.github/pull_request_template.md`의 네 머리는 짧은 PR에서 줄이거나 해당 없음으로 처리할 수 있다. 새 승인 단계는 없다. 이 비례성은 0028 AC06과 맞는다.

`GIT-WORKFLOW.md`의 기존 단계 수락·영향 문서 갱신·실제 diff 대조·머지 뒤 검증을 대체하지 않고 PR/커밋 표현을 연결한다. `changes/README.md`의 현재 행은 plan의 요약·대상 코드판·PR과 다음 작업을 찾는 색인이며 각 시험 출력의 두 번째 장부가 아니다. 의미 있는 인도/중단/머지 때만 갱신하고 단순 질문이나 모든 미세 커밋에 상태 변경을 요구하지 않는다. 이 설계는 0018의 낡은 plan 머리와 0029·0030의 “머지 대기” 문구를 **찾기 쉽게** 할 수 있으나, 누가 실제로 현행 판을 확인해 행을 고치는지가 여전히 중요하다. 보존된 역사 spec은 새 변경의 현재 정본이 아니라 당시 결정 기록이라는 `GIT-WORKFLOW.md:32-33`과 스킬 `:134-135`의 문구는 0011→0017 탐색기 계약 대체, 0003→0014 ms 단위 정정처럼 실제 사례에 맞는다. 현재 코드를 무조건 옳은 계약으로 승격하지 말라는 마지막 문장도 필요하다.

링크·범위의 정적 확인은 통과했다. PR 양식은 전달 문서로, Git 정책은 양식·changes 색인으로, `PROJECT-POLICY.md`는 전달 정책으로 연결한다. `git diff --check`는 수정된 정책 세 파일에서 문제를 보고하지 않았다. **문서와 link의 정적 검토**일 뿐 새 프로젝트 설치, 실제 GitHub PR 양식 표시, 커밋 작성, 새 문맥 인계 또는 실제 PR 리뷰 효과의 PASS가 아니다. 사용자 요구의 실험은 0028 plan T04의 별도 결과로 판단해야 한다. 이 전달 정책 때문에 현재 검토 범위에서 추가 문서·자동 검사·승인 규칙을 제안하지 않는다.
