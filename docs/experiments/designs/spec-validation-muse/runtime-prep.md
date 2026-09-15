# 0035 spec 검증 Muse 실험 런타임 준비

2026-09-14 읽기 전용 사전 조사. 이 문서는 실행 준비만 다룬다. 모델 호출, 설치, 사용자 전역
설정 변경, 제품/템플릿 수정은 수행하지 않았다. `docs/experiments/`의 추적 문서는 0034가 마지막이고
`0035-*`는 없으므로 다음 실험 번호를 **0035**로 예약한다. 실제 기록 파일을 만들기 직전에 한 번 더
확인하고, 동시 작업이 먼저 0035를 만들었으면 다음 번호로 올린다.

## 확인된 런타임과 모델

- 실행 파일: `/opt/homebrew/bin/opencode`
- CLI: `opencode 1.18.30`
- 2026-09-14 로컬 카탈로그 명령 `opencode models opencode-go --verbose`의 활성 모델:
  `opencode-go/muse-spark-1.3-contributor` (`Muse Spark 1.3 Contributor`)
- 같은 metadata의 `variants.xhigh.reasoningEffort`는 `xhigh`다. 이는 현재 카탈로그·요청 가능성의
  근거이며 실제 호출 근거가 아니다. 실행 뒤 session export의 provider/model/variant와 각 assistant
  message를 따로 대조한다. 이전 0027에서는 parent가 xhigh로 기록됐지만 native child export의
  variant가 `default`였으므로, child 설정의 `reasoningEffort=xhigh`만으로 실제 variant를 단정하지 않는다.
