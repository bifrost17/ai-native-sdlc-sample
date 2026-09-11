# Astra 범위 한정 후속 리뷰 — r2

**판정: CHANGES REQUIRED.** 대상은 `920ca52db361387eddf82d26e7fd67d455d2a634`다.
기존 작성 지침의 보존·교체 매핑을 실제 본문과 대조한 결과, 한 문장으로 복원할 수 있는 잔여 누락이 있다.
F03·M01의 이번 보완에서는 추가 차단 발견이 없다.

**수정 필요 — 생성 prompt의 보존 지시가 전체 교체안에서 빠졌다.**

- 위치: `candidate/skills/design-spec/SKILL.md:10–19`의 입력·출처 기록 지침,
  `candidate/policy-and-delivery.md:44`의 본문 교체 및 `:63–65`의 보존 매핑.
- 근거: 기존 `.claude/skills/design-spec/SKILL.md:36`은 생성 prompt와 적용 스킬 판을
  versioned spec/PR 기록에 함께 보존하도록 명시한다. 고정 원문
  `inputs/north-star-excerpts.md:57`도 스펙·그것을 만든 prompt·효력 있는 스킬 판의 기록을 요구한다.
  후보는 스킬 판과 입력 SHA는 남기지만 prompt의 보존은 본문·출처 reference·교체 매핑 어디에도 없다.
- 반례: 작성자가 intent SHA와 `Skills applied`를 채우고 최종 spec만 커밋하면 후보 지시는
  지킬 수 있지만, 별도 제약을 전달했던 생성 prompt는 임시 대화에만 남아 사라질 수 있다.
  따라서 전달표대로 기존 스킬을 교체하면 이미 있던 원문 추적 의무를 잃는다. 이 연구 실행 자체의
  prompt 보존이 향후 작성 스킬의 지시를 대신하지는 않는다.
- 최소 수정: 후보 스킬의 출처 기록 문단에 기존 의미를 복원한다. 예를 들어
  `Keep the originating prompt and applied skill versions with the versioned spec/PR record (L3 279).`
  한 문장을 넣고 보존 매핑에도 해당 항목을 포함하면 된다. 새 양식 절·로그 체계·검사기·승인은 필요 없다.
  이는 이번 후속 검토에서 확인한 기존 대비 누락이며, r2에서 새로 삭제한 문장이라고 주장하는 것은 아니다.

**해결 확인과 인접 회귀**

- r1의 비차단 전달 의존성 항목은 해결됐다. `policy-and-delivery.md:47–58,73–82`가 기존
  reference 경로의 후속 정본, walkthrough, cases·baseline·JSON·M01 context, 내부 링크 수정과
  역사 자료의 보존 위치를 구분한다. 독립 공개가 가능한 기존 F02 예시도 F03로 덮어쓰지 않는다.
- 두 양식·두 지침·plan 스킬의 정책 링크는 기존 GitHub Flow·PR 크기·공개 제어 정본을 연결한다.
  스킬 판 reference와 실제 사용 가능한 `spec-policy-pass`, fix 단계의 시험 선행 커밋·새 시험 생성
  차단·mutation 원본 복구 지침도 유지된다. 새 필수 스킬이나 별도 규칙 정본을 만들지 않는다.
- TDD 정책의 적용 위치가 maker `CLAUDE.md / Conventions`, 다음 사용판의
  `PROJECT-POLICY.md / 검증과 운영` 및 참조 지침으로 구체화됐다. maker의 L9 원문 인용은
  바꾸지 않으며, 검토 기준은 기존 verifier 절을 정본으로 유지한다. 실제 사용판 두 파일을 읽어
  지정한 절이 존재함을 확인했다. 과거 branch 수정이나 현재 설치를 요구하는 전달안도 아니다.
- F03 `context.md`, `spec.md / Design`, `plan.md / Order·P4`는 현재 정본과 역사 출처,
  공개 전 사본 리허설과 실제 일반 환경의 결정·관측을 분리한다. PR1 부분 TEST ON을 전체 공개로
  오인하거나 리허설을 실행하기 위해 먼저 일반 공개해야 하는 해석을 줄인다. 기존 OFF 기본·
  공유 제어·cleanup 조건과 최종 회귀 계약은 보존된다.
- M01 `design/architecture.md / 배포 경계`와 `plan.md / PR-C·P-C`는 없는 경로에 빈 DB를
  만들거나 잘못된 버전·스키마를 수락하는 시작을 거부한다. 기존 DB·제약 확인이 시험 선행 작업에
  연결되며 JSON 기본·자동 fallback 금지와 일치한다. 운영 조건은 `design/operations.md`, 실제
  호스트 명령·경로·리허설 절차는 제품 `docs/operations.md`가 소유한다. Q4와 안전한 재개 조건을
  코드 통합만으로 충족했다고 쓰지 않는다. F03/M01의 동시 개정도 `Current change`로 연결했다.

**범위와 한계**

r1→r2 후보 diff와 지정된 변경 파일의 최종 본문, 관련 기존 작성 스킬·reference·정책·기본 지침 및
사용판 파일을 읽기 전용으로 대조했다. r1 전체 검토를 반복하지 않았고 다른 리뷰어 결론·제안·인계
응답은 읽지 않았다. 제품·시험·설치·렌더링·인계 실행을 하지 않았으며, 명령의 성공이나 실제
TDD 준수·운영 준비를 판정하지 않는다. 추가 비차단 제안은 없다.
