# 0024 북극성 HTML closing review

최종 판정은 **관측한 0024 범위 PASS**다. 마지막 「최종 r02b·통합·HTML 재검사」 절을 현재 결과로 읽는다.
아래 최초 정적 검토와 96c0043 검토는 당시 판정·미해결 사항을 보존한 중간 기록이다.
maker e0657c9의 make check(96시험, 기존 skip1, hooks28, eval fixture8, managed settings)와
원 실행/r01의 독립 검토 원문은 `codex/experiment-2026-09-11-f04-r01:raw/closing-first-runs.md`,
전체 검사 출력은 같은 ref의 `raw/maker-check-e0657c9.txt`에 보존했다.

2026-09-11. 비교 기준은 maker `e0657c999fbb805f8edbdc380dc5ab40fcb49e0d`의
`docs/verification/north-star-playbook.html`이다. 이 1차 정적 검토는 root가 추가한 아홉 개
`0024` 주석만 대상으로 한다. 진행 중인 r02와 이후 추가 예정인 V4-11/V6-04/V6-06은 아직
읽거나 판정하지 않았다.

판정: **요청한 아홉 주석의 정적 구조와 보존 조건은 PASS.** r02 이후 세 주석이 추가되면 같은
검사를 좁게 다시 적용해야 하므로, 이 문서는 전체 closing 완료 판정이 아니다.

## 실행한 검사

Python read-only 검사에서 현재 파일과
`git show e0657c9:docs/verification/north-star-playbook.html`을 읽었다. 현재 파일을 줄 단위로
순회하며 활성 `<details class="verify ..." open id="...">`를 추적하고, 정확히
`<p><b>0024`로 시작하는 줄만 제거한 byte string을 기준 원문과 비교했다. 같은 검사에서
검증 블록의 `(id, class, summary의 판정)` tuple, 중복 ID, 새 주석의 상대 링크 해소를 확인했다.

결과:

```text
base_bytes 1272792
current_bytes 1278357
new_0024_count 9
new_0024_ids V3-01,V3-09,V4-06,V4-08,V6-05,V7-09,V8-02,V8-09,V10-05
expected_ids_match True
base_equal_after_removal True
base_details_count 179
current_details_count 179
details_tuples_equal True
duplicate_ids []
local_link_count 9
missing_local_links 0
```

바이트 비교 해시는 다음과 같이 같다.

```text
base_sha256=04945f0ebaa80d5ca58f9b2c8c0df9d0175b91cb6eae4e50bba37b1a4eeec707
stripped_current_sha256=04945f0ebaa80d5ca58f9b2c8c0df9d0175b91cb6eae4e50bba37b1a4eeec707
```

아홉 줄 모두 `<p>...</p>` 한 쌍과 `<a ...>...</a>` 한 쌍을 가지며 해당 verify body의 닫힘
앞에 있다. 따라서 새 주석 밖 원 플레이북 bytes, 기존 주석, 기존 ID, class/판정, 본문에 있던
카운트는 바뀌지 않았다. 검증 블록 수도 179개로 유지됐다.

## 새 주석과 대상 블록

| 대상 ID | 새 문단 제목 | 상대 링크 |
|---|---|---|
| V3-01 | 0024 활성화와 실제 정책 적용 | `../experiments/0024-spec-plan-activation.md` |
| V3-09 | 0024 HUMAN 검토와 개정 | 같은 파일 |
| V4-06 | 0024 구체적인 실행 계획 | 같은 파일 |
| V4-08 | 0024 새 구현 문맥 | 같은 파일 |
| V6-05 | 0024 영구 설치와 선택 예시 | 같은 파일 |
| V7-09 | 0024 독립 검토의 관측과 오류 | 같은 파일 |
| V8-02 | 0024 loop와 마지막 검토 | 같은 파일 |
| V8-09 | 0024 실제 통합 판과 인도 | 같은 파일 |
| V10-05 | 0024 현재 합의와 실제 diff | 같은 파일 |

