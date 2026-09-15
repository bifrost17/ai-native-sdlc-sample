# T03 — 설치·자료 동등성 확인

2026-09-15 / Asia/Seoul. 대상은 0027 SP02/03의 `tdd-optional` 0.1.8 작업 사본이다.
원본 출력·절대 경로·파일별 SHA-256은 [parity-installation.json](parity-installation.json)에 둔다.
이 기록은 패키지 설치·자료 전달 확인이며 실제 모델의 스킬 사용 판정은 아니다.
최종 실행은 PASS다. 16개 스킬의 파일별 비교와 설치·패치·보존 확인을 통과했다.

## 변경

- `org-skills/claude/README.md`에 프로젝트 작성 3개와 팀 플러그인 13개의 설치·갱신·명시 호출을 분리했다.
  기존 공통 정본을 그대로 사용하고 폴더 전체·동반 자료·검증자 기준의 출처를 설명했다.
- Codex에 `pr-loop.patch`를 추가해 Claude 입력·선실행·도구 목록 문법을 현재 요청과 실제 도구 호출로
  바꿨다. `Team settings`부터 끝까지의 작업·보호·종료 규칙은 원문과 동일하다.
- Codex 설치 안내의 입력 사전 확인, 명시 호출, 이전→새 소스 변경 병합을 보완했다.
  두 도구 모두 로컬 정책·참고 자료를 보존한다. OpenCode의 기존 변환 범위는 유지했다.
- 배포판과 패키지 manifest, 현재 설치 안내를 0.1.8로 맞췄다. 이전 버전 설명과 실행 근거는 역사로 유지했다.

## 실행 방법과 범위

`tempfile.mkdtemp(prefix="sdlc-parity-0027-")` 아래에 세 제품을 만들었다. 각각 `project/` 전체를
복사하고 `git init -q`를 실행했다. 각 README의 bash 블록을 추출해 절대 경로 예시만 임시 경로로
바꿔 실행했다. Claude에는 비어 있는 별도 `CLAUDE_CONFIG_DIR`과
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`을 지정하고 API/OAuth 환경 토큰을 전달하지 않았다.
실제 사용자 프로필의 플러그인을 설치·갱신하거나 전역 스킬을 변경하지 않았다.

Claude Code 2.1.269에서 strict manifest 검사, 프로젝트 범위 marketplace add/install/list를
실행했다. 목록과 설치 manifest의 버전 0.1.8·project 범위·캐시 경로를 확인했다.
작성 폴더는 별도로 복사했다. Claude 팀 13개 캐시 폴더와 작성 3개는 공통 원본과 파일별로 같았다.
채택 제품의 기존 파일 해시도 보존됐다. 작성 폴더 재설치는 실패로 중단하고 기존 파일을 보존했다.

Codex CLI 판은 0.153.4다. 네 patch를 적용하고 16개 폴더의 원본 동반 자료를 비교했다.
네 명시 전용 스킬은 `allow_implicit_invocation: false`를 확인했다. `skill-creator`의
`quick_validate.py`로 16개 Codex 설치 스킬을 검사했다. 재설치는 실패로 중단하고 설치본을 보존했다.

OpenCode의 팀 11개 native·2개 자료 폴더와 선택 작성 3개를 기존 명령으로 복사했다.
기존 세 patch가 적용됐고 자료를 보존했다. `ux-copy/PROVENANCE.md`의 기존 어댑터 안내 추가만
동반 자료 원문 비교에서 구별했다. OpenCode 런타임·모델은 실행하지 않았다.

Claude와 OpenCode의 `Review criteria` 전문은 같다. Codex 전문은 프로젝트 진입 파일 목록에
`AGENTS.md`를 추가한 기존 변환 외에 같다. `pr-loop`의 Claude 전용 문법 제거와
`Team settings` 이후 동일성을 확인했다. 실제 PR 조회·수정·push·댓글은 수행하지 않았다.

## 확인 중 보정과 한계

첫 실행은 시스템 Python 3.9에 `tomllib`이 없어 시작되지 않았다. 증거 추출을 표준 문자열 처리로
바꾸었다. 이후 두 실행은 `quick_validate.py`가 요구하는 PyYAML이 선택한 Python에 없어 중단됐다.
이미 설치된 uv 캐시 환경의 Python/PyYAML을 확인해 사용했으며 새 패키지를 설치하지 않았다.
설치·패치 자체의 실패는 아니었다. 자료 비교의 첫 기대는 OpenCode의 기존 provenance 추가까지
원문 일치를 요구해 실패했고, 기준 비교는 기존 `AGENTS.md` 표기를 백틱으로 잘못 예상해 실패했다.
실제 어댑터 변환 범위를 읽고 비교 기대를 고쳤다. 제품 기준이나 어댑터를 시험에 맞춰 약화하지 않았다.

최종 파일 해시와 CLI 설치 목록은 스킬 발견·본문 읽기·행동 준수·검증자의 실제 위임과 대기를
입증하지 않는다. 유료 모델 턴·자연 선택·명시 Skill 실행·전체 개발 실험은 이번 범위에서 실행하지 않았다.
공식 문법은 [Claude 스킬](https://code.claude.com/docs/en/skills),
[Claude 설정](https://code.claude.com/docs/en/settings),
[OpenAI 스킬](https://developers.openai.com/codex/skills/) 문서와 로컬 CLI 도움말을 대조했다.
