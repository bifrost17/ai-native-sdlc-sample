# org/ — 관리형 설정 비활성 예시
<!-- TEAM: real managed-settings deployment (MDM/admin console) — docs/ADOPTING.md · L19 -->

**비활성 예시다.** 적용하려면 조직(Team/Enterprise) 관리 콘솔이나 MDM 이 각
기기의 `managed-settings.json` 에 실제로 배포해야 하고, 이 레포는 그것을 하지
않는다 — 어떤 스크립트·훅·CI 도 `org/managed-settings.example.json` 을 읽지
않는다. 조직 계정이 없어 배포 대상이 없기 때문이다.

🔴 이 파일을 자신의 관리형 설정 경로(`~/Library/Application Support/ClaudeCode/
managed-settings.json` 등)에 복사해 넣지 마라 — 이 레포 전용 권한·훅 배선이라
다른 프로젝트를 덮어쓴다.

## 무엇을 담았나

L12 899~926행이 다루는 관리형 전용 키(permissions.deny/allow ·
disableBypassPermissionsMode · allowManagedPermissionRulesOnly · sandbox.* ·
allowManagedHooksOnly · disableSideloadFlags · strictKnownMarketplaces ·
allowManagedMcpServersOnly · requiredMinimumVersion)를 이 레포 값으로 채운
예시다. 각 키의 뜻은 원문(위 줄 번호)이 정본이다 — 여기서 되풀이하지 않는다.

## 🔴 함정 — `allowManagedHooksOnly` 가 프로젝트 훅을 죽인다

L12 920행: "allowManagedHooksOnly means only hooks defined in managed settings
run; hooks in user, project, and local settings are blocked." 이 레포의 승인
훅 5개(`protect-paths.sh` · `protect-tests.sh` · `no-secrets.sh` ·
`format-lint.sh` · `production-gate.sh`)는 프로젝트 설정(`.claude/settings.json`)에
있으므로, 켤 때는 이 예시의 `hooks` 블록에 같은 5개를 반드시 다시 등록한다.
`tests/test_managed_settings.sh` 가 이 불변식과 「여기 이름 댄 훅 파일이
`.claude/hooks/` 에 실재한다」를 잰다.