아홉 링크 모두 현재
`docs/experiments/0024-spec-plan-activation.md`로 해소되고 파일이 존재한다. 링크의 대상 내용은
root가 closing 기록을 작성 중인 별도 산출물이므로 이 정적 링크 검사에서 사실 판정하지 않았다.

## r02 뒤 재검사

root가 V4-11/V6-04/V6-06 주석을 추가했다고 알리면 다음 조건만 다시 검사한다.

1. `0024` 문단이 기존 아홉 개와 새 세 개, 총 12개인지와 대상 ID 순서.
2. 12개 문단을 제거한 결과가 위 기준 SHA256과 byte-identical인지.
3. 기존 179개 검증 블록의 ID/class/판정 tuple과 중복 없음이 유지되는지.
4. 새 세 문단의 `<p>`/`<a>` 구조와 모든 로컬 링크가 실제 파일로 해소되는지.
5. 새 세 문단의 사실 주장이 완료된 r02 공개 근거와 일치하고, 원 실행·r01·r02의 결과를 섞지 않는지.

## r02 독립 검토 — `fe61fe7..96c0043`

판정: **관측한 r02 경계에서 AC5는 PASS.** 원 실행 T07과 r01에서 각각 plan과 구현이 서로
다른 커밋이었던 실패를 되풀이하지 않았다. 다만 `96c0043` 시점 문서에는 HUMAN 최종 수락 전에
고쳐야 할 현재성 불일치 두 건이 있어, 이 판정만으로 전체 0024 closing을 완료할 수는 없다.

### 실제 실행과 커밋 경계

완료된 r02 공개 이벤트를 결과 요약과 분리해 확인했다. 구현 전에 `sdlc-feedback`, `tdd`,
`brand`, `data-compliance` Skill이 실제로 호출됐고, intent는 `7d32d1a`, 최초 spec은
`38694b6`에 각각 커밋됐다. plan 편집 뒤 테스트 파일을 먼저 고쳤으며, 실제 명령 출력은
`test_summary_json_object_counts`에서 `unrecognized arguments: --json`과 함께 3개 중 1개
실패, 종료 코드 1을 기록했다. 그 뒤 `tracker.py`를 편집하자 같은 3개 테스트가 통과했고,
release-control 6개와 당시 전체 15개 테스트도 통과했다.

`dc05fc0`에는 plan, `tracker.py`, summary/release 테스트, `USAGE.md`가 함께 들어 있다. 따라서
계획 변경과 그 계획을 구현한 diff가 같은 커밋에 있어 AC5의 핵심 요구를 자연 실행에서 충족한다.
이는 원 T07의 `efa6a5b`/`fb6e374`, r01의 `ac1674b`/`2e1e4ed` 분리를 바로잡은 직접 증거다.

native Agent 검토도 실제로 실행됐다. 검토자는 당시 execution 근거 누락, plan의 R1–R5와
AC1–AC7 범위 및 release P0–P4 잔존, R6 실패 경로의 수락 조건·테스트 누락을 찾았다. parent는
추가 HUMAN 힌트 없이 execution 근거 `b4c0863`, spec AC10 `e18a807`, plan 범위와 실패 테스트를
보완했다. 새 테스트 두 개가 먼저 통과했고, 전체 17개도 통과했으며, 세 mutation check가 각각
`list --json`, JSON 오류 stdout, open count 회귀를 잡았다. 후속 plan·테스트·결정·실행 문서는
`96c0043`에 함께 커밋됐다. 검토 당시 `dc05fc0`에 execution 기록이 없었다는 지적은
`b4c0863` 이후의 현재 결함으로 재사용하지 않았다.

