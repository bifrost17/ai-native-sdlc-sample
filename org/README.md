# org/ — 관리형 설정 비활성 예시

**이 파일은 비활성 예시다** — 적용하려면 조직(Team/Enterprise) 계정의 관리 콘솔이나 MDM 으로
각 기기의 시스템 경로(`managed-settings.json`)에 실제로 배포해야 하고, **이 레포는 그것을 하지
않는다.** `org/managed-settings.example.json` 은 그 배포 대상 파일의 견본일 뿐이며, 이 레포의
어떤 스크립트·훅·CI 도 이 파일을 읽어 적용하지 않는다. `docs/PHASES.md` 레슨 11 행이
「조직 계정이 없어 관리형 설정을 실제로 배포할 대상이 없다」고 적은 것과 같은 이유다.

🔴 **이 파일을 `~/Library/Application Support/ClaudeCode/managed-settings.json` 등
사용자 자신의 관리형 설정 경로에 복사해 넣지 마라.** 견본은 이 레포 예시의 실제 규약(레포 명령·
훅 5개)을 담고 있어 그대로 적용하면 다른 프로젝트의 권한·훅 배선을 덮어쓴다.

## 무엇을 담았나

Anthropic 「The AI-Native SDLC Playbook」레슨 11(관리형 설정 · 마켓플레이스)이 다루는 관리형
전용 키를, 이 레포에 맞춘 값으로 채운 예시다. 원문은 Claude Code 공식 문서
(`https://code.claude.com/docs/en/settings-reference` · `.../managed-settings`, 2026-09-08 판)로
확인했다 — 확인 방법과 원문은 아래 "문서에서 확인한 키" 절 참조.

## 키별 — 무엇을 막는가

| 키 | 무엇을 막는가 | 이 예시에서 쓴 값 |
|---|---|---|
| `permissions.allow` | 묻지 않고 허용할 도구 사용 | 이 레포 명령: `Bash(make check)` · `Bash(make test)` · `Bash(git *)` |
| `permissions.deny` | 비밀 파일 읽기 · 임의 네트워크 접근 | `.env`·`secrets/**`·`~/.aws/credentials` 읽기 차단, `WebFetch` 전체 차단 |
| `permissions.disableBypassPermissionsMode` | `--dangerously-skip-permissions` 및 서브에이전트의 `permissionMode: bypassPermissions` | 문자열 `"disable"`(불리언이 아니다 — 문서 확인 사항) |
| `allowManagedPermissionRulesOnly` | 사용자·프로젝트·로컬 설정의 권한 규칙이 관리형 규칙에 규칙을 더하는 것 | `true` — 이 예시 파일의 `permissions.*` 가 유일한 권한 출처가 된다 |
| `sandbox.enabled` / `sandbox.failIfUnavailable` | Bash 명령의 파일시스템·네트워크 격리, 그리고 샌드박스가 못 뜰 때 무격리로 새는 것 | 둘 다 `true` — 샌드박스 없인 기동 자체를 거부 |
| `sandbox.allowUnsandboxedCommands` | `dangerouslyDisableSandbox` 로 샌드박스를 우회한 재시도 | `false` — "Strict sandbox mode" |
| `sandbox.network.allowedDomains` | 샌드박스 명령이 프롬프트 없이 나갈 수 있는 도메인 | 예시 도메인 3개(`github.com` 등) |
| `sandbox.credentials.files[].mode` | 샌드박스 안에서 자격증명 파일을 읽는 것(`deny`) 또는 실제 값 대신 sentinel 을 보여주는 것(`mask`) | AWS 자격증명은 `deny`, `gh` 호스트 파일은 `api.github.com` 요청에만 실값 대체하는 `mask` |
| `sandbox.credentials.envVars[].mode` | 샌드박스 안에서 환경변수를 보는 것(`deny`) 또는 sentinel 로 가리는 것(`mask`) | `NPM_TOKEN` 은 `deny`, `GITHUB_TOKEN` 은 `api.github.com` 한정 `mask` |
| `allowManagedHooksOnly` | 관리형이 아닌 훅(사용자·프로젝트·로컬·다른 플러그인)의 실행 | `true` — 🔴 아래 "함정" 절 |
| `disableSideloadFlags` | `--plugin-dir`·`--plugin-url`·`--agents`·`--mcp-config` 로 관리 정책을 CLI 플래그로 우회하는 것 | `true` |
| `strictKnownMarketplaces` | 사용자가 추가·설치할 수 있는 플러그인 마켓플레이스 출처 | 조직 소유 GitHub 레포 1개만 허용(플레이스홀더 `your-org/approved-plugins`) |
| `allowManagedMcpServersOnly` | 사용자·프로젝트·로컬 설정이 MCP 서버 허용목록을 넓히는 것 | `true` |
| `requiredMinimumVersion` | 조직이 정한 최저 버전보다 낮은 바이너리의 기동 | `"2.1.150"`(문서 예시와 동일 — 실제 배포 시 조직이 정한 값으로 교체) |

