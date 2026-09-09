ultracode

# 공통 브리프 — 조직 스킬 세트 (intent-sdlc-skills)

너는 세션 S{N} 이다. 이 레포는 AI-Native SDLC Playbook 을 채택한 한 조직의 스킬 세트를
만드는 곳이고, 네 임무는 스킬 하나 — {SKILL} — 를 구해 오는 것이다.

## 무엇이 제일 중요한가
1. **이미 있고 사람들이 쓰는 적합한 스킬을 찾는 것.** 하나일 필요 없다 — 정책의 다른 조항을
   덮는 스킬 여럿을 함께 채택해도 된다(서로 모순만 없으면).
2. 못 찾거나 조항이 남으면 **직접 설계한다** — 찾은 것들의 좋은 점을 가져와서, 정책 원문을
   전사해서. 설계에도 근거(무엇을 참고했고 왜 그렇게 갈랐는지)를 남긴다.
3. 어느 쪽이든 **트리거되는지 실증**하고, 조사·판단·시험을 문서로 남긴다.

## 읽을 것
- 플레이북(원문): 스킬 레슨 https://academy.claude.com/courses/ai-native-sdlc-playbook/skills-as-institutional-knowledge
  — 경험칙(어떤 지식을 스킬로 쓰고 무엇은 CLAUDE.md/prompt 에 두는가), SKILL.md 의 꼴,
  배포 위치, 트리거 시험, 정책 변경 시 오너 서명, 「스킬은 권고적 통제」. 정책 스킬이 쓰이는
  자리는 spec 레슨 https://academy.claude.com/courses/ai-native-sdlc-playbook/requirements-and-design
  (PO 프롬프트, 적용된 스킬 판 기록). 네 스킬에 해당하는 레슨은 변수 블록에 있다.
  전체 목차 https://academy.claude.com/courses/ai-native-sdlc-playbook
- 변수 블록 docs/work/S{N}-{SKILL}.md — 네 스킬의 범위 · 기준선 · 정책 파일 · 특별 지시.
- policies/{POLICY}.md — 정책의 정본(v0 초안, 오너 서명 대기). 스킬은 이것을 옮긴다. 정책을
  만들거나 고치지 않는다; 모호하면 결정하지 말고 「정책 오너에게 묻는다」에 적는다.
- docs/research/00-method.md — 다른 세션과 결과를 맞추기 위한 최소 약속.
- 템플릿 레포 https://github.com/bifrost17/ai-native-sdlc-sample — 이 스킬 세트가 꽂힐 자리
  (`.claude/skills/`, `.claude/commands/`, `docs/ADOPTING.md` 의 팀 자리).

## 방법은 네가 정한다
어디서 찾을지, 어떻게 평가할지, 얼마나 깊이 볼지는 네 판단이다. 넓은 조사·후보 정독·
적대 검토·초안 병렬 생성이 필요하면 서브에이전트를 써라(예: 후보 발굴 여러 갈래, 후보마다
정독 1명, 채택안을 깨 보는 1명). 단, 판정은 네가 한다. 지켜야 할 것은 셋뿐:
- 실재 확인: 저장소·파일은 열어 본 것만 적는다. 이름을 짐작해 적지 않는다. 없으면 「없음」.
- 라이선스: MIT/Apache/CC-BY 계열만 채택. 불명이면 보류하고 이유를 적는다.
- 조사 시각과 판(sha·태그)을 적는다 — 별 수·갱신일은 그 시각의 값이다.

## 트리거 시험
채택·작성한 스킬마다, 임시 프로젝트에 넣고 관련 과제를 서로 다른 문구로 여러 번(최소 셋)
시켜 매번 로드되는지 본다(헤드리스면 `claude -p … --output-format json` 의 도구 호출 기록).
실패하면 트리거 문장을 고치고 다시. 집합이면 함께 넣고 같은 과제를 한 번 더 시켜 지시가
어긋나지 않는지 본다. 명령·rc·시각·출력 원문을 raw/ 에 남긴다.

## 남길 것 (파일 이름은 이대로 — 더 만드는 것은 자유)
docs/research/{SKILL}/README.md        요약 · 결론(채택 집합 / 직접 설계 / 기각) · 남는 구멍 · 정책 오너에게 묻는다
docs/research/{SKILL}/candidates.md    본 후보 전부: 출처 · 판 · 라이선스 · 사용 신호 · 트리거 문장 · 덮는 조항 · 판정과 이유
docs/research/{SKILL}/coverage.md      정책 조항 × 스킬 행렬(겹침 · 모순 · 빈칸)
docs/research/{SKILL}/trigger-tests.md 문구별 결과 + 집합 충돌 시험
docs/research/{SKILL}/raw/             사본(sha) · 명령 출력 원문
skills/<name>/SKILL.md                 채택분은 원문 유지(수정은 PROVENANCE 에) · 설계분은 정책 조항 번호를 본문에 인용
skills/<name>/PROVENANCE.md            출처 · sha · 라이선스 · 수정 여부 · 설계분이면 참고한 것
docs/decisions/S{N}-{SKILL}.md         결정 1쪽 — 위 research 파일을 인용

## 지키는 것
- 실행하지 않은 명령의 결과, 열지 않은 파일의 내용을 적지 않는다. 확인 못 한 것은 「확인 못 함」.
- 빨간 출력을 그린이라 하지 않는다. 지시받지 않은 파일(다른 세션의 폴더, policies/)을 고치지 않는다.
- 브랜치 lane/S{N}-{SKILL} 에서만(이미 체크아웃돼 있다). 단계마다 커밋, 파일은 이름으로 add.
  끝나면 `gh pr create --base main` 으로 PR 을 열되 머지하지 않는다. PR 본문 = 5줄(채택 집합 ·
  설계분 · 트리거 n/n · 오너 질문 수 · 확인 못 한 것) + 파일 경로.
- 멈출 때: 정책 결정이 필요하다 · 접근에 인증이 필요하다 · 라이선스 불명 → 짐작하지 말고
  README 「정책 오너에게 묻는다」에 적고 PR 을 연다.

## 완료
파일 계약이 다 있고, 채택·설계 스킬마다 트리거 원문이 있고, coverage 의 빈칸마다 이유가
있고, PR 이 열려 있다. 마지막 응답은 PR 번호와 5줄 요약이다.
