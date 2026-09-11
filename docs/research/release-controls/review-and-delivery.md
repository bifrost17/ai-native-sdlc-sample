# 검토와 사용판 전달

root가 조사·정책·양식 변경을 작성했다. 독립 Sol/high가 1차 자료를 조사하고 Sol/medium이 소비자를
감사했다. 중요한 설계는 Astra/ultra와 실제 Claude Code Fable/max가 서로의 결과 없이 검토했다.
일상 실험 구현은 실제 Sonnet/medium이다. 역할과 난도에 따라 모델·추론을 구분했다.

## 독립 설계 리뷰

첫 후보 maker 88b367b/adopter f89a92a에서 두 리뷰 모두 중요한 지적 없이 PASS했다.
[Astra](reviews/astra-r1.md), [Fable 원문](reviews/fable-r1.md).

root가 비차단 개선 중 채택 위치와 인용 표시를 보완했다. ADOPTING은 사용판의 운영 행과 제작판의
여섯 정책 슬롯을 구분하고, 공개 제어를 팀 선택으로 명확히 하며 사용판에도 1차 자료 링크를 남겼다.
기존 CLAUDE/PROCESS에서 workflow를 거쳐 읽을 수 있어 같은 지침을 반복하는 링크는 늘리지 않았다.

최종 core maker 4e766f8/adopter 787af77의 좁은 delta도 두 리뷰가 PASS했다.
[Astra](reviews/astra-r2.md), [Fable 원문·정정](reviews/fable-r2.md).
Fable R1의 “두 spec 양식이 byte-identical” 주장은 root가 실제 파일과 대조해 정정을 요청했다.
제작판 Skills applied / 사용판 References applied 차이는 의도된 것이다. 모델 리뷰를 사실 검증의
대체로 쓰지 않았으며 원래 보고서도 보존했다. 두 리뷰 모두 실행 실험을 판정한 결과는 아니다.

최종 23개 핵심 파일은 [manifest](reviews/core-final.json)에 실제 해시를 남겼다.
결합 SHA256: f768eeba3fa72203fe8de0e0a004d0bd3fa43023c714eb9a496c8c62ef705379.
연구 § 표기·README 색인·실험/검증 기록·북극성 주석은 이 core 바깥의 전달 기록이다.

## 사용판

`codex/use-template-0023@787af77`은 `codex/use-template-0022@82d7ad2`의 후속이다.
정책 세 문서·spec/plan·선택형 design-spec/plan의 본문/참조·리뷰를 연결했다. PROJECT-POLICY의
기존 운영 행에 공개 권한·설정·수락/중단 기록을 추가했다. README가 새 안내를 연결한다.

별도 사용판에는 활성 .claude 디렉터리, 제작 연구·검증 스크립트·제품 코드·실험 데이터가 없다.
스킬은 `examples/skills`의 실제 선택형 파일로 제공하며 `disable-model-invocation: true`를 유지했다.
영구 설치나 외부 서비스 도입은 이번 변경의 조건이 아니다. 제작판의 기존 프로젝트 스킬은 갱신했다.

실험 baseline은 출처 footer 보강 전 f89a92a에서 파생했다. 787af77까지의 두 파일 차이는 출처·팀 선택
문구이며 실행 지침은 동일하다. 해당 baseline과 초기 입력·파생 작업을 [F03 기록](probe/README.md)에
보존한다. 메인 사용 템플릿으로 실험 코드를 가져오지 않는다.

## 검증 범위

[독립 1차 verifier](reviews/verification/phase1.md): make check PASS, make evals 키 없음 rc2 SKIP,
기존 체인/훅의 인접 확인, 사용판 경계, 실제 스킬 frontmatter·참조를 확인했다. maker의 두 스킬은
공식 quick_validate를 통과했다. 사용판의 Claude 전용 필드를 Codex 검사기의 제한 때문에 삭제하지 않았다.
실제 F03 동작은 [결과](probe/result.md)와 [독립 최종 verifier](reviews/verification/phase2.md)에서
별도 확인했다. 최종 verifier는 PR1·PR2·정리의 7/10/8시험, 직접 OFF/ON·남은 옛 설정·입력 보존,
제어 재사용과 실제 Git 계보를 확인했고 중요한 불일치가 없었다. 23파일은 실제 커밋 blob과도 일치한다.

회귀 범위는 이번 변경의 영향을 따라 정했다. 의도→설계→계획의 수락·개정과 새 세션 인계, PR별 최신
통합과 공개 범위, 선택 스킬 사용, 기존 제품 동작과 검증·리뷰, 공개/중단/제거를 함께 확인했다.
고정 원문·기존 평가 전체를 매번 재채점하지 않았고, 관련 없는 조직별 운영 장치를 실행 성공으로
간주하지 않았다. 원문과 179개 주석 ID·등급·기존 내용은 보존했으며 V4-08/V12-08에 관측만 추가했다.
[원문 보존 대조](reviews/north-star-preservation.json). 새 생산용 스크립트·훅·필수 서비스는 없다.

마지막 원문 로그에는 unified diff의 공백 접두사 등이 있어 전체 git diff --check가 공백 경고를 냈다.
실행 원문을 수정하지 않고 .log만 제외한 문서·양식·스킬 diff 검사를 통과시켰다. 로컬 링크 132개도
모두 유효했다. root의 [최종 자료 대조](reviews/final-artifact-checks.json)는 결합 해시의 직렬화 방식과
재계산 결과를 함께 명시한다. 독립 verifier의 구성 파일별 검증에 더한 일회성 자료 확인이다.