- 현재 1.18.30 SDK의 `AgentConfig.variant`와 [공식 agent model 안내](https://opencode.ai/v2/docs/agents#model)는
  agent의 기본 variant를 별도 필드로 둔다. read-only probe에서 `agent.general.variant`와
  `agent.sdlc-verifier.variant`를 `xhigh`로 설정하자 `debug config`와 두 `debug agent`가 모두
  `variant: xhigh`를 반환했다. 따라서 child에는 `reasoningEffort` 대신 `variant`를 명시한다.
- 현재 CLI는 `run --dir --format json --model --variant --agent --session`, `export <sessionID>`와
  `export --sanitize`를 지원한다. provider 연결 상태를 바꾸거나 `models --refresh`를 실행하지 않았다.

재확인 명령은 비밀 값을 출력하지 않는 아래 범위로 제한한다.

```bash
command -v opencode
opencode --version
opencode run --help
opencode export --help
opencode models opencode-go --verbose \
  | awk '/opencode-go\/muse-spark-1\.3-contributor/{show=1;n=0} show{print;n++} show&&n>=95{exit}'
```

## 고정 경로와 격리

HUMAN 전용 prompt, 정답표, 채점과 전체 결과는 제품 밖에 둔다.

```bash
MUSE_MAKER=/Users/jake/Projects/ai-native-sdlc-sample
MUSE_PRIVATE=/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse
MUSE_PRODUCTS=/Users/jake/Projects/ai-native-sdlc-spec-validation-muse-20260914
MUSE_BASELINE_REV=fa76b89512c181d9c525341727bbfb78a06e1021
MUSE_IMPROVED_REV='<root가 구현·정적 검증 후 고정한 전체 SHA>'
```

`MUSE_BASELINE_REV`는 설계 문서가 밝힌 출발판이며 활성 선택형 패키지는 0.1.5다. 개선판은 root가
구현 뒤 새 SHA와 package version을 고정한다. 기준/개선마다 별도 디렉터리와 새 Git 이력을 쓰고,
같은 완전한 입력 packet을 복사하되 검토 지침 판만 바꾼다. 제품에는 원인 보고서, F1/F2 정답표,
HUMAN 판정이나 다른 실행 결과를 넣지 않는다. provider 자격은 기존 사용자 연결을 읽기만 해야 하므로
임시 `HOME`/`XDG_CONFIG_HOME`로 바꾸지 않는다. 대신 `--dir`을 항상 명시하고 프로젝트
`opencode.json`에서 `external_directory`, web, push/merge, 중첩 `opencode`/`claude`를 deny한다.
`--auto`, `--share`, `models --refresh`는 사용하지 않는다.

제품 root 생성은 root가 만든 packet 경로를 정한 뒤 아래처럼 수행한다. `git archive`는 maker의
고정 Git 객체만 읽고, 대상이 이미 있으면 중단한다.

```bash
set -eu
mkdir -p "$MUSE_PRIVATE/prompts" "$MUSE_PRIVATE/raw" "$MUSE_PRODUCTS"
for lane in baseline-r1 improved-r1 small-r1 boundary-r1; do
  test ! -e "$MUSE_PRODUCTS/$lane"
done
mkdir "$MUSE_PRODUCTS/baseline-r1" "$MUSE_PRODUCTS/improved-r1" \
  "$MUSE_PRODUCTS/small-r1" "$MUSE_PRODUCTS/boundary-r1"

git -C "$MUSE_MAKER" archive "$MUSE_BASELINE_REV:tdd-optional/project" \
  | tar -x -C "$MUSE_PRODUCTS/baseline-r1"
git -C "$MUSE_MAKER" archive "$MUSE_IMPROVED_REV:tdd-optional/project" \
  | tar -x -C "$MUSE_PRODUCTS/improved-r1"
for lane in small-r1 boundary-r1; do
  git -C "$MUSE_MAKER" archive "$MUSE_IMPROVED_REV:tdd-optional/project" \
    | tar -x -C "$MUSE_PRODUCTS/$lane"
done
for lane in baseline-r1 improved-r1 small-r1 boundary-r1; do
  git -C "$MUSE_PRODUCTS/$lane" init -b main
  git -C "$MUSE_PRODUCTS/$lane" add .
  git -C "$MUSE_PRODUCTS/$lane" commit -m "Seed 0035 spec validation $lane"
done
```

위 명령 전에 각 대상 디렉터리는 `mkdir`로 비어 있게 만들어야 한다. 구현 시에는 한 번에 처리하는
작은 setup script가 더 안전하며, 기존 `/Users/jake/Projects/ai-native-sdlc-experiment-private/0029-optional-opencode/setup.py`
의 `git archive` → 독립 Git root → package 복사 → patch dry-run/apply → discovery 기록 순서를 재사용한다.

## 선택형 OpenCode 스킬 전달

현재 정본 명령은 `tdd-optional/org-skills/opencode/README.md`의 프로젝트별 설치다. 각 lane의
package는 해당 lane과 같은 revision에서 따로 archive해 고정한다. 11개 native 스킬, 수동 자료 2개,
verifier를 복사하고 `sdlc-feedback`, `ux-copy` patch를 적용한다. 이번 spec 작성/검토 흐름은 작성
예시도 명시 채택하므로 세 예시를 복사하고 `authoring-native.patch`를 적용한다.

```bash
OC_PACKAGE="$MUSE_PRIVATE/package-improved"
OC_TARGET="$MUSE_PRODUCTS/improved-r1"
mkdir "$OC_PACKAGE"
git -C "$MUSE_MAKER" archive "$MUSE_IMPROVED_REV:tdd-optional/org-skills" | tar -x -C "$OC_PACKAGE"

(
  set -eu
  test -f "$OC_PACKAGE/.claude-plugin/plugin.json"
  test ! -e "$OC_TARGET/.opencode/skills"
  test ! -e "$OC_TARGET/.opencode/agents/sdlc-verifier.md"
  test ! -e "$OC_TARGET/team-resources"
  mkdir -p "$OC_TARGET/.opencode/skills" "$OC_TARGET/.opencode/agents" "$OC_TARGET/team-resources/skills"
  for skill in brand data-compliance secure-api-review spec-policy-pass tdd stop-slop-ko accessibility secrets-scan grilling sdlc-feedback ux-copy; do
    cp -R "$OC_PACKAGE/skills/$skill" "$OC_TARGET/.opencode/skills/$skill"
  done
  for skill in to-questionnaire pr-loop; do
    cp -R "$OC_PACKAGE/skills/$skill" "$OC_TARGET/team-resources/skills/$skill"
  done
  cp "$OC_PACKAGE/opencode/agents/sdlc-verifier.md" "$OC_TARGET/.opencode/agents/sdlc-verifier.md"
  cp "$OC_PACKAGE/opencode/team-resources/INDEX.md" "$OC_TARGET/team-resources/INDEX.md"
  patch --batch --dry-run -d "$OC_TARGET/.opencode/skills/sdlc-feedback" -p1 < "$OC_PACKAGE/opencode/patches/sdlc-feedback.patch"
  patch --batch -d "$OC_TARGET/.opencode/skills/sdlc-feedback" -p1 < "$OC_PACKAGE/opencode/patches/sdlc-feedback.patch"
  patch --batch --dry-run -d "$OC_TARGET/.opencode/skills/ux-copy" -p1 < "$OC_PACKAGE/opencode/patches/ux-copy.patch"
  patch --batch -d "$OC_TARGET/.opencode/skills/ux-copy" -p1 < "$OC_PACKAGE/opencode/patches/ux-copy.patch"
  mkdir -p "$OC_TARGET/.claude/skills"
  for skill in capture-intent design-spec plan; do
    test -f "$OC_TARGET/examples/skills/$skill/SKILL.md"
    cp -R "$OC_TARGET/examples/skills/$skill" "$OC_TARGET/.claude/skills/$skill"
  done
  patch --batch --dry-run -d "$OC_TARGET/.claude/skills" -p1 < "$OC_PACKAGE/opencode/patches/authoring-native.patch"
  patch --batch -d "$OC_TARGET/.claude/skills" -p1 < "$OC_PACKAGE/opencode/patches/authoring-native.patch"
)
```

기준 lane은 같은 명령에서 `MUSE_BASELINE_REV`와 별도 `package-baseline`을 사용한다. 복사 뒤 source
revision, manifest version, patch stdout/rc, 설치 파일 SHA-256을 private installation manifest에
남긴다. `opencode debug skill`과 `opencode debug agent sdlc-verifier`의 정리된 JSON으로 실제 경로,
본문, 최종 model/steps/permission을 확인한다. 전역/상위의 동명 스킬이 섞이면 호출 전에 중단한다.

```bash
(cd "$OC_TARGET" && opencode --pure debug skill) > "$MUSE_PRIVATE/improved-skills.json"
(cd "$OC_TARGET" && opencode --pure debug agent sdlc-verifier) > "$MUSE_PRIVATE/improved-verifier.json"
```

프로젝트 `opencode.json`에는 최소한 아래 실행 경계를 둔다. verifier의 model도 동일하게 고정하되
실제 child variant는 export로 다시 확인한다.

```json
{
  "model": "opencode-go/muse-spark-1.3-contributor",
  "agent": {
    "general": {
      "model": "opencode-go/muse-spark-1.3-contributor",
      "variant": "xhigh"
    },
    "sdlc-verifier": {
      "model": "opencode-go/muse-spark-1.3-contributor",
      "variant": "xhigh"
    }
  },
  "permission": {
    "external_directory": "deny",
    "webfetch": "deny",
    "websearch": "deny",
    "skill": {"*": "allow", "aside-browser": "deny", "customize-opencode": "deny"},
    "bash": {
      "*": "allow",
      "git push*": "deny",
      "git merge*": "deny",
      "curl *": "deny",
      "wget *": "deny",
      "opencode *": "deny",
      "claude *": "deny"
    }
  }
}
```

## 실행·세션·출력 보존

검증된 public transport는
`docs/research/opencode-compatibility/experiment/run-opencode.py`다. 같은 파일의 고정 사본이
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0027-muse-larger/run-opencode.py`에 있고,
`export-opencode.py`도 양쪽에 있다. runner는 prompt 하나만 전달하고 `--format json`의 공개 event만
새 `.jsonl`에 기록하며 reasoning/signature/encrypted 항목을 버린다. stderr와 요청 모델/variant,
session ID, 시간, rc, timeout, event 수를 각각 `.stderr.txt`와 `.meta.json`에 남긴다.

실험용 사본을 먼저 만들고 SHA-256을 기록한다. prompt와 output stem은 매 호출 새 이름을 써야 한다.
runner는 `.jsonl` 덮어쓰기만 막으므로 같은 stem을 재사용하지 않는다.

이번 통제 비교에는 **private 사본의 최소 보정**을 권한다. runner의 `cmd`에 `--pure`를 추가해 외부
plugin을 끄고, exporter의 명령을 `opencode export --pure --sanitize <session>`으로 바꾼 뒤 두 사본의
diff와 SHA-256을 setup 기록에 남긴다. 프로젝트 native skill과 agent는 product root에서 계속 읽는다.
보정 뒤 `debug skill` 결과가 예상한 14개 프로젝트 스킬만 가리키는지 확인하고, provider/model을 찾지
못하면 모델 호출 전에 중단한다. 보정하지 않으면 전역 external plugin의 비개입을 주장할 수 없다.

```python
# run-opencode.py의 기존 cmd
cmd = ["opencode", "run", "--pure", "--dir", a.cwd, "--format", "json", ...]

# export-opencode.py의 기존 read_pty 호출
raw = read_pty(["opencode", "export", "--pure", "--sanitize", args.session], cwd, args.timeout)
```

```bash
cp "$MUSE_MAKER/docs/research/opencode-compatibility/experiment/run-opencode.py" "$MUSE_PRIVATE/run-opencode.py"
cp "$MUSE_MAKER/docs/research/opencode-compatibility/experiment/export-opencode.py" "$MUSE_PRIVATE/export-opencode.py"
shasum -a 256 "$MUSE_PRIVATE/run-opencode.py" "$MUSE_PRIVATE/export-opencode.py"

python3 "$MUSE_PRIVATE/run-opencode.py" \
  --cwd "$MUSE_PRODUCTS/baseline-r1" \
  --prompt "$MUSE_PRIVATE/prompts/01-baseline.prompt.txt" \
  --out "$MUSE_PRIVATE/raw/01-baseline" \
  --model opencode-go/muse-spark-1.3-contributor \
  --variant xhigh --agent build --timeout 600
```

같은 lane의 후속 메시지만 metadata의 단일 `session_ids[0]`를 확인한 뒤 이어 간다.

```bash
MUSE_SESSION='<직전 meta의 유일한 session id>'
python3 "$MUSE_PRIVATE/run-opencode.py" \
  --cwd "$MUSE_PRODUCTS/boundary-r1" \
  --prompt "$MUSE_PRIVATE/prompts/05-boundary-followup.prompt.txt" \
  --out "$MUSE_PRIVATE/raw/05-boundary-followup" \
  --model opencode-go/muse-spark-1.3-contributor \
  --variant xhigh --agent build --session "$MUSE_SESSION" --timeout 600
```

완료 세션은 sanitized helper로 공개 export한다. 입력 packet과 tool output에도 비밀을 넣지 않는다.
helper의 문자열 필터는 Bearer 형식과 reasoning 계열만 다루므로 임의 API key 패턴의 완전한 유출 방지
장치로 해석하지 않는다.

```bash
python3 "$MUSE_PRIVATE/export-opencode.py" \
  --cwd "$MUSE_PRODUCTS/boundary-r1" \
  --session "$MUSE_SESSION" \
  --out "$MUSE_PRIVATE/raw/05-boundary.public.json" --timeout 30
```

각 호출 뒤 `.meta.json`의 `exit_code == 0`, `timed_out == false`, `invalid_line_count == 0`,
`error_events == 0`, session ID와 event 수를 확인한다. rc0는 검토 내용 PASS가 아니다. 공개 export의
session model과 assistant provider/model/variant, child session 반환·부모 대기, 실제 읽은 스킬 경로를
판정과 별도로 기록한다.

## 호출 상한과 중단

설계의 기본 요청은 기준 r1, 개선 r1, 작은 충분 spec, 합성 경계 parent+child로 총 5 model 호출이다.
중요 누락이 있을 때만 최소 수정 후 영향 사례를 새 branch/session에서 한 번 재시험한다. parent와 child를
포함한 모든 참가 agent 합계 **최대 6호출, 총 30분**이며 먼저 닿는 상한에서 새 호출을 시작하지 않는다.
개별 root CLI는 600초 timeout으로 둔다. timeout/오류/부분 결과를 PASS로 바꾸지 않고 보존한다.

기준과 개선 모두 같은 Muse/xhigh, 완전한 설계 입력, 참조, 요청 범위를 쓴다. 바꾸는 것은 검토 지침
revision뿐이다. 수정 뒤 재시험은 최초 결과를 보존하고 영향 사례만 새 Git branch와 새 session에서 한다.
기준도 결함을 찾을 수 있으며, 이 작은 비교를 모델 실패율·일반 탐지율·전체 SDLC 통과로 확대하지 않는다.