이 결과는 r02가 대상으로 삼은 흐름에서 계획과 구현의 same-commit 조건이 작동했다는
표적 증거다. 보편적인 무결성이나 전체 실험 체인의 무결점을 뜻하지 않는다. 특히 두 앞선 실행은
그대로 실패이며, 뒤의 HUMAN 복구가 그 실행들을 소급해 PASS로 만들지 않는다.

### `96c0043`에서 발견한 문서 불일치

1. `plan.md`의 헤더는 `Upstream: spec.md@38694b6`으로 남아 있지만 현재 수락 조건 AC10을
   도입한 spec은 `e18a807`이다. 본문은 이미 AC10과 P5를 참조하므로 헤더가 현재 계보와
   충돌한다.
2. `plan.md`의 `이 PR의 유일한 RED`라는 문구는 뒤에 실제 JSON RED가 추가된 현재 문서에는
   맞지 않는다. 최초 text-summary 단계로 범위를 제한해야 한다.

두 항목은 r02의 자율 검토 성공을 부정하지 않지만, 최종 HUMAN 수락 입력으로 쓰는 plan의
정확성을 막는다. root가 요청한 r02b 수정은 명시적인 HUMAN 복구로 기록해야 하며, 이를 native
reviewer가 자율적으로 해결한 것으로 세면 안 된다. `execution.md` 끝의 추가 빈 줄 때문에
`git diff --check fe61fe7..96c0043`가 종료 코드 2를 낸 점도 사소한 기계적 한계로 남는다.
`decisions.md`의 생성 커밋 요약이 `b4c0863`과 `96c0043`을 열거하지 않는 점은 execution의 상세
기록으로 보완되지만 현재 최종 상태 요약으로는 덜 완전하다. plan 5단계의 P0–P4 표기는 뒤의
JSON 확장 단계가 P5를 별도로 정의하므로 역사적 단계 설명으로 해석할 수 있다.

### closing 전에 남은 조건

HUMAN은 Q-json-1/2의 가정을 답하고, r2 정책의 권한·출처를 확인한 뒤 intent `7d32d1a`, spec
`e18a807`, 수정된 최종 plan을 명시적으로 수락해야 한다. 위 두 plan 문구 수정과 그 커밋을
확인한 다음 local merge, 최종 17개 테스트와 50개 root 관측을 독립 확인해야 한다. 원 T06의
역사적 RED→GREEN 증거는 원 실행 raw가 소유하며, 상속된 baseline에 그 실행 절이 없다는 사실을
r02의 새 결함으로 계산하지 않는다. maker source와 fixture의 `make check`는 이 좁은 r02 검토에서
다시 실행하지 않았다.

## 최종 r02b·통합·HTML 재검사

2026-09-11. 이 절은 위의 `96c0043` 중간 판정을 최종 HUMAN 복구와 통합 판까지 좁게
연장한다. 판정은 **관측한 0024 범위에서 PASS**다. 원 T07과 r01의 same-commit 실패는 그대로
남고, r02의 자연 실행 성공과 마지막 HUMAN 참조 정정을 서로 다른 사건으로 기록한다.

### HUMAN 복구와 제품 통합

`71b67c2`의 실제 diff는 `plan.md` Upstream을 수락된 spec `e18a807`로 바꾸고, 앞서 발견한
`유일한 RED` 표현을 텍스트 요약 1–5단계로 한정해 6단계 JSON RED와 구분했다. 같은 커밋의
`decisions.md`에는 Q-json-1/2 답과 intent `7d32d1a`·spec `e18a807` 수락, r2 Git 문구의
`d4d2153`/maker `e0657c9` 출처와 사전 HUMAN 정책 결정, 준비 기록 누락을 소급하지 않는다는
설명이 있다. 이는 native reviewer의 자율 보완이 아니라 최종 HUMAN 복구다.