인용은 레슨 11 의 요지를 우리 말로 옮긴 것이고, 정확한 키 의미·스코프·타입은 위 공식 문서
원문이 정본이다(원문은 짧은 축자만 인용하고 전문을 옮기지 않는다).

## 🔴 함정 — `allowManagedHooksOnly` 가 프로젝트 훅을 죽인다

레슨 11 이 경고하는 함정을 이 예시가 실측으로 확인했다: `allowManagedHooksOnly: true` 를 켜면
Claude Code 는 **관리형 설정과 Agent SDK 가 등록한 훅만** 실행하고, **사용자·프로젝트·로컬
설정의 훅은 전부 차단한다.** 공식 문서(`settings-reference#what-runs-under-allowmanagedhooksonly`)
원문: *"Everything else is blocked: user, project, and local hooks, hooks from other plugins, and
hooks declared in agent frontmatter."*

이 레포의 승인 게이트(`.claude/settings.json` 이 배선하는 훅 5개 — `protect-accepted.sh` ·
`protect-tests.sh` · `no-secrets.sh` · `plan-sync.sh` · `production-gate.sh`, 설계안 §6.1)는
프로젝트 설정 파일에 있다. 그래서 이 예시 파일의 `hooks` 블록에 **같은 5개를 관리형 쪽에
다시 정의했다** — `allowManagedHooksOnly` 를 켜면서 프로젝트 훅을 그대로 잃는 실수를 막으려면
관리형 파일 자신이 그 훅들을 등록해야 한다. 경로는 `.claude/hooks/*.sh` 그대로 유지했다(관리형
설정이 배포되는 기기에서도 같은 레포 체크아웃을 전제하기 때문 — 실제 배포에서는 조직이 이
경로 전제가 유효한지 스스로 검증해야 한다).

`tests/test_managed_settings.sh` 케이스 ③이 이 불변식(`allowManagedHooksOnly=true` 면 `hooks`
블록 필수)을 기계로 고정한다 — `hooks` 블록을 지우면 그 케이스가 red 로 운다.

## 문서에서 확인한 키

아래 URL 을 2026-09-08 에 직접 열어 각 키의 이름·타입·스코프·예시를 확인했다 — 재현은
아래 두 URL 을 열어 이 절 끝의 15키 목록이 문서화돼 있는지 직접 대조한다:

- `https://code.claude.com/docs/en/settings-reference.md`
- `https://code.claude.com/docs/en/managed-settings.md`

이 예시 파일이 쓰는 15키 전부(`permissions.deny` · `permissions.allow` ·
`permissions.disableBypassPermissionsMode` · `allowManagedPermissionRulesOnly` ·
`sandbox.enabled` · `sandbox.failIfUnavailable` · `sandbox.allowUnsandboxedCommands` ·
`sandbox.network.allowedDomains` · `sandbox.credentials.files[].mode` ·
`sandbox.credentials.envVars[].mode` · `allowManagedHooksOnly` · `disableSideloadFlags` ·
`strictKnownMarketplaces` · `allowManagedMcpServersOnly` · `requiredMinimumVersion`)를 위
문서에서 확인했다. `hooks` 키는 관리형 전용 키가 아니라 이 레포가 이미 실제로 쓰는
`.claude/settings.json` 배선(설계안 §6.1~6.2, PR `feat/0001-enforcement-hooks`)을 그대로
가져온 것이라 별도 문서 대조가 필요하지 않았다.

**문서에서 확인 못 한 키는 없다** — 15키 전부 위 두 문서에서 이름·타입·예시를 원문으로
확인했고, 확인하지 못한 채로 "있는 척" 넣은 키는 없다.
