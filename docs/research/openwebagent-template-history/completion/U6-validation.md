# U6 패키지와 전체 회귀 기록

2026-10-03 Asia/Seoul. source 기준 `df3ae99c3ba9bab5b656a0761aa52ba7a733bb79`.
maker plan의 현재 인계 기록은 후속 미커밋 문서 개정이며 제품 source는 같은 바이트다.
실제 제품 개발·모델 CLI 실행·전역 설치·배포와 구분하는 제작 검증이다.

## 패키지 확인

root가 private 실행 자료의 `completion/verify_package.py`를 실행했다. 최종 exit 0.
전체 명령·출력·설치판 파일 해시는 다음 경로에 보존한다.

`.local/research/openwebagent-template-history/20261003/completion/package/`

- `results.json`: argv·cwd·exit code·출력 파일 해시와 실제 source SHA.
- `asset-hashes.json`: 원본과 임시 설치본의 전체 스킬 동반 파일 해시.
- `versions.json`: root/배포판 catalog와 plugin의 0.1.9 일치.
- `claude-strict-*.log`: 별도 `CLAUDE_CONFIG_DIR`에서 플러그인·두 catalog strict 검증 3건 exit 0.
- `codex-*-{dry-run,apply}.log`: explicit-only, feedback, ux-copy, pr-loop 순차 dry-run/적용 모두 exit 0.
- `skill-frontmatter-*.log`: Codex 복사본의 작성 스킬 3개와 feedback quick_validate 모두 exit 0.

Claude 작성 스킬은 전체 폴더가 source와 같은 바이트다. Codex에는 팀 13개와 작성 3개를 복사하고
네 patch·verifier TOML·AGENTS 예시를 적용했다. 작성 본문은 명시 호출 frontmatter 변환 외 동일하며
참고 자료가 빠지지 않았다. 실제 설치 위치의 작성 링크128개와 네 명시 호출 정책을 확인했다.
공통 verifier 기준은 Codex의 명시된 AGENTS 진입 안내 추가만 정규화하면 같은 전문이다.
플러그인 등록/사용자 캐시 갱신·모델 호출은 하지 않았다. Claude 실행기 판은 로컬 `2.1.285`다.

## 최초 검사 오류 보존

첫 시도에서 strict 3건과 네 patch는 통과했지만 quick_validate에 필요한 PyYAML이 없었고,
private 비교 절차가 이미 명시된 Codex AGENTS 안내 차이를 허용하지 않아 실패했다.
`package-attempt-1/`의 전문 로그를 보존했다. source 결함으로 판단하지 않고 private 환경·비교를
수정했다. validator 의존성은 같은 .local 아래 격리 환경에 설치했고 제품·전역 환경은 바꾸지 않았다.
수정된 private 절차로 같은 source를 다시 확인한 결과 위 검사가 통과했다. 최초 기록은 덮어쓰지 않았다.

## 최종 확인

새 verifier의 [전문](U6-review.md)을 원 응답 그대로 저장했다. 현재판 make check exit 0:
Python103건(1skip), hooks28/0, eval shell8/0, managed-settings PASS. 예상 bad input hook은 exit2로
차단했고 이전0027의 자체 diff도 plan과 대조했다. plan 경로 인계 누락은 후속 복구·재검토에서 해결됐다.
원격 fetch·최신 main 통합 검사는 하지 않았다. 검사·도구 실패/교정·전문과 한계는 리뷰 원문에 있다.
제품 효과 AC04, 실제 개발 실험, main 통합·배포·기존 설치 업그레이드는 이 결과에 포함하지 않는다.

## 중간 발견과 수정

verifier가 제작 plan의 Files that change에 실제 경로가 부족해 양방향 대조가 어려운 누락을 발견했다.
root는 원 후보 27개 source 경로와 이번 순차 정리 10개 경로를 실제 작업·설계·방법에 연결하고,
읽기/검증 입력과 수정 파일을 구분했다. 수정 전 plan은 private `completion/plan-before-u6-findings.md`에
보존했다. 이는 후속 문서 복구이며 최초 계획부터 충분했다고 소급하지 않는다. 좁은 재검토를 요청했다.

U4 리뷰의 원문 인용에 들어간 상대 링크는 source 위치 기준이다. completion 폴더에서 따라갈 수 있는
대상은 [제품 개발건 색인](../../../../tdd-optional/project/changes/README.md)이다. 리뷰 전문·raw diff는
그대로 보존한다. 전체 diff 공백 검사는 raw diff의 context 공백/EOF 경고로 nonzero이며, 배포 source의
공백 검사 통과와 구분한다.