`54b1d8d`에서 HUMAN은 전체 `plan.md@71b67c2`를 읽고 수락해 로컬 통합을 결정했다. merge
`c5ea850d1204bc9adf84741c07e673cf402f75c7`는 최신 main `79103f7`과 그 수락 판을 두 parent로
결합한다. 최종 main `910e2ac`은 merge 뒤 검증 결과만 `decisions.md`에 추가했다.
`git merge-base --is-ancestor 79103f7 910e2ac`는 성공했고,
`git diff --check 79103f7..910e2ac`도 성공했다. 따라서 `96c0043`에서 관측한 execution EOF
blank 문제는 최종 범위에 남지 않는다.

root가 생성한 `r2-merged-check.json`을 다시 실행하지 않고 직접 읽었다. `revision`은 위 merge
SHA, `pass`는 true, `count`는 50이다. `whole_test`는
`python3 -m unittest discover -s tests -v`, 종료 0, `Ran 17 tests`, `OK`를 기록한다. 50개
관측은 OFF에서 새 명령 거부와 기존 명령 유지, ON에서 텍스트/JSON·owner·빈 결과·대소문자·
complete 후 최신 집계, 읽기 불변과 반복 complete, 다시 OFF를 포함한다. 이 근거는 archival 뒤
`codex/experiment-2026-09-11-f04-json-r2:raw/r2-merged-check.json`에서 보존된다.

### HTML 12개 주석 보존 검사

최종 HTML에서 `0024` 문단은 다음 12개이며 문서 순서도 예상과 같다.

```text
V3-01,V3-09,V4-06,V4-08,V4-11,V6-04,V6-05,V6-06,V7-09,V8-02,V8-09,V10-05
```

정확히 `<p><b>0024`로 시작하는 12줄만 제거한 결과를 maker `e0657c9`의 원문과 byte 단위로
비교했다.

```text
base_bytes 1272792
current_bytes 1280714
new_0024_count 12
expected_ids_match True
base_equal_after_removal True
base_sha256 04945f0ebaa80d5ca58f9b2c8c0df9d0175b91cb6eae4e50bba37b1a4eeec707
stripped_current_sha256 04945f0ebaa80d5ca58f9b2c8c0df9d0175b91cb6eae4e50bba37b1a4eeec707
base_details_count 179
current_details_count 179
details_tuples_equal True
duplicate_ids []
local_link_count 12
missing_local_links []
bad_paragraph_structure []
```

따라서 새 주석 밖 원 플레이북 bytes와 기존 주석, 179개 ID/class/판정 tuple은 그대로다. 각 새
문단은 `<p>`와 `<a>` 한 쌍을 가지며 12개 상대 링크 모두 현재
`docs/experiments/0024-spec-plan-activation.md`로 해소된다.

새 세 문단의 주장도 완료된 공개 이벤트와 일치한다. V4-11은 원 T07/r01 실패와 r02
`dc05fc0`·`96c0043` same-commit 성공, 마지막 HUMAN 참조 정정, hook 미도입을 구분한다. V6-04는
r02가 실제로 feedback/TDD/brand/data Skill을 읽고 문서 선행 개정·RED→GREEN·native 검토로
연결한 사실만 말한다. V6-06은 원 실행의 미호출, r01의 부분 선택, r02의 자연 선택을 구분하고
매번 로드나 일반 성공률을 주장하지 않는다.

### 최종 판정 범위

AC5는 r02에서 자연스럽게 충족됐고, native 검토 뒤의 plan·시험 보완도 같은 커밋에 남았다.
마지막 upstream/RED 문구는 HUMAN이 고쳤으므로 전체 사슬의 자율·무오류 성공으로 판정하지 않는다.
결론은 같은 데이터와 제한된 모델·문맥의 표적 재시험에 대한 PASS다. 의미 동기화 hook, 호스티드
PR/CI, 실제 운영 배포, 장기 안정성은 검증하지 않았고 기본 공개 설정은 OFF다. 원 실패와 이 HUMAN
복구를 보존하는 현재 HTML의 기존 `부분` 판정이 이 증거 범위와 맞는다.
