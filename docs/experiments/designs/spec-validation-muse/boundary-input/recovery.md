# 실행·복구와 효과 순서

C는 OS supervisor가 이전 C의 실제 종료를 확인한 뒤 기동한다. C는 원장의 프로세스 간 배타 잠금을
획득해야 한다. supervisor는 C/W process identity를 PID 재사용과 구분해 보존하고 실제 wait/reap 결과로
종료를 증명한다. 단절·응답 timeout·lease 만료만으로 종료를 인정하지 않는다. 동시 C는 허용하지 않는다.
모든 업무 갱신은 C의 직렬 event loop에서 원자 트랜잭션으로 수행하며 외부 호출 중 잠금을 오래 잡지 않는다.
일시적인 원장 트랜잭션 잠금 구현과 프로세스 수명 전체의 C 독점 잠금은 구분한다.

## 정상 작업
1. submit 등록이 커밋되면 queued다. C는 W가 없고 이전 W 종료가 확인되었을 때만 새 W를 기동한다.
   한 W는 한 번에 한 작업을 처리한다. C는 queued 중 requestId ASCII 순서로 하나를 골라 attempt+1과
   calculating을 함께 커밋한 후 compute를 전달한다.
2. W의 result를 contracts 순서로 대조해 publishing과 total을 함께 커밋한다. ack가 유실되어 W가
   같은 result를 다시 보내도 state가 calculating이 아니므로 stale_attempt다. 이는 이미 확정된 결과를 취소하지 않는다.
3. C는 publishError가 없는 publishing 행마다 같은 key/total로 R.put을 호출한다. 한 행에 한 outstanding
   호출만 허용한다. 5초에 한 번 재시도하며 연결 실패 후 timeout은 10초다. timeout 뒤 이전 R 처리가
   살아 있어도 같은 key/total의 중복은 R의 원자 멱등 계약으로 한 결과만 저장된다.
4. R created/existing 응답과 total을 대조한 뒤 published를 커밋한다. R 커밋과 C 커밋 사이의 분산 원자성은
   약속하지 않는다. 같은 키 재시도로 수렴한다. publishError가 생기면 그 행만 중단하고 다음 행을 처리한다.

## 독립 장애
| 사건·생존 주체 | 차단과 재개 |
|---|---|
| W 종료, C/R 생존 | C는 supervisor의 해당 W 실제 종료를 기다린다. 종료 확인 전에는 새 W/새 compute를 금지하나 get·새 submit·기존 publishing의 발행은 허용한다. 확인 후 calculating 행을 queued로 되돌리고 total null 유지, 다음 dispatch에서 attempt를 증가시킨다. 이전 result는 유효 calculating attempt가 아니어서 거절된다. |
| C 종료, W/R 생존 | 새 C는 이전 C 종료·원장 독점 잠금을 확인하고 이전 W를 종료시켜 실제 종료를 기다린다. 모두 확인하기 전 readiness false, result/submit/get 및 R 새 호출 금지. 그 뒤 calculating만 queued로 회복, publishing/published와 확정 total은 유지한다. 새로운 W 기동 후 readiness true. |
| R 종료, C/W 생존 | submit·compute·조회는 계속한다. C는 publishing 행을 유지하고 같은 key/total로 5초 간격 재시도한다. R 복구 후 멱등 결과로 published를 확정한다. 계산 상태로 되돌리지 않는다. |
| C/W 함께 종료 | C 기동 절차의 이전 C/W 종료·독점 잠금 확인을 그대로 적용한다. calculating만 queued, 확정 데이터는 유지한다. |
| 원장 읽기/쓰기 실패 | C가 readiness false가 되어 업무 갱신·새 dispatch·발행을 멈추고 W를 종료시킨다. 이전 C/W 종료와 원장 정상 접근·독점 잠금을 확인한 재기동 절차에서만 복구한다. |

W 종료를 확인하지 못하면 운영자가 supervisor 상태를 확인하고 실제 프로세스를 종료한 뒤 같은 절차를
재개한다. C가 살아 있는 W 장애 대기 동안은 서비스 전체 readiness를 false로 만들지 않으며 계산 배정만
차단한다. AC10의 readiness false는 C 기동/원장 장애 복구 중 이전 W를 확인하지 못한 경우다.
서비스 기동 후의 일반 W 장애에서 작업자 실행권 차단과 조회 가능성을 구별한다.
이 절차는 미래 실행 계약이다. 실제 재시작·중복 전달·응답 유실 시험 결과는 plan과 구현에서 확보한다.
