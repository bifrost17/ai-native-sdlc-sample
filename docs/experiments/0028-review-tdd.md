# 0028 — 리뷰 피드백 뒤 TDD 복귀 부분 실험

**판정: 리뷰 수신 뒤 TDD 복귀의 관측 범위 통과.** 2026-09-12, 두 새 세션의 최초 사례와
HTTP의 실제 후속 발견을 주고받는 1회 대화까지 수행했다. 첫 HTTP 완료의 계약 누락은 HUMAN
피드백 후 복구했으므로 최초부터 무결한 통과로 바꾸지 않는다. 아래 고정 설계는 실행 전에 작성했다.

## 목적과 변경

0027의 HTTP·CSV 리뷰 수정에서 수동 재현 뒤 구현을 먼저 고치고 자동 시험을 추가한 누락이 있었다.
팀 `sdlc-feedback` 0.1.7은 동작 결함을 받으면 기존 `tdd`의 자동 재현 → 예상 RED → 수정으로
돌아가도록 짧게 연결한다. 기존 예외·증거 규칙을 재사용하고, 템플릿 정책·양식·검사기는 추가하지 않는다.
목표는 주요 흐름이 대체로 잘 작동하는 수준이며 에이전트의 실수를 완전히 막는 것이 아니다.

## 고정 설계와 중단 기준

- HUMAN: Codex root. AGENT: OpenCode 1.18.30, `opencode-go/muse-spark-1.3-contributor` / xhigh.
- 후보 팀 소스: `ece15c449452f6a425d049172e0e71aa94ebc180`; 템플릿 `84a77b3`, 어댑터 `fbe019c` 유지.
- HTTP: 0027 PR2 최초 native review 직전(`raw/08.jsonl` 103행 전), 기존 52개 시험 GREEN.
- CSV: 0027 PR3 최초 native review 직전(`raw/09.jsonl` 83행 전), 기존 65개 시험 GREEN.
- 원래 base의 얕은 이력과 당시 파일 전체를 보존하고, 이후 수정 파일·리뷰 결과·제작 자료를 전달하지 않는다.
  각 설치 seed → 보존 snapshot → seed에서 파생한 수정 브랜치를 유지한다.
- 새 세션마다 HUMAN은 기존 리뷰의 **증상·계약만** 전달한다. 구현 해법·스킬 이름·시험 순서 힌트는 주지 않는다.
  AGENT가 결과를 보고하면 HUMAN이 근거를 읽고 필요한 실제 피드백을 전달한다.
- 최초 두 사례 후 중요한 누락이 있으면 스킬을 한 번만 보완하고 새 세션으로 해당 사례를 재시험한다.
  최대 root 개발 CLI 4호출, 시작 07:24:35 UTC부터 45분(08:09:35 UTC) 이내다. 실패 후 예산을 늘리지 않는다.
  두 사례가 충분히 통과하면 추가 실행하지 않는다. 검토 대기·오류·미완료도 그대로 보존한다.

판정은 HUMAN이 실제 tool 사건과 파일 diff를 읽어 내린다. 리뷰의 동작 결함 → 자동 재현 시험 추가
→ 예상 동작 차이로 RED 실행 → 첫 제품 코드 수정 → 같은 기대 GREEN 순서가 주 평가 대상이다.
수동 재현이나 사후 시험만으로 RED를 주장하지 않는다. 기존 TDD 예외는 근거와 적용 범위를 별도 기록한다.
시험 수·기대 완화·실제 종료코드·전체 제품 회귀·문서 정합성·변경 범위·최종 독립 검토 대기를 함께 본다.
OpenCode에는 Claude 보호 hook을 설치하지 않았으므로 보호 단계의 강제 실행은 통과 범위가 아니다.

이는 리뷰 발견 **수신과 수정 방법**의 부분 실험이다. native reviewer의 자발적 발견·콜백 자동 연결,
전체 SDLC 재실행·성공률·개선의 인과 효과는 증명하지 않는다. CSV는 그 시점에 이미 수락된 HTTP
이력을 포함하므로 두 사례도 완전히 독립된 표본이 아니다. 새 문맥의 최종 검토는 별도 관측한다.
변하지 않은 설계·계획·인도 전체 흐름은 0027 근거를 재사용하며 실제 운영·hosted PR은 미관측이다.

