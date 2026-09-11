# 제작 원본과 실제 사용 후보의 대응

2026-09-11. 이번 변경은 제작 브랜치 `codex/spec-template-design`과 실제 사용 후보
`codex/use-template-0021`에 각각 보존했다. 사용 후보는 `codex/use-template-0017@add296d`에서
파생했으며 원래 분기를 바꾸거나 제품 실험 브랜치를 제작 main으로 합치지 않았다.

| 판 | maker | adopter | 의미 |
|---|---|---|---|
| 직전 기준 | a734b29 | add296d | 완료된 intent 설계 / 기존 사용 후보 |
| 사용 후보 준비 | ac0963b의 합성 입력 | dbfd371 | intent 양식·선택 지침·입력 예시 전달 |
| R1 | 4f52028 | 3e2f693 | 같은 내용의 첫 검토 후보 보존. 실패 발견을 포함한 이력 |
| R2 | efc65d9 | ca87cdb | 복구 계약·검증 범위 등 리뷰 수정. 같은 후보 파일의 독립 재검토 대상 |

개별 33파일과 결합 해시는 [R2 영수증](reviews/candidate-r2.json)에 있다. 영수증의 base_heads는
R2 작성 직전 R1 HEAD이며 최종 R2 파일은 위 커밋에서 조회할 수 있다. 이후 제작 브랜치의
리뷰·실험 기록·색인·주석 커밋은 이 33개 핵심 파일을 바꾸지 않는다.

- intent 양식은 직전 maker에서 검토한 바이트를 전달했다. 사용판 capture-intent 선택 지침에도
  제안 보존·미확인 구별·없는 수치나 담당자 비발명·비례적 질문을 반영했다.
- spec 양식은 참조 메타데이터만 `Skills applied` 대신 `References applied`다.
  기능·버그·이행 예시는 실제 상류 commit과 해당 참조 문장만 다르며 나머지 본문은 같다.
  입력 intent/context와 design-depth는 동일하다.
- 사용판 지침은 `examples/skills/`에 있는 선택 예시이고 `disable-model-invocation: true`를
  유지한다. 팀의 실제 정책·선택 자료를 쓰며 maker의 조직 플러그인이나 검사기를 요구하지 않는다.
- adopter에는 제작 연구·평가·하네스·원시 리뷰·제품 실험 코드가 없다. 기존 GitHub Flow와 PR 크기,
  plan 양식·선택 예시는 유지했다. 사용판의 이행 예시는 제품용 DB 프로그램을 추가한 것이 아니다.

부분 대화는 `codex/exp-0021-spec-handoff`에 별도로 보존했다. 초기 R1 조건에서 생성·리뷰하고
R2 자료를 `a2908b1`에 전달한 뒤 마지막 인계를 대조했다. [실험 기록](probe/README.md)의 한계를 따른다.

이 작업은 로컬 브랜치와 커밋까지다. 호스티드 PR·merge·운영 배포나 새 플러그인 영구 설치는 하지 않았다.
