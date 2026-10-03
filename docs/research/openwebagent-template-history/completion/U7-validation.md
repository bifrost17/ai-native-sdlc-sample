# U7 — 선택 훅의 제작 검증

2026-10-03 Asia/Seoul. root는 후속 사용자 결정에 따라 선택 Git 예시의 source 범위를 완료로 판정한다.
제작 기준 HEAD는 `8d5175efddc6875ffe6613725110a5f78a3dc1c7`이고, 이 기록과 함께 담긴 U7 변경이
대상이다. [초기 설계](U7-hook-design.md), [독립 리뷰 전문](U7-review.md), 현재 0028의 SP08/T12를
함께 읽는다. 최초 제안·결함을 최종 통과로 소급하지 않는다.

## 실제 변경과 중요한 복구

공통 예시에 Python 표준 라이브러리 검사와 작은 pre-commit 진입점을 추가했다. 기존 개발 세션이
의미를 검토하고 `SDLC_DOC_SYNC`에 snapshot과 필요한 문서 경로를 전달한다. 훅은 현재 대상과
선언한 포함만 확인한다. 파일명·개발건 경로를 하드코딩하지 않으며 Codex·Claude가 같은 파일을 쓴다.
팀 스킬/제품 설치가 hook을 자동 활성화하지 않는다. source 배포 후보는 0.1.9를 유지한다.

Astra/high 독립 리뷰는 두 P2를 재현했다. patch 표시 바이트 기반 지문은 diff 설정과 unstaged
attributes에 영향받았고, 시험은 global hooksPath·기본 브랜치를 상속했다. 첫 옵션 수정 후에도
attributes 영향이 남아, SP08을 HEAD+index 엔트리+실제 staged 변경 경로의 framing으로 바꿨다.
빈 파일의 intent-to-add와 실제 stage가 같은 엔트리를 갖는 반례도 변경 경로 집합으로 구별했다.
fixture 환경을 격리하고 브랜치를 명시했다. 초기 시험·복구 시험·독립 재검토를 모두 보존했다.

현재 independent probe는 표시/환경/attributes 변경 후에도 기존 신호로 commit 성공, intent-to-add
후 실제 추가의 옛 신호 차단·새 신호 성공, fake global hooksPath/signing/trunk/wrong index 아래 시험
성공을 확인했다. root는 현재 범위의 중요한 지적이 해결됐다고 판단한다. 작은 maker 문서/출처 정정도
반영했다. 리뷰는 수락·통합·완료 권한을 갖지 않는다.

## 실행한 확인과 원본

전체 출력·메타데이터는 저장소 아래 private 원본 경로에 보존한다. 새 자료를 U6 출력에 덮지 않았다.

| 확인 | 관측 | 전문 위치 |
|---|---|---|
| 실제 Git fixture 회귀 | 최종 13건 PASS. 최초 9건·첫 복구 10건의 출력도 유지 | `.local/research/openwebagent-template-history/completion/U7-worker-tests{,-followup,-final}.log` |
| make check | Python116건·1skip, hook28건, eval shell8건, managed-settings11키 PASS | `.local/research/openwebagent-template-history/20261003/completion/U7-make-check/` |
| 패키지 strict | Claude plugin/edition catalog/root catalog 3건 PASS. 모델 호출 없음 | 같은 completion의 `package-u7/results.json`과 각 log |
| Codex 전달 | 4patch dry-run/적용, 4skill frontmatter, 128 작성 링크·공통 기준 PASS | `package-u7/asset-hashes.json`, `results.json` |
| README 설치 명령 | 새 저장소 설치, 기존 hook/관리 경로 보존 중단, linked worktree 공통 경로 확인 | `U7-install-fixtures/results.json`·4개 log |
| 독립 재검토 | F1/F2·intent-to-add 복구 확인, 중요한 미해결 발견 없음 | `U7-review/`의 probe·stderr·해시와 공개 리뷰 전문 |
| 현재 source | U6와 별도 바이트 지문 | `U7-source-hashes.json` |

패키지/설치 안내의 검사는 최초 U7 source에서 실행했다. 이후 수정한 것은 지문 helper·fixture 시험·
그 계약 설명이며 설치 shell block·Codex patch 입력 skill·manifest/version은 그대로다. 해당 최초
확인을 새 모델 행동의 증거로 바꾸지 않는다. helper 최종판은 13개 실제 Git 시험과 fresh probe가
확인했다. source diff 공백 검사는 통과했다. U4 raw 리뷰의 기존 공백 경고는 보존한다.

## 남는 한계와 다음 범위

필수 목록을 잘못 정하거나 빈 목록을 거짓 선언하면 차단할 수 없다. 형식적인 문서 수정도 포함
검사만 통과할 수 있다. hook 미설치/제거·`--no-verify`, 검토 뒤 worktree만 변한 의미 영향, 동시
index 수정은 보장하지 않는다. 지문은 검토 인증서가 아니며 같은 HEAD/index에는 재사용 가능하다.
자동 stage·별도 모델·네트워크·영구 receipt 장부·새 승인 단계는 추가하지 않았다.

maker·제품·사용자 전역 설치는 활성화하지 않았다. 실제 에이전트의 읽기·의미 판단·실패 후 복구·
동반 문서 내용의 정확성은 위 Git fixture로 입증되지 않는다. 북극성 V4-11의 기존 부분 판정을 유지한다.
사용자의 새 OpenCode Muse Spark/xhigh 지시에 따른 실제 실행은 별도 0038로 관측한다. 그 한 사례로
기존 AC04의 전체 전후 비교나 두 도구의 실제 개발 통과를 대체하지 않는다.
