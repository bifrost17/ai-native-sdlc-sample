# 0032 — Text2SQL 콘솔의 검사 실패 이유 표시

판정: **집중 시험·개발 브라우저까지 검토한 병합 사례.** [PR #474](https://github.com/bifrost17/openwebagent/pull/474)는 `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`로 머지되어 고정 main에 포함된다. 0030의 API `detail.check`가 콘솔에서 일반 실패 문구로만 보이던 간극을 다룬다.

| 사건 | 근거·범위 |
|---|---|
| 최초 문서·코드 | [`9253408`](https://github.com/bifrost17/openwebagent/commit/9253408d97450d639c147f518c3ad6ee75f9fab1) `intent/0032-text2sql-console-check-failed-reasons/spec.md:9-25`는 `verdict`가 null/없고 errors가 있을 때 “검사에서 막혔습니다”와 짧은 사유를 표시하고, 정책 verdict가 있는 “정책에 걸렸습니다”는 유지하도록 구분한다. [`1a04045`](https://github.com/bifrost17/openwebagent/commit/1a040456a8e17296a6191d79865b4c9f20a44ac2)는 `logic.ts` 분류와 `Text2SqlPanel.svelte` 상태·표시를 연결했다. 최초 AC08은 실제 개발 브라우저를 요구한다. |
| 시험·리뷰 수정 | [`ce0637d`](https://github.com/bifrost17/openwebagent/commit/ce0637d03590db1d6f513813d482d41b317bea50) `logic.ts:188-211`, `Text2SqlPanel.svelte:231-264,295-296,562-596`은 실패 구분, stale state 해제, rejected SQL 복사 유지, 이유와 advisory를 그린다. 리뷰 뒤 advisory 한도를 200→600 코드포인트로 늘리고 이모지 절단·빈 값·접근성 이름/라벨 시험을 보강했다. `plan.md:27-39,60-69`은 초기 15개 중 13 RED·2 보존 통과, 집중 403→418→422 통과를 적는다. |
| 실제 표시 확인·통합 | `plan.md:60-69`는 frontend build 후 개발 :3080 컨테이너에 임시 복사해 라이트 화면을 관찰하고 `research/captures/ac-08-check-failed-reasons-light.png`를 남긴다. 병합 후 main에는 해당 코드가 있다. 전체 프런트엔드/CI 통과 기록은 없고 `svelte-check`의 기존 7739 오류 중 이 변경 파일 0건이라는 제한된 확인이다. 임시 복사 관찰을 배포 증거로 확대하지 않는다. |

여섯 축: **의도 보존**은 검사 실패와 정책 차단을 구별하고 구체 사유를 사용자에게 돌려준다. **설계 충실성**은 분류·상태·표시가 최종 spec과 맞으며 리뷰로 길이와 접근성이 보완됐다. **계획 실행 가능성**은 AC08과 집중 시험을 실행했지만 전체 앱 게이트는 남는다. **PR/병렬 분할**은 0030의 응답 계약을 UI가 이어받는 후속 PR로 통합됐다. **변경 피드백**은 리뷰의 코드포인트·라벨 지적이 최종 코드와 시험으로 이어졌다. **검증/보고**는 RED 순서, 집중 422, build/개발 브라우저 관찰을 구별하고 운영 사용까지 단정하지 않는다.

**요약 정확성:** #474 본문은 집중 시험과 브라우저 관찰의 범위를 대체로 명시한다. `plan.md`의 “merge pending” 헤더는 머지 뒤 현황 설명으로 재사용하면 낡는다. 기존 형식 오류가 많은 상태에서 `svelte-check`의 touched zero를 전체 정적 검사 통과라고 요약해서는 안 된다. 리뷰 수정 뒤 별도 독립 검증자는 확인되지 않는다.

가설: H1 **부분 지지**(기본 설계는 구분했지만 길이·접근성 세부는 리뷰 보완). H2 **지지**(0030의 유효 API 사유와 실제 콘솔 표시가 불일치했고 이 변경으로 연결). H3 **지지**(API `detail.check`→분류→상태→패널의 전체 흐름이 후속에서 완성). H4 **부분 지지**(초기 AC08·RED 존재, 접근성/문자 경계는 리뷰 뒤). 당시 지침과 현행 0.1.8/WIP의 브라우저·검증판 요구는 별도로 보며, 이 사례의 집중 검증 부족을 지침 부재로 바로 치환하지 않는다. 모델·OS는 브랜치명에서 추정하지 않는다.
