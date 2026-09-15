# F03 실행 결과와 HUMAN 판정

root 판정: **이번 범위 통과**. 두 PR이 하나의 공개 단위를 구성하며, 같은 release flag 아래 일반
OFF와 테스트 ON을 유지하고, 전체 완료 후 소스 수정 없이 설정으로 공개/중단했다. 모의 조건을 수락한
별도 정리 PR에서도 완성 동작과 기존 기능을 보존했다. 자동으로 오류를 막는 템플릿을 입증한 것은 아니다.

## 실제 대화와 수정

실제 Claude Code `claude-sonnet-5` / medium, 네 세션·다섯 턴이다. root가 HUMAN 역할로 각 결과를
읽고 다음 요청을 썼다. [1: 문서 제안](cli/turn-1.md), [2: HUMAN 리뷰 반영](cli/turn-2.md),
[3: 새 세션 PR1](cli/turn-3.md), [4: 새 세션 PR2](cli/turn-4.md), [5: 조건부 정리](cli/turn-5.md).
각 prompt·invocation·필터링한 tool I/O·실제 모델/사용량·export 해시는 같은 cli 폴더에 있다.

첫 spec@32d64b9에는 부분 TEST와 일반 공개의 혼동, 두 기능이 한 PR에서 끝난다는 잘못된 문구가
있었다. all=open+done 조건도 현재 데이터 계약과 범위 밖 입력 설명이 섞였고, cleanup은 계획 밖으로
밀려 있었다. root가 이를 짚고 모의 안정화 조건을 정했다. AGENT는 spec@f1ba82e → plan@5fc8bdc로
각각 수정·커밋·참조 갱신했다. root는 이 판들을 수락했다. 최초 작성의 자발적 완전 통과로 세지 않는다.

그 뒤 구현은 문서의 계획 범위를 따랐다. PR1/PR2/정리에서 파일·순서·공개 계약을 새로 바꿀 필요가
없어 매번 spec/plan을 형식적으로 수정하지 않았다. 두 문서의 중요한 개정은 구현 **전에** 검토됐다.
이 실행은 구현 중 새 요구의 동기화 검증을 추가로 한 사례가 아니다. 그 검증은 선행 0019/0022에 있다.

## 보존한 Git 흐름과 동작

| 단계 | 실제 판 | 관측 |
|---|---|---|
| 사용판 → 초기 제품 | f89a92a → f35b19e | 별도 초기 branch, 기존 3시험 PASS |
| 수정한 문서 수락·통합 | spec f1ba82e, plan 5fc8bdc; main 497db33 | HUMAN 수락 221298d, 문서만 통합 |
| PR1 목록 | 구현 85dc853; main 4c5bf2e | 일반 OFF·테스트 목록 ON·집계 없음. 실제 main 7시험, 독립 27관측 PASS |
| PR2 집계 | 구현 55394d9; main 2e2bd22 | 같은 제어·필터 재사용, 일반 OFF 유지. 실제 main 10시험, 독립 36관측 PASS |
| 모의 공개·중단 | 같은 main 2e2bd22 | 두 명령을 미설정→1→미설정, 6관측 PASS. HEAD·소스·데이터·clean 상태 불변 |
| 정리 PR | 구현 5786273; main f3126d1 | 최종 기능 기본 사용, 옛 설정 값 무관. 실제 main 8시험, 독립 36관측 PASS |

관측 원본: [PR1](pr1-observations.json), [PR2](pr2-observations.json),
[공개 결정](release-decision.md), [공개/중단](release-observations.json), [정리 후](cleanup-observations.json).
조회는 매번 파일 바이트를 대조했다. complete는 사본의 해당 상태를 바꾸고, 그 뒤 조회의 read-only와
최신 집계 반영을 확인했다. “모든 명령이 파일을 안 바꾼다”는 주장은 하지 않는다.

10→8시험은 R6의 수명 전환에 따라 OFF 거부 시험 두 개를 제거한 결과다. 완성 기능의 exact-match,
순서, 빈 결과, 집계, complete 이후 결과, 원본 보존과 기존 세 시험은 유지했다. 테스트 설정 보조 코드와
사용 안내에서 임시 변수 소비를 제거했고, 역사 spec/plan/결정·옛 branch는 보존했다.

maker Git에도 codex/exp-0023-base, -plan, -owner, -summary, -cleanup, -main refs를 로컬 fetch로
보존했다. 최종 main은 f3126d1470f97cb112afe13e04150549cb49aeb3이다. 초기 판에서 문서·PR1·PR2·
정리로 순차 파생했고 product main에 로컬 merge commit으로 통합했다. hosted PR을 만든 것은 아니다.

## 범위와 비용

CLI는 프로세스 운영자가 환경을 선택한다. 이 사실은 브라우저 사용자의 임의 설정으로 서버 기능을
열어도 된다는 의미가 아니다. 서버 대상 선별·인증 우회·백그라운드 효과·DB 호환·운영 배포는 미검증이다.
모의 안정화 조건도 실제 관측 기간을 대체하지 않는다. 정책은 이를 제품별 설계·시험 대상으로 남긴다.

Sonnet 다섯 턴의 CLI 보고 합계는 약 809.4초·$2.6745다(로컬 대기/검토 시간, Codex 사용량 제외).
Fable 설계 리뷰 두 턴은 약 424.8초·$4.0235였다. 실제 청구서가 아니라 CLI가 반환한 사용량 추정값이다.
새 상시 서비스·SDK·검증 엔진·설치 절차는 추가하지 않았다. 선택 예시를 실제로 읽은 실행이며
플러그인 자동 발견/native Skill 호출 성공률을 측정한 것은 아니다.

[독립 최종 검증](../reviews/verification/phase2.md)도 PR1·PR2·정리의 실제 동작과 Git 판을 확인해
중요한 불일치가 없다고 보고했다. 전체 시험 명령과 실제 출력은 그 옆 로그에 보존한다.
