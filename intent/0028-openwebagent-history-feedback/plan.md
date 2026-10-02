# Plan — openWebAgent 이력에서 개선과 재실험으로

Status: draft
Upstream: [spec](spec.md), [intent](intent.md), 사용자의 실행 요청.

현재 상태: T01의 340 PR·114 브랜치·30 번호 개발건과 4 무번호 개발건 수집 완료. T02 전수 보고서 작성 중.
초기 main은 a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e.
기존 제작 HEAD ad98ade와 미커밋 patch는 start/에 보존한다. 새 보고서를 제품 완료로 주장하지 않는다.

## Files that change
제작 연구 폴더의 방법·개발건별 보고서·발견·검토·실험 요약과 이 chain을 작성한다.
승격된 개선은 tdd-optional의 기존 정책·양식·스킬·전달 안내에 가장 작은 변경으로 반영한다.
북극성과 연구 색인은 실제 확인한 근거만 연결한다. 원제품과 전역 설치는 범위 밖이다.

## Order of work
- T01 / SP01 (Luna medium + root): 원격 API 전수 페이지와 bare Git를 수집한다. main/ref SHA와 원본 hash를 고정한다. intent 이력, PR의 head/title/body/diff에서 개발건을 정규화한다. 당시 지침·현재 HEAD·후보를 서로 구분한다. Done: AC01의 조사 모집단과 담당 목록.
- T02 / SP02 (Sol medium, 큰 계약 Astra high): 0018/0021/0028을 먼저 읽어 사건 기준을 맞춘다. 모든 개발건을 4~5개 묶음으로 병렬 분석한다. 승인·최초 문서·관련 구현·리뷰·후속 갱신의 실제 Git 판을 대조한다. 중요한 원인이 불명확할 때만 필요한 대화 구간을 수집한다. Done: AC02의 전체 건별 보고서와 coverage.
- T03 / SP02 (root + Astra high): 공통 원인을 중복 제거하고 반증·성공 대조·현행 지침을 읽는다. 후보가 두 독립 사건 또는 중대한 현재 재현에 근거하는지 확인한다. 개선할 실제 지침과 바뀔 판단을 이 spec/plan에 추가한다. Done: AC03의 최대 2~3개 작은 변경 또는 근거 있는 보류.
- T03a / SP04 (Astra high, T02와 병렬): 사용자 추가 네 가설을 원전 연구와 대조한다. 실제 UI/공유 시퀀스의 조기 검증과 설계 검증의 구체화를 현행 지침에 대조하고 역사 증거와 결합한다. 일반 방법의 효과를 해당 실사용 실패의 원인 증명으로 대신하지 않는다.
- T03b / SP05 (root 설계, Sol medium 구현, Astra high 검토): 사용자 추가 PR·커밋·총괄/정본 요구를 배포판의 기존 정책과 대조한다. changes 경로와 총괄 README, .github PR 양식과 commit 작성 문서를 제공한다. 기존 intent 경로·maker 이력은 자동 이동하지 않으며 source 작성 스킬/도구 전달의 참조를 맞춘다.
- T03c / SP06 (root 구현, Astra high 설계 검토): templates/spec.md의 AC 안내에 검증 경계·입력/환경·독립 기대·관측/한계를 연결한다. design-spec/references/design-depth.md의 기존 설계 블록에 실제 UI/앱 셸과 검증 예시를, plan/references/execution-depth.md에 첫 실제 수직 경로와 늦는 경우의 대안을 보강한다. disposable-ui-exploration 예시는 정적 배치 탐색과 실제 컴포넌트 결합 탐색의 선택을 설명한다. 공통 feedback은 최종 PR본문·현재판·개발건색인/과거spec대조를 짧게 연결한다. source package를 0.1.9로 맞추고 Codex patch/Claude strict검증, 작은 사례 부담 검토를 거친다. Done: AC03/06의 실제 diff·검토 기록 및 T04의 현재판/수정판 경계 비교.
- T04 / SP03 (root HUMAN + 실제 CLI): 원래 도구의 두 사례 전후 네 실행, 다른 도구의 별도 한 실행을 수행한다. 각 제품은 독립 repo와 고정 template ref/파생 branch를 갖는다. 설치 자산·실제 model/effort·질문/답변·실행·commit을 보존한다. 새 문맥 인계와 후속 변경을 관측한다. Done: AC04; 부족하면 최대 두 차례 수정과 전체 9실행 안에서 재검증.
- T05 / 전체 (root + fresh verifier): 현재 diff와 coverage·실험·회귀 결과를 독립 검토한다. make check와 필요한 패키지/adapter 확인을 수행한다. 확인 범위만 주석·최종 보고·인계에 반영하고 관련 파일만 커밋한다. Done: AC05 및 실제 결과/잔여 한계.

## Risks
PR title·최종 문서·version 문자열만으로 실제 사건과 설치를 판단하지 않는다.
사람의 복구는 초기 자발적 수행 성공과 구별한다. 원격 body는 수집 시점의 mutable 자료다.
큰 개발건의 반복 수정이 전체 실패율을 부풀리지 않도록 같은 사건을 dedupe한다.
기록 결손으로 템플릿 결함을 추정하거나, 단일 프로젝트의 검사 정책을 일반 템플릿에 편입하지 않는다.

## Proof
원본/API/Git manifest, 전체 개발건 coverage와 보고서, 원문·발췌 대조, 후보 검토,
실제 CLI 설치·전후 실행·독립 동작 확인·회귀·새 문맥 리뷰, maker make check와 필요한 배포 검사.
전문은 .local/의 실행 자료에 보존하고 연구 문서에서 경로·hash·SHA·결론을 연결한다.
