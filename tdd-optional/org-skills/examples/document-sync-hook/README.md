# 선택 설치: 커밋의 문서 포함 확인

기존 개발 세션이 `sdlc-feedback` 기준으로 이번 diff와 관련 문서를 확인하고, Git hook은 그 판단에서
필요하다고 선언한 문서가 실제 커밋 대상에 포함됐는지 확인한다. Codex·Claude Code에 같은 파일을 쓴다.
팀 스킬이나 제품 템플릿을 복사하는 것만으로 활성화되지 않는다. Git과 Python 3.8 이상이 필요하다.

훅은 스킬을 호출하거나 판단을 대신하지 않는다. 별도 모델·네트워크·영구 기록·자동 stage는 없다.
동기화가 필요한지, 개정 내용이 맞는지, 실제로 검토했는지는 기존 세션의 책임이다. 거짓 빈 목록,
신호만 재계산, 미설치/제거·`--no-verify`를 막지 못한다. 신호는 서명이나 검토 인증서가 아니다.
훅 통과를 시험·수락·통합·전체 완료로 보고하지 않는다.

## 저장소별 설치

기존 Git hook과 `core.hooksPath`를 먼저 확인한다. 아래는 **설정된 hooksPath나 동명 파일이 없는**
저장소의 수동 선택 설치 예시다. 기존 경로나 관리 설정이 있으면 멈추고 그 팀의 기존 hook에 호출을
통합한다. 덮어쓰기·전역 설정 변경·새 hooksPath 설정을 이 예시에 포함하지 않는다. linked worktree는
hooks 디렉터리를 공유할 수 있으므로 저장소의 다른 worktree에도 영향을 주는 설치인지 확인한다.

```sh
HOOK_SOURCE=/absolute/path/to/org-skills/examples/document-sync-hook
PRODUCT_ROOT=/absolute/path/to/adopted-product
(
  set -eu
  cd "$PRODUCT_ROOT"
  git rev-parse --show-toplevel
  if git config --get core.hooksPath >/dev/null; then
    echo '기존 hooksPath가 있습니다. 현재 팀의 설치 방식으로 연결하세요.' >&2
    exit 1
  fi
  HOOK_TARGET=$(git rev-parse --git-path hooks)
  test -f "$HOOK_SOURCE/pre-commit"
  test -f "$HOOK_SOURCE/document_sync.py"
  for name in pre-commit document_sync.py; do
    test ! -e "$HOOK_TARGET/$name"
    test ! -L "$HOOK_TARGET/$name"
  done
  mkdir -p "$HOOK_TARGET"
  cp "$HOOK_SOURCE/pre-commit" "$HOOK_TARGET/pre-commit"
  cp "$HOOK_SOURCE/document_sync.py" "$HOOK_TARGET/document_sync.py"
  chmod +x "$HOOK_TARGET/pre-commit"
)
```

`README.md`도 팀이 사용하는 기존 개발 안내에서 찾을 수 있게 보존한다. 설치본의 두 실행 파일과
원본 해시·source 판을 남긴다. 갱신은 이전→새 source 차이와 설치본의 로컬 변경을 비교해 필요한
부분만 병합한다. 다른 hook이나 제품 정책을 새 패키지로 덮지 않는다. Python 실행 파일이 `python3`와
다르면 커밋 명령의 `SDLC_PYTHON`에 실제 Python 3 실행 파일 경로를 전달할 수 있다. 명령 문자열은 받지 않는다.

## 커밋 전 사용

1. 기존 feedback 기준으로 **실제 staged 변경**을 plan 작업·설계·요구와 대조한다. 관련 unstaged/
   untracked 내용도 읽되 무관한 WIP는 stage하지 않는다. 작은 수정은 짧게 확인하며 매 커밋 새 verifier를
   호출하지 않는다. 의미 있는 인도의 최종 검토는 기존 절차대로 별도로 한다.
