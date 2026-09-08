# 승인 게이트로서의 훅 (hooks-as-approval-gates)

> 플레이북에서: 차단은 스스로를 설명해야 한다 — "A block should explain
> itself". 에이전트는 프로덕션 게이트까지 가되 그 게이트를 넘지는 못한다.
> 출처: 레슨 11.

## 이 레포에서 무엇이 강제되나
- `.claude/hooks/production-gate.sh`(PreToolUse·matcher `Bash`, PR #6
  대기)가 `scripts/deploy.sh … production` 계열 명령을 토큰 단위(세그먼트별
  대입·`--env=production` 값부 포함, `docs/production-notes.md` 같은 부분
  문자열은 제외)로 판정해, `RELEASE_APPROVAL` 환경변수가 공백이 아니면
  통과, 없거나 같은 명령줄의 인라인 대입(자기 승인)이면 exit 2 로 차단하고
  사유+승인 경로를 stderr 에 낸다.
- `scripts/deploy.sh`(PR #6, 대기) 자체가 그 차단 대상 — 실제 배포 대신
  흉내만 낸다(설계안 비목표: 배포 대상 없음).
- `org/managed-settings.example.json`(관리형 설정 예시)은 main 엔 아직
  없고 PR #11 이 들고 있다(대기) — `docs/DESIGN.md` §6.3·§8 은 이를 레슨
  11 의 「구현」 근거로 적고 `docs/PHASES.md`(PR #3)도 같은 행에서 "예시
  파일만 비활성으로 둠"이라 적어 파일이 있다고 전제하는데, 그 전제는 PR
  #11 이 머지될 때 비로소 참이 된다.

## 증거는 무엇인가
- `tests/test_hooks.sh`(PR #6, 대기)의 production-gate 관련 `expect` 단정
  (RELEASE_APPROVAL 공백값·인라인 대입·`--dry-run=false` 같은 무해 인자
  포함, 전체 79건 중 일부).

## 어디에 기록되나
- 훅이 차단한 stderr 메시지(승인 경로 안내) · 통과된 배포는 승인 근거를
  PR 본문/커밋에 남기라고 훅 메시지가 요구한다(자동 기록은 아니다).

## 누가 승인하나
- 사람 — 배포 승인권자가 세션 환경에 `RELEASE_APPROVAL` 값(변경 승인
  번호·PR 링크)을 넣는다. 조직 배포(`allowManagedHooksOnly` 등)는 이월
  원장에 있다(아래).

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `.claude/hooks/production-gate.sh` | 대기(PR #6) | `.claude/hooks/production-gate.sh` |
| `scripts/deploy.sh` | 대기(PR #6) | `scripts/deploy.sh` |
| `.claude/settings.json`(PreToolUse 배선) | 대기(PR #6) | `.claude/settings.json` |
| `tests/test_hooks.sh` | 대기(PR #6) | `tests/test_hooks.sh` |
| `org/managed-settings.example.json` | 대기(PR #11) | `org/managed-settings.example.json` |

## 이 플레이에서 우리가 하지 않는 것
- 관리형 설정 MDM 배포 · 플러그인 마켓플레이스는 안 한다 — `docs/PHASES.md`
  (PR #3): 조직(Team/Enterprise) 계정이 없어 배포할 대상이 없음, 승격
  조건은 「조직(Team/Enterprise) 계정」. (PHASES 의 "예시 파일만 비활성으로
  둠" 이라는 부기는 위에서 실측한 대로 그 파일이 없어 지면 정정 대상이다.)