HUMAN 전용 준비·설계 리뷰·원본 증거:
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0028-review-tdd/`.
제품 공간: `/Users/jake/Projects/ai-native-sdlc-opencode-review-tdd-20260912/{http,csv}/`.
첫 실패와 수정 후 결과를 덮어쓰지 않는다. HUMAN의 시험은 파이프 없이 실제 종료코드를 따로 기록한다.

## 결과와 반복

두 최초 요청은 스킬 이름이나 시험 순서를 지정하지 않았다. 모두 실제 `tdd`와 `sdlc-feedback`
본문을 읽은 뒤 자동 재현 시험의 실패를 확인하고 제품 코드를 고쳤다. 0.1.7을 실험 중 재개정하지
않았다. 추가 계약 결함에는 HUMAN이 실제 응답을 읽고 후속 요청을 했으며 새 대본을 미리 넣지 않았다.

| 사례·실제 사건 | 자동 RED → 구현 → GREEN 근거 | 판정 |
|---|---|---|
| HTTP 최초: 미지원 메서드 501 HTML | `http/raw/01.jsonl` 시험 편집 52행 → 실행 55행, `501 != 405`·`501 != 404`, rc 1 → 제품 편집 64행 → 같은 시험 67행 GREEN, 전체 54개 | 해당 발견의 TDD 복귀 통과. 최초 PR 완료는 아래 경로 계약 누락으로 불완전 |
| CSV 최초: 리터럴 DB 경로·빈 경로 | `csv/raw/01.jsonl` 시험 편집 57행 → 60/63행 신규 4개 실제 실패 → 제품 편집 66/69/72행 → 75행 15개 GREEN, 전체 69개 | 해당 발견의 TDD 복귀 통과. 파이프 rc 한계 별도 |
| HTTP 후속: `/requests/`의 잘못된 405 | `http/raw/02.jsonl` 시험 편집 14행 → 17행 `405 != 404`, rc 1 → 제품 편집 23행 → 같은 시험 26행 GREEN, 전체 55개 | 같은 세션의 HUMAN 보조 복구 통과. 새 독립 표본으로 세지 않음 |

HTTP 최초 native는 `TRACE /requests/`가 405라는 사실을 관측하고도 경미한 선택 사항으로 낮췄다.
그러나 `design/api.md`는 끝 `/`의 경로와 빈 ID를 이미 404로 정한다. HUMAN은 기존 계약을
그대로 적용하라고 두 번째 요청을 보냈다. AGENT는 미지원 메서드의 경로 판정을 바로잡아 기존
POST도 함께 404로 맞췄다. 정상 경로의 405·일반 404·OFF·부호화된 ID 의미를 유지했다.
이것은 템플릿 규칙 부족으로 단정하지 않고 **검증자 판단 누락과 사람 협업의 복구**로 기록한다.

CSV의 RED는 `tail`/`grep` 파이프의 tool rc가 0이었지만 출력에 `FAILED (failures=4)`와 실제
단언 실패가 남았다. 따라서 자동 실패 관측은 확인하되 **시험 프로세스의 rc를 보존했다고 쓰지 않는다**.
HTTP도 전체 회귀 일부를 `tail`로 줄였다. HUMAN은 두 최종 제품에서 파이프 없이 전체 시험을
별도 실행해 stdout/stderr와 실제 rc 0을 보존했다. [실험 기록 양식](run-record.template.md)의
공통 증거 안내만 보강하고, 에이전트의 모든 셸 실행을 통제하는 장치는 추가하지 않았다.

계약·설계·작업 순서는 그대로여서 제품 spec/plan은 형식적으로 수정하지 않았다. 실제 구현·시험·
USAGE/IMPLEMENTATION 근거를 같은 제품 커밋에 담았다. 이번 결과를 요구 변경 시 선행 문서
갱신의 재실증으로 쓰지 않으며, 그 항목은 0026·0027의 해당 근거를 재사용한다.

## 전체 회귀와 수락 범위

- HTTP 최종 `638a9411fcb4bcdffd1e12c75a872fafcfd772d8`: HUMAN 직접 전체 **55시험, rc 0**.
  최초 `7d8ab7c`와 뒤의 경로 수정 커밋을 모두 보존한다. 기존 저장소·가져오기·CLI 파일은 유지했다.
- CSV 최종 `d16de164a907a0e63ce58eae06feee8c5434d36f`: HUMAN 직접 전체 **69시험, rc 0**.
  0027의 수정된 독립 관측기를 새 상태·새 출력 경로로 실행해 **126/126** 통과했다.
  명령 17·HTTP 요청 67·SQLite 스냅샷 8개로 읽기/실패 불변·CSV/API·OFF→ON→OFF를 확인했다.
- HUMAN 수락 뒤 각 부분 실험의 main으로 통합했다. 두 main은 각각 HTTP/CSV 시점의 결과이며
  서로 결합한 새 전체 릴리스가 아니다. CSV의 역사적 HTTP 기준판에는 별도 HTTP 후속 수정이
  들어 있지 않다. 126관측은 trailing-slash 경계를 덮지 않으므로 전 경계 무결성으로 확대하지 않는다.
- 시험한 개발판과 수락·merge 결과를 비교해 `DECISIONS.md`만 바뀌고 시험 대상 파일은 동일함을
  확인했다(HTTP 150파일, CSV 152파일 동일). merge 뒤 같은 시험을 다시 실행한 것으로 쓰지 않는다.
- 제작 저장소 `make check`: Python **96개/1 skip**, hooks **28**, eval harness **8**,
  managed-settings 검사 통과. 스킬 quick validation·Claude plugin strict validation도 통과했다.

새 native 최종 검토는 HTTP 두 번·CSV 한 번, 모두 결과를 반환한 뒤 부모가 커밋·보고했다.
검증자는 현재 파일과 실제 시험을 확인했지만 최초 역사적 RED를 직접 본 것은 아니었다.
HUMAN은 별도의 공개 도구 사건에서 실제 선후를 확인했다. native가 구 코드를 임시 재현한 것을
원래 자동 RED 실행 증거와 혼동하지 않는다. 재현 시험의 별도 보호 커밋·Claude hook 집행은
이 OpenCode 부분 실험의 통과 범위가 아니다.

## 환경·설치·호출

OpenCode 프로젝트에서 native 14종(총 발견 16종 중 외부 두 스킬은 권한 거부)과 수동 파일 자료
2종을 유지했다. feedback 원본 폴더만 pinned 0.1.7로 교체하고 기존 어댑터 patch의 dry-run과
실제 적용을 확인했다. 독립 재구성 검토는 HTTP 151/151·CSV 153/153 파일 해시 일치와 미래
제품 `7e60309` 객체 접근 불가를 확인했다. 복원 준비는 HUMAN이며 제품 수정·새 시험은 AGENT가 작성했다.

Claude 사용자 범위 `intent-sdlc-skills@intent-sdlc-skills`를 **0.1.5 → 0.1.7**로 영구 갱신했다.
validate/marketplace update/plugin update/list와 설치 캐시의 feedback 본문·출처·TDD 본문 해시를
확인했다. 이번 실제 동작 실험은 OpenCode다. Claude 새 개발 세션의 로드·동작까지 시험했다고
쓰지 않는다. [설치 안내](../../org-skills/README.md)와 [OpenCode 고정 판](../../org-skills/opencode/README.md)을 갱신했다.

| 문맥 | session ID | 실제 export 모델·variant | assistant 메시지 |
|---|---|---|---:|
| HTTP 개발, 2회 대화 | `ses_f6b76e29effeSWvBnY7r1M5kVl` | Muse Spark 1.3 / xhigh | 60 |
| CSV 개발 | `ses_f6b76e29dffecsOfoDENmqaPHD` | Muse Spark 1.3 / xhigh | 44 |
| HTTP 최초 검토 | `ses_f6b74b824ffen7vasAQM46dQs4` | Muse / default; assistant variant 없음 | 12 |
| HTTP 후속 검토 | `ses_f6b707646ffeg3YMVFbs07sLo4` | Muse / default; assistant variant 없음 | 16 |
| CSV 검토 | `ses_f6b74cba4ffe0sjq4Qv6uO0KCy` | Muse / default; assistant variant 없음 | 16 |

개발 CLI **3호출**, native **3세션**. 모든 root 실행 종료 0, timeout/error event 0이며 호출 시간은
262.150초·306.939초(최초 둘은 병렬)·197.698초다. 마지막 개발 호출은 07:42:25 UTC경 끝나
고정 45분/4호출 상한 안에서 중단했다. 비용·성공률·모델 우위를 추정하지 않는다. verifier 설정은
Muse/xhigh·30 steps지만 native export의 default를 실제 내부 xhigh 실행의 증명으로 쓰지 않는다.

HUMAN 도구의 최초 복원 실패(삭제된 임시 probe 경로), PyYAML 미설치, OpenCode debug pipe의
UTF-8 절단은 별도 준비 실패로 보존했다. 복원 오류는 실제 모델 실행 전에 정정하고 해시로 확인했다.
발견·설정은 기존 PTY 방식으로 재확인했으며 잘린 debug 출력 바이트는 보존하지 못한 한계가 있다.
HTTP 후속 수동 probe의 중복 INSERT 오류도 원래 trace에 남고 정정 후 재실행했다. 이를 제품
회귀나 자동 시험 RED로 세지 않는다. 이전 0027 관측 JSON 소실도 이번 통과로 지우지 않는다.

## 보존과 최종 판단

설계 독립 검토(Astra/ultra), 실험·판정 독립 검토(Sol/high), HUMAN 최종 판독이 관측 범위 통과에
동의했다. 변경된 리뷰→실행→회귀→완료 인계는 다시 평가했고, 변하지 않은 플레이북 원문·역할·
정책 소유·작성 양식은 0027 근거를 재사용했다. 실제 운영·hosted CI/PR·전체 새 개발 사슬은 미관측이다.

스킬은 네 줄의 연결 보강에 그쳤다. 템플릿 정책·양식·의미 검사기·새 승인 단계는 추가하지 않았다.
사람이 계약 누락을 바로잡아 결과를 인도하는 목표는 달성했으며, 추가 규칙으로 완전 통제를 추구하거나
같은 사례를 통과할 때까지 반복하지 않는다. 북극성 주석에는 이 좁은 근거만 추가하고 0027의 부분
TDD 판정과 새 검증자 판단 누락을 보존한다.

| 보존한 제작 저장소 ref | 고정 커밋 |
|---|---|
| `codex/product-0028-http-seed` | `fd787e3da5b950f015a0f8807904903eb8c63987` |
| `codex/product-0028-http-snapshot` | `39ad3e297a54f42e9804469e5ea8290e05f89c51` |
| `codex/product-0028-http-fix` (HUMAN 수락 포함) | `664ae4a7b83295600a86c118b78dacce72971c2a` |
| `codex/product-0028-http-main` | `f8162c47247f15ded52532b35245066735adfa1e` |
| `codex/product-0028-csv-seed` | `cfa9a622253a096f8950452e8c5194b89fbca0e4` |
| `codex/product-0028-csv-snapshot` | `fae75c562e17b4cfb86126fc325ba840101d76dd` |
| `codex/product-0028-csv-fix` (HUMAN 수락 포함) | `44f2cb5b765b12afda831c49fec6664e7132b956` |
| `codex/product-0028-csv-main` | `e7a9734fb3e5128c56b7362c541dcd0f22b3d01b` |
| `codex/experiment-2026-09-12-review-tdd` (사후 증거 bundle) | `f9a367ef993cfdbc2aa26b324ef5198e3cd79288` |

증거 bundle은 위 기록 브랜치의 `_experiment/0028-review-tdd/`이며 **69파일+MANIFEST.json**
전체 해시를 확인했다. 설계·독립 감사·준비 코드·프롬프트·정제된 공개 trace/export·첫 실패·최종
시험·HUMAN 관측·수락·설치 증거가 들어 있다. 로컬 체크아웃은
`/Users/jake/Projects/ai-native-sdlc-exp-0028-record/`다. CSV main을 부모로 한 사후 기록 브랜치이며
HUMAN 판단 자료가 포함되므로 후속 AGENT 실험의 입력 seed로 쓰지 않는다. 제품 코드는 제작 main에
합치지 않았고, 위 ref와 기록은 로컬 보존이며 push·hosted PR·실제 배포는 하지 않았다.
