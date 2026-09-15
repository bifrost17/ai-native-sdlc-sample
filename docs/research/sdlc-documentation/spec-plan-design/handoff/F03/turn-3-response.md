## cleanup 전제 (spec R5 / AC6 / AC7 + Design, plan Order of work "cleanup" 행)

spec.md의 cleanup 근거는 **R5**이며, cleanup 검증 자체는 **AC7**(선행: AC6의 OFF→ON→OFF 전환 관측)에 걸려 있습니다. Design 문단(줄60-62)과 plan Order of work의 cleanup 행(줄21-22)이 요구하는 전제는 다음 넷입니다.

1. PR2 통합 (Files/Order of work: PR2가 PR1 main에 의존, cleanup은 그 이후)
2. 공개/중단 관측 — AC6·P4가 요구하는 "같은 완성 코드에서 OFF→ON→OFF" 전환이 실제 관측·기록됨
3. 알려진 구버전/복구 대상이 이 flag에 의존하지 않는다는 확인
4. 오너(합성 업무 오너, root 역할)의 정리 요청

이 넷은 spec Design 줄62 "합성 예시에서 이 조건들은 아직 이행되지 않았다"로 **현재 미충족**임이 명시돼 있습니다. R6는 이번 spec에 없으므로 인용하지 않습니다.

## 확인 역할

spec Design 줄56 "공개 담당은 합성 업무 오너(root 역할), 환경 조작·관측은 개발 실행자다"와 plan 줄37, 44가 일관되게 구분합니다. 조건 충족 판단·정리 요청 승인은 오너(root) 소관이고, 환경변수 설정/해제와 그 관측·기록 실행은 개발 실행자 소관입니다. 개발자가 스스로 조건 충족을 선언하고 cleanup에 착수할 근거는 문서에 없습니다.

## cleanup 최초 시험 (plan 줄44-46)

착수 순서는 "**최종 무설정 동작 시험을 먼저 실행해 기존 OFF 거부가 예상 RED인지 확인**"입니다. 즉 flag 분기를 아직 지우기 전에, 설정 없이 `list --owner`/`summary`를 직접 호출하는 최종 계약 시험을 먼저 작성·실행하면 현재 코드(OFF 거부가 아직 남아있음)에서는 rc2로 실패하는 것이 예상 RED입니다. 그다음 flag 판정/조건부 분기를 제거해 GREEN으로 만듭니다.

## 최종 유지 시험 vs 폐기 시험 (AC7, Proof P5)

- **유지**: AC1–4에 대응하는 test_owner.py·test_summary.py의 exact-match·원순서·all/open/done 집계·무쓰기 케이스, 그리고 P0(test_tracker.py 기존 회귀). Proof P5가 이를 "cleanup 전체 시험 + 설정 없는 직접 목록/집계"로 재확인합니다.
- **폐기**: test_release_control.py의 OFF 거부 시험과 값별 토글 시험(P2에 해당하는 test_off_rejects_new_commands, test_setting_values류). AC7이 "예전 OFF 거부는 이 판의 요구가 아님"이라 명시하고, plan 줄45-46이 "이전 OFF 거부·값별 토글 시험은 이제 폐기된 계약이라 교체/제거 이유를 spec/plan/PR에 명시한다"고 절차를 요구합니다.

정리하면, 이번 현행 문서 기준으로 cleanup은 R5/AC6/AC7·P4/P5 라인을 따라 전제·역할·시험 순서가 정의돼 있으며, 조건 충족 여부는 아직 문서상 미이행 상태로 남아 있습니다.
