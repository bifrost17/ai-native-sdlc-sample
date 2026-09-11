# 팀 스킬 활성화 구현 기록

2026-09-11. 0024의 허가 범위에서 `skill-creator`를 읽고 org-skills 소스만 변경했다.
설치·새 세션 적용·제품 구현은 이 작업의 관측이 아니며 root의 후속 실행에 남는다.

- 후보의 spec-policy-pass, spec-policy 명령, tdd의 SKILL/PROVENANCE 네 파일은 활성 경로에
  바이트 동일하게 전달했다. 기존 영문 PO 프롬프트도 185dd5e와 바이트 동일함을 대조했다.
- 정책 검토는 연결된 spec 설계 정본 전체와 실제 관련 정책 적용·출처·판·중요 미결 근거를 본다.
  기존 허가/결정을 재사용하며, 한 파일·우려 수·전량 표·빈 결정칸을 강제하던 절차는 대체했다.
  기존 spec-policy-pass/PROVENANCE는 원문을 보존하고 상단에 0.1.4까지의 역사 기록임을 밝혔다.
- sdlc-verifier의 기존 Review criteria 네 항목에 영향 spec/plan 동시 기록, 선행 시험의 실제
  행동 실패와 독립 기대의 GREEN, 정당한 시험 수정/기존 GREEN/리팩터링/종료된 공개 단계,
  최신 결합·머지 결과와 완료 주장에 해당하는 전체 공개 단위를 통합했다. 현재 허가된 draft/change와
  수락 기준 판을 구별하며 이미 허가된 작업에 새 수락 관문을 만들지 않는다. Opus/high·보고 전용 권한은 유지했다.
- sdlc-feedback은 위 공통 기준을 참조하며 각 이벤트의 영향 문서와 실행 근거 인계를 보강했다.
  새 loop·승인·CLI·checker를 추가하지 않았다. README에 정책/명령의 역할과 TDD 소스·배포·단독 설치·
  적용 및 실제 로드/행동 증거의 구분을 추가했다.

## Validation

- 변경한 스킬·명령·검증자·README·출처의 로컬 Markdown 링크 대상 12개 존재 확인.
- 후보 네 파일 및 기존 PO 영문 프롬프트 보존 대조 통과.
- `git diff --check` 통과. 별도 제품 RED는 만들지 않았다.
- `quick_validate.py`는 시스템 Python과 Codex bundled Python에서 PyYAML 부재로 먼저 종료했다.
  root가 안내한 기존 uv 방식으로 다시 실행해 세 변경 스킬 모두 `Skill is valid!`, rc=0을 확인했다:
  `uv run --with pyyaml --no-project python /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-path>`.
  대상은 `org-skills/skills/{spec-policy-pass,tdd,sdlc-feedback}`다. 전역 Python이나 저장소 의존성은
  변경하지 않았다. 이 결과는 형식 확인이며 실제 행동을 입증하지 않는다.

## Activation caveats

현재는 소스 변경 근거다. plugin/marketplace 판 갱신, 실제 validate/update/list, 새 정상 세션의
로드 경로·판 확인과 자연 요청 적용, 제품 test-first·문서 동기화 관측이 필요하다. README의 명령은
설치 안내이며 이 작업이 실제 실행했다는 뜻이 아니다. 연구 출처는 보존 맥락이며 설치된 TDD 실행의
필수 의존성이 아니다. 전체 활성 변경의 `make check`와 독립 검증은 root가 통합된 범위에서 수행한다.