2. 바뀐 계약/계획의 관련 문서를 갱신하고 이번 커밋에 필요한 부분을 stage한다. 이미 수락·커밋한 상류
   문서는 형식적으로 다시 고치지 않는다. 부분 stage의 내용이 충분한지는 staged diff/blob을 읽고 판단한다.
3. 최종 staged 범위를 확인한 뒤 `snapshot`과 필요한 `documents`를 JSON으로 전달한다.

아래는 필수 plan 개정을 포함하는 **입력 예시**다. 실제 경로·커밋 메시지로 바꾸고 기존 의미 검토 후 실행한다.

```sh
SDLC_DOC_SYNC=$(python3 - <<'PY'
import json, subprocess
from pathlib import Path
hook_dir = subprocess.check_output(['git', 'rev-parse', '--git-path', 'hooks'], text=True).strip()
snapshot = subprocess.check_output(['python3', str(Path(hook_dir) / 'document_sync.py'), 'snapshot'], text=True).strip()
print(json.dumps({'snapshot': snapshot, 'documents': ['changes/0002-example/plan.md']}))
PY
) git commit -m 'fix(example): 변경 결과'
```

문서 개정이 필요 없다는 판단이면 `documents`를 `[]`로 전달한다. 이를 위해 spec/plan에 의미 없는
수정을 만들지 않는다. 의미 있는 판단의 이유·검증은 기존 대화·커밋/PR 기록에 남긴다. 값은 `export`나
셸 초기화 파일에 저장하지 않고 커밋 한 번에 전달한다. 소비 여부를 저장하는 일회용 토큰은 아니므로
같은 HEAD·같은 staged 범위에 재사용하는 것까지 막지 않는다.

## 검사 계약과 복구

`document_sync.py snapshot`은 현재 HEAD(첫 커밋은 unborn)와 `git ls-files --stage -z`의 mode·object ID·
stage·경로 엔트리와 실제 cached 변경 경로 집합을 묶은 SHA-256 한 줄을 출력한다. diff 표시 설정과 unstaged `.gitattributes`는
지문에 넣지 않는다. raw index의 stat cache도 제외한다. intent-to-add가 있으면 엔트리 지문에는
포함되며, intent-to-add에서 실제 추가로 바뀌면 변경 경로 집합도 달라져 지문이 바뀐다. 문서 변경 포함은
실제 cached diff 경로로 확인한다. `check`는 `SDLC_DOC_SYNC` JSON의
정확히 두 필드를 확인한다.

| 필드 | 의미 |
|---|---|
| `snapshot` | 검토한 HEAD+staged 범위의 지문. 현재 대상과 달라지면 다시 확인한다. |
| `documents` | 이번 커밋에 동반해야 하는 개정의 저장소 상대 경로 목록. 빈 배열 허용. |

기존 `intent/`, 설계 하위 문서, 공백·한글 경로를 사용할 수 있다. 새 문서/삭제/이동은 실제 staged
변경 경로를 선언한다. 경로 escape·glob·중복·잘못된 타입은 오류다. 신호 누락/불량·지문 불일치·
선언 문서 미포함이면 오류를 읽고 기존 세션에서 검토·보완 후 재시도한다. helper는 Git이 전달한
`GIT_INDEX_FILE`을 사용한다. path-limited/`-a` 커밋의 대상이 일반 index와 달라지면 그 실제 범위를
확인해야 한다. 훅은 자동 재시도하지 않는다.

부분 stage와 무관한 worktree 편집은 그대로 둔다. 문서 경로가 들어 있어도 필요한 본문이 빠진 경우,
검토 뒤 worktree만 바뀐 의미 영향이나 동시 index 수정은 기계적 포함 확인으로 해결되지 않는다.
커밋 후 실제 내용 확인을 유지한다. 이 예시의 설치·Git fixture 시험은 실제 에이전트의 자연스러운
검토·실패 뒤 보완 행동과 별도 근거다.
