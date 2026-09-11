## 인계 판단: 대화 없이 구현 가능한가

가능하다. spec.md/plan.md가 요구·AC·파일·PR 순서·Proof를 구체적으로 연결하고, TDD SKILL이 RED→GREEN 절차를 규정하며, baseline 코드/데이터/RELEASE-CONTROL 정책까지 정합적으로 맞물린다. 다만 아래 "공백" 항목들은 구현 중 개발자 재량으로 채워야 하며, 이를 인지하지 못하면 계약 이탈 위험이 있다.

## 첫 작업(PR1) — 파일·검증 순서

1. `tests/test_owner.py` 신설: AC1 기대(원순서·기존 열·rc0·바이트 불변, `--owner hana`)를 먼저 작성해 실행 → 현재 `--owner` 미지원이므로 `argparse` rc2 RED 확인(P0/P1).
2. `tracker.py`에 공유 판정 함수(`TRACKER_OWNER_INSIGHTS` 읽기, "1"/대소문자무관"true"만 ON, 공백 미제거) + ON일 때만 `list`에 `--owner` 등록 → 최소 구현으로 GREEN.
3. `tests/test_release_control.py` 신설: OFF에서 `list --owner`/`summary` 직접 호출도 rc2(AC5), 설정값별 ON/OFF 표(P2) 확인. 이 시점 `summary`는 ON이라도 미구현이며, 그 관측은 "단계 한정"임을 기록(영구 회귀 아님).
4. 기존 `tests/test_tracker.py` 전체 재실행(P0, 회귀 유지) + `USAGE.md` 갱신.
5. PR1 리팩터링 후 최신 main과 결합 검증.

## 각 PR의 통합·공개 상태와 남은 판단

- **PR1**: main 머지 후 기존 명령은 그대로 동작, 일반 OFF, TEST ON에서는 `list --owner`만 가능. 남은 판단: 집계 구현, 전체 공개 여부. 리스크는 "PR1 시점 summary 부재"를 PR2까지 영구 계약으로 착각하는 것(plan이 명시적으로 경고).
- **PR2**: PR1 main에 의존(순차 진행, 동시 branch 편집 금지). `tests/test_summary.py` 신설로 all/open/done RED→GREEN(P3), `test_release_control.py` 갱신. 머지 후에도 일반 OFF 유지, TEST ON에서 목록+집계 전체 가능(P0–P4). 남은 판단: 개발자 리허설(P4, 사본에서 OFF→ON→OFF)과 오너의 실제 공개 결정, 그 이후 실제 운영 환경에서 새 프로세스로 ON 적용/OFF 관측. **공개 자체는 코드 PR이 아니라 별도 설정 변경 행위**이며, 이 인계 범위에서 실행하지 않는다.
- **cleanup(조건부)**: PR2 통합·공개/중단 관측, 구버전/복구 대상의 flag 의존 소거, 오너의 정리 요청이라는 세 조건이 모두 충족된 뒤에만 착수. 아직 어느 조건도 이행되지 않았다고 문서가 명시.

## 완료/cleanup에서 유지·변경할 검증

- **유지**: `test_tracker.py`(P0) 전 구간, 최종 AC1–4(P1/P3의 정확 일치·순서·집계 수식) — cleanup 후에도 무설정으로 동일하게 통과해야 함.
- **변경(폐기 대상으로 명시)**: PR1/PR2의 OFF 거부 시험(P2)과 값별 토글 시험은 cleanup에서 "폐기된 계약"이 되므로 제거하되, spec/plan/PR에 교체·제거 사유를 명시해야 한다(AC7이 "예전 OFF 거부는 이 판의 요구가 아님"이라 못박음). SKILL의 원칙과도 일치: 요구 변경/은퇴된 release-control 단계는 assertion 완화의 정당한 근거이나, 독립적 근거 보존과 리뷰가 필요.
- cleanup 착수 시 순서: 먼저 무설정 최종 동작 시험을 RED로 확인(현재 flag 판정이 남아있어 실패해야 정상) → flag 판정 제거 → GREEN, 코드/시험/문서 배포 확인 후에만 설정 정리(설정 먼저 지우면 OFF 기본값 코드가 남아 기능이 다시 꺼질 위험, RELEASE-CONTROL 경고와 일치).

## 문서상 공백

1. **공개 결정 기록 문서 부재**: spec/plan 모두 실제 공개·중단 결정을 "제품의 `intent/f03-owner-insights/decisions.md`"에 남기라고 지시하지만, 이 파일의 서식(결정자·시각·코드 판·대상·설정값·근거 필드)이 후보 문서 어디에도 정의되어 있지 않다. 실채택 저장소에서 새로 만들어야 하며, 인계만으로는 그 구조를 알 수 없다.
2. **오너/담당자의 실체 미지정**: "공개 담당(root 역할)"·"합성 업무 오너"라는 placeholder만 있고, 실제 승인자 이름·역할·연락 경로가 없다. 실무 인계 시 반드시 구체 인물/역할로 확정해야 하는 판단 공백이다.
3. **cleanup 트리거의 판정 절차 미정**: "안정화", "알려진 구버전/복구 대상의 flag 의존 없음"이라는 조건이 정성적으로만 서술되고, 이를 어떤 로그/모니터링/조사로 확인할지는 문서화되지 않았다. 로컬 CLI 모의라는 범위 제약과 맞물려 실제 판정 방법은 채택 시점에 별도로 정해야 한다.
4. **CLI 문법 세부(usage string) 미확정**: `summary`가 완전히 새 서브커맨드인지, `--owner`의 에러 메시지·`--data`와의 조합 등 정확한 argparse 그래마가 spec Design에 예시로 없다. AC/Proof의 행동 계약(출력·rc)은 충분하지만, 문법 세부는 구현자가 결정해야 하는 여지로 남아 있다.
