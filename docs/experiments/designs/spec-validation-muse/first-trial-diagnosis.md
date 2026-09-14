# Muse 첫 비교 실행의 발견 대조와 최소 보완안

2026-09-14. 읽은 실행 출력은 private 실험의
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse/raw/01-baseline.result.md`와
`02-improved.result.md`다. 제품 근거는
`/Users/jake/Projects/ai-native-sdlc-spec-validation-muse-20260914/improved-r1/context/source-project/`의
고정 사본에서 읽었다. 아래 제품 경로는 이 루트 기준이며 `D/`는
`intent/0003-redesign-compatibility-gateway/design/`, `spec`은 같은 개발건의 `spec.md`다.

이번 진단은 두 결과와 중요한 지적의 실제 근거 대조다. 제품·활성 지침은 수정하지 않았다.
검토자는 보완 절차의 설계와 구현에 참여했으므로 독립 최종 제작 심사가 아니다. 내부 추론을
추정하지 않으며 이 관측만으로 모델 일반 성능이나 문구 변경의 인과 효과를 확정하지 않는다.

## 요약

기준 출력은 계획 인계 가능으로 판단하면서 F1의 manifest 완성을 구현으로 이월했고, 개선 출력은
인계 불가로 바뀌었으나 알려진 F1/F2를 정확히 찾지 못했다. 인계 결론이 더 엄격해진 사실만으로
개선이라고 평가할 수 없다. 반면 개선 출력의 PTY 단위 지적은 실제 문서/코드 충돌을 찾았다.
유효한 추가 발견을 알려진 두 결함을 놓쳤다는 이유로 삭제하면 안 된다.

## 개선 출력의 주요 지적별 대조

### 1. turn/steer 수락·fallback 누락 — 제시한 근거로는 인계 차단 부당

`spec:36` R6는 `docs/diagnosis/execution-lifecycle-contract.md`를 연결하고 `spec:120`은 R에서
연결한 기존 계약의 명시 부분을 보존 대상으로 삼는다. 기존 정본 `:60,66–80`에는 start와 steer의
서로 다른 성공 shape, expectedTurnId, receipt identity, 첫 handoff 후 correction/fallback 금지가
구체적으로 있다. `D/protocol-and-resources.md:162–167`도 원래 native correlation/응답 의미를 유지한다.

따라서 “S8만 지키면 fallback을 부활시켜도 위반이 아니다”는 전체 spec의 권위를 제외한 판단이다.
S2가 한 turn/start 흐름만 구체화했다는 사실은 새 protocol 전체의 충분성을 증명하지 않지만,
이미 정확히 참조한 steer 의미가 새 문서에 반복되지 않았다는 것과는 다른 문제다.
이 지적에서 새로운 충돌/누락을 입증하려면 참조한 정본까지 지키는 두 구현이 달라질 이유가 필요하다.

### 2. PTY tail characters/bytes — 유효한 불일치 발견, 변경 방향은 별도 판단

`docs/TERMINAL.md:18`은 snapshot의 last 16,000 characters를 적고,
`D/protocol-and-resources.md:104`는 기존 16,000 bytes 계약 유지라고 적는다.
현재 `src/server/terminal.mjs:9,37–51`도 실제 UTF-8 bytes를 세어 Unicode suffix를 제한한다.

한글 6,000자는 문자 기준으로 전부 남지만 16,000 UTF-8 bytes에는 전부 들어가지 않는다. 문서와
현재 소스가 같은 의미라고 할 수 없으므로 단위·보존 정본을 정리할 필요는 실제로 있다.
다만 새 S8이 현재 소스의 bytes 기준을 따른다는 근거도 있으므로 곧바로 characters로 바꾸라는
결론은 나오지 않는다. 원본 보존 약속과 현재 기준의 권위를 확인해 문서/설계를 정리할 사안이다.
이는 현재 제품 실행이나 새 topology의 회귀 실패를 실측한 결과는 아니다.

### 3. file etag 식 재기술 부재 — 현재 지적은 과도한 재기술 요구

`docs/APP_HOST_CONTRACT.md:52–57`은 입력/반환, ifMatch/conflict, 정확한 stat etag 식과
낙관 동시성의 한계까지 정한다. `spec:33,120`은 원본 host 계약을 보존하며,
`D/compatibility-coverage.md:11,14`는 file/Git 실행을 X work helper로 옮기고 B의 원래 반환을 유지한다.
`D/integration-and-verification.md:96`도 원래 반환·partial/conflict를 연결한다.

계산 위치 이동이 이 식을 무효화하거나 새 의미를 선택해야 한다는 구체 근거는 결과에 없다.
이미 연결된 정본의 식을 S7/S8에 다시 쓰지 않았다는 이유만으로 계획 인계를 막을 수 없다.

### 4. 두 WS 정체·PTY 소유권 — 기존 정본에 답이 있어 누락 주장 불충분

`docs/TERMINAL.md:24`는 PTY service를 app-host WebSocket connection마다 만들며 연결 close에
명시 dispose한다고 정한다. `src/server/gateway.mjs:454`에는 /bridge와 /app-host 두 endpoint가 있다.
`D/integration-and-verification.md:75`는 browser의 한 WS 손실 때 두 WS/RPC/구독을 닫으며,
`:97`은 PTY의 per-connection 종료 정책을 보존한다. `spec:64` AC6도 기존 PTY 종료 정책을 참조한다.

따라서 한 browser WS 상실에서 두 WS를 닫는지, PTY가 어느 연결에 속하는지는 제공된 계약으로
알 수 있다. 새로운 내부 C/D TLS와 원래 browser 두 WS는 S8 `:20–25`가 구별한다.
추가 소유권표가 없다는 것 자체는 중요한 공백이 아니다.

### 5. automation/queue 선택적 계승 — 검토 우려는 이해되나 제시한 인계 차단 근거 부족

원본 `docs/diagnosis/automation-settings-contract.md:54–76,111–147`에는 thread-keyed settings,
pending/resolution-required, 30일/4096 manual request, fingerprint, history 삭제와 no-replay가 있다.
`docs/diagnosis/execution-lifecycle-contract.md:212–218`에는 legacy queue 이행/격리 import 계약이 있다.

새 `spec:38,128–130`은 automation의 기존 의미를 보존하고 물리 저장만 명시적으로 바꾼다.
S7 `:97–109`는 원본 ID/호출/반환 및 canonical admission/claim을 유지한다. `:138–142`는
가변 파일/runtime-v1.json의 물리 대체와 heartbeat thread-keyed/manual override/unknown 보존을
구분한다. `:170–181`은 재전송 방지 사실과 payload의 회수, 기존 domain count/byte 상한을 유지하며,
`:202–205`는 정지한 writer/claim, 원문 hash/버전, 명시 import와 consumed/unknown 보존을 요구한다.

현재 출력은 특정 필드가 새 논리 테이블 설명에 다시 열거되지 않았다는 점을 주로 지적했다.
원본 ID/의미 유지와 새로운 내부 namespace/fence를 모두 지키는 구현이 왜 재입고를 허용하게
되는지까지 보이지 않았다. 실제 mapping 충돌을 찾아 지적하는 것은 유효하나, 이 근거만으로
자동화를 다시 제외하거나 모든 기존 manual/queue 의미를 S7에 복제하라고 요구하는 것은 과도하다.

### 6. cache-bypass 경로 미실증 — 기존 준비 판별이며 현재 인계 차단 근거 부족

S7 `:227–238`은 기존 loader의 bypass를 사용할 수 없으면 같은 bytes/error 계약의 명시적
network fetch adapter를 구현한다고 정한다. 거짓 cache shim을 금지하고 fetch/cancel/failure/hash,
동시 load와 준비 build의 network/offline·CacheStorage·serviceWorker 관찰을 명시한다.
S9 `:46–48`도 이 선택을 실제 loader·준비 patch 검증에 연결한다.

따라서 특정 loader 옵션의 존재를 아직 실행으로 증명하지 않았다는 사실과 설계 대안/번복 경로가
비었다는 것은 다르다. S9 §6에 같은 항목을 반복하지 않았다는 이유로 준비 계획 자체를 막을
근거는 부족하다. 실제 판별과 후속 제품 실행은 여전히 남으며 성공으로 올려서는 안 된다.

### 7. 독립 두 리뷰 미제공 → 미완료 — 증거 부재에서 미실행을 추론한 문제

S9 `:147–153`과 제품의 review-policy-amendment는 해당 원본 작업의 독립 검토 완료 조건을 정한다.
그러나 이 실험의 `context/README.md:4–10`은 별도 리뷰 판정/과거 기록을 의도적으로 제공하지 않으며
설계 계약 충분성만 읽으라고 범위를 한정한다. 기록 부재로 그 행위가 없었거나 실패했다고 알 수 없다.

따라서 현 입력에서 확인할 수 없다는 한계는 맞지만, “독립 검토가 남음/완료 정의 미충족”을
관측 사실로 제시하거나 새로운 두 리뷰를 요구하는 것은 부당하다. `Status: draft`도 S9 `:153`에서
유지하도록 한 표기이므로 검토 미실행의 증거가 아니다. 기준 출력도 이 항목을 남은 작업으로 표현했다.

## 놓친 두 계약의 구별 가능한 반례

### F1 — 보존한 원본 method 계약과 새 내부 protocol 의미를 구별해야 함

S8 `:3,20–46`은 원본 wire와 다른 protocol1, 공통 prefix/header, type 값과 일부 필수 필드를 정한다.
`:43–46`은 나머지를 type별 schema에만 허용한다고 하지만 그 schema/동등한 의미 정본을 완결하지 않는다.
`:143–152`는 정확 opcode 목록을 build artifact로 이월하고 family 역할을 적으며 coverage `:23–25`는
모든 producer/consumer를 manifest에 연결하도록 남긴다. credit/취소/결과에 관한 일부 의미는 있으므로
아무 계약도 없다는 뜻은 아니다.

그러나 새 binding/flow·blob 등에서 양쪽이 합의해야 하는 지원 operation의 입력·결과·거절 후 상태를
공통 header와 대표 native turn/start 흐름만으로 결정할 수는 없다. 예를 들어 lookup의 대상과
응답 evidence/실패 shape를 서로 다르게 구현하면 각자의 common header와 no-retry 불변식은
지키면서도 상호운용이 깨질 수 있다. 기존 native method의 정확한 응답을 재사용하는 경우와,
새 내부 lookup/handshake 등의 의미를 아직 공동 결정해야 하는 경우를 분리해야 한다.

필요한 것은 지원 operation 의미의 충분한 정본이며 숫자 opcode 배정·코드 생성 완료·모든 JSON schema
파일을 지금 생성하라는 요구가 아니다. 기준 출력은 manifest 완성을 plan 입력으로 이월했고 개선 출력은
원본 steer/etag 의미를 다시 쓰는 데 초점을 옮겼다. 두 출력 모두 이 새 경계의 핵심 공백은 발견하지 못했다.

### F2 — engine만 종료하고 B/X/M은 생존하는 분기

`spec:66` AC8은 engine·container·gateway를 **각각** 재시작한다. S5 `:134–137`의 네 장애는
transport/B/X/늦은 메시지이며 engine 단독 상실과 같지 않다. S6 `:105–108`의 cold recovery 진입은
B/X process 또는 M 연속성 상실이다. S9 `:75–83` 표에도 engine-only 행이 없다.

engine만 종료되고 B/X/M·별도 PTY가 살아 있는 경우, 새 engine을 누가 어떤 세대로 기동하고
현재 binding/credit/PTY와 업무 재개를 어떻게 대조하는지가 다른 장애의 절차로 자동 결정되지 않는다.
S9 `:85–86`의 옛 approval 무효화나 초기 architecture `:141`의 영속/불명 보존은 필요한 불변식이지만
그 새 기동·재개 전이를 완성하지 않는다. 초기 architecture는 `spec:117`에서 현재 결정 정본으로
자동 채택하지 않도록 구분돼 있다. 보존할 값이 있다는 사실과 이 분기가 닫혔다는 판단을 분리해야 한다.

## 최소 일반 개정안과 과잉 경계

root가 제안한 기존 verifier 질문의 명확화는 위 관측에 맞는다. 새 항목 묶음이나 형식을 만들기보다
현재 문장을 다음 의미로 교체/명확히 하는 편이 적절하다.

1. 공유 경계 질문에서 먼저 새/변경 경계와 정확한 기존 정본으로 재사용하는 계약을 구분한다.
   재사용된 계약은 중복 재기술 없이 충분할 수 있다. 새 protocol의 header나 대표 operation만으로
   나머지 지원 operation의 필요한 입력·결과·오류 의미까지 닫혔다고 판단하지 않는다.
2. 기존 AC 분기 질문은 **요구/AC가 독립 또는 각각의 실패를 약속한 경우**, 명명된 실패 주체만
   실패하고 다른 주체가 살아 있는 출발 상태에서 인용한 recovery의 진입 조건을 먼저 대조하게 한다.
   문서에 이름이 나오는 모든 컴포넌트의 단독 실패를 새 의무로 만들지는 않는다.
3. 기존 보고 문장에 검토/실행 기록 미제공은 미실행·실패의 증거가 아니며 확인 불가로 구분한다는
   짧은 경계를 둔다. 실제 관측된 미호출/실패와는 별개다.

REVIEW/design-depth에 정확한 기존 정본 참조를 인정하는 한 문장을 연결하는 것도 중복 요구를
줄이는 보완이다. 숫자 opcode·표·UML·전수 상태·보편적 여러 검토자를 요구하지 않고 필요한 의미와
구현자 인계 가능성에 머무르면 과잉 절차가 아니다. 미검출 때마다 항목을 더하는 방향으로 확장하지 않는다.

이 보완이 실제 Muse 행동을 개선하는지는 다음 한정 실행에서 별도로 관측해야 한다. 현재 출력의
PTY 발견은 보존하고, F1/F2 재검출 여부와 불필요한 재기술/미실행 추론 감소를 각각 기록해야 한다.
