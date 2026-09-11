# Claude Code fable result

Filtered CLI export; private reasoning omitted. Final result below is verbatim.

# R2 독립 리뷰 보고: 결합 spec 양식 후보

## 판정과 검토 범위

**판정: PASS.** R1과 같은 기준을 적용했다. 잘못된 plan이나 거짓 준비 완료 주장을 만들 만한 누락·모순은 없다. R1 이후의 수정이 복구 계약의 회귀 경로를 닫았고, 새 필수 절차나 검사기를 추가하지 않았다.

**검토 대상.** receipt는 `docs/research/sdlc-documentation/spec-design/reviews/candidate-r2.json`의 round 2이며 33개 파일이다. 아래 값은 receipt에 적힌 값이고 내가 재계산한 값이 아니다.

| 항목 | 값 |
|---|---|
| combined_sha256 | f4b37b76c06a28360bdf6bce56f2ebd3289b905b88d5135011ac6c43e337de02 |
| maker base_head | 4f5202824e9e800c293ccbc2b126037e9b08ac0a |
| adopter base_head | 3e2f693d5ca171d34aa3f464893b96dfd9429d2e |

**실제로 다시 읽은 파일.** 원래 review-request.md, r2-changes.md, candidate-r2.json, 그리고 changed_from_r1의 13개 파일 전부다. maker는 `/spec` 명령, CLAUDE.md, F01 spec, M01 context, M01 spec, design-depth, eval 03 양성·음성 fixture이고, adopter는 design-spec 예시 스킬, F01 spec, M01 context, M01 spec, design-depth다. F01의 새 문장을 확인하려고 데이터셋 baseline의 test_tracker.py도 읽었다. 변경되지 않은 20개 파일은 R1 관찰을 재사용했고, receipt의 제공 해시가 R1 값과 같음을 대조해 변경 목록이 정확히 13개와 일치함을 확인했다. Astra의 보고서는 읽지 않았고 r2-changes.md에 있는 root의 한 줄 요약만 보았다.

**미러 대조.** adopter의 F01 spec·M01 spec은 maker와 2행·4행만 달랐고, M01 context와 design-depth는 본문이 동일했다. 해시는 제공된 값이며 재계산하지 못했다.

## 변경 항목별 평가와 발견

- **M01 복구 계약 수정이 회귀를 닫는다.** context의 추가 결정이 R4·AC4·Design·Q2에 일관되게 반영됐다. R4는 쓰기 여부 불명확 시 쓰기 이후로 취급하고, R1을 유지하는 쓰기 경로가 검증되기 전에는 중지를 유지한다. Design은 데이터 검증만으로 결함 있는 구버전 writer를 재개하지 않으며 기본 복구 방향이 최신 데이터를 보존한 SQLite 경로임을 밝힌다. AC4는 재개할 쓰기 경로의 AC1 미충족을 실패 분기로 다루고, 구버전 호환 시험을 별도 사본에서 하며 원래 내보낸 복구 데이터를 바꾸지 않는다. 내보낸 JSON은 schema_version=1 형식이므로 R3의 이행 경로로 재투입할 수 있어 복구 방향과 이행 계약이 맞물린다. 백업 체계는 이제 사실로 단정하지 않고 입력에 없다고 적었다.
- **F01 AC3 수정은 사실과 맞다.** baseline의 test_tracker.py는 목록 순서·무기록, 조회 성공·실패, 완료 대상만 변경·반복의 세 시험만 있고 rc=2의 I/O 오류 경로는 없다. 새 문장은 기존 시험이 다루지 않는 범위를 plan의 판단으로 넘기므로 R1보다 정확하다. 제품 계약과 요구·설계는 그대로다.
- **eval 03 fixture는 약화되지 않았다.** AC 절만 Requirements 다음으로 옮겼고 케이스 JSON의 해시는 R1과 같다. 음성 fixture는 여전히 Q1 행이 없어 Q1 정규식 검사에 실패하며, 양성 fixture는 Q1 answered와 Q2 carried forward를 모두 담는다. 테스트와 채점기에서 fixture 구조나 절 이름을 고정하는 코드는 없었다.
- **CLAUDE.md와 `/spec` 명령은 연결 설명만 바뀌었다.** CLAUDE.md는 templates 설명 한 줄만 바뀌었고, 명령은 마지막 문장이 스킬의 승인 판 확인과 기록된 초안 예외를 가리키도록 바뀌었다. L3 프롬프트 본문·frontmatter·TEAM 표식은 R1 내용과 글자 그대로 같다. 두 파일을 고정하는 테스트는 없고, 북극성 주석 V3-08·V3-13의 축자 판정도 여전히 성립한다.
- **design-depth 이행 행은 프롬프트 보강에 그친다.** 전환 후 쓰기와 재개 시 불변 조건 보존을 한 문장으로 넣었고 표제·검사기·관문은 추가하지 않았다. maker와 adopter 본문이 같다.
- **adopter 지침의 두 문장은 선택형을 유지한다.** intent의 해결 제안과 실제 설계 선택의 구분, 요청·자료 판을 기존 기록에 남기는 문장이 추가됐다. `disable-model-invocation: true`와 References applied가 유지되고 설치 요구는 없다. 이는 R1 권고 10을 해소한다.

**차단하지 않는 권고.** 경로와 영향을 함께 적는다.

1. **전환 전 실패 분기의 범위 명시.** `.claude/skills/design-spec/examples/migration/spec.md:70`부터의 "구버전 writer 재개 금지"는 문맥상 전환 후 복구에 한정되지만, 이행 검증 실패 뒤 기존 JSON 서비스가 그대로 계속되는지는 61~64행이 암시만 한다. 보수적으로 잘못 읽으면 불필요한 중지가 길어질 뿐 데이터 손실은 없다. 한 문장으로 전환 전 실패는 현상 유지임을 적으면 된다.
2. **앞머리 요약의 결정 노출.** 같은 파일 6~8행은 옛 시스템으로 되돌아가지 않고 안전한 경로 확보 전까지 중지를 유지한다는 결정을 담지 않는다. 제품 오너가 요약만 읽으면 중지 감수라는 절충을 놓칠 수 있다. R4가 바로 아래에 있어 차단 사유는 아니다.
3. **AC1 확인의 실행 방식.** 같은 파일 70~71행의 "AC1로 확인"은 운영 데이터에서 실제 완료를 겹쳐 실행하는 것으로 읽힐 수 있다. 사본이나 시험 데이터에서 확인한다는 말을 plan에 남기면 충분하며 spec의 계약 자체는 온전하다.
4. **구버전 호환 시험의 목적.** 같은 파일 33~34행과 68행의 구버전 조회·완료 시험은 구버전 writer를 재개하지 않는 지금은 내보낸 파일의 형식·이식성 검증 역할만 남는다. 목적을 한 마디 적으면 옛 경로가 복구 수단이라는 오해를 막는다.
5. **읽기 전용 운영 선택지.** 같은 파일 73행은 안전한 쓰기 경로가 없을 때 중지만 허용한다. 쓰기를 닫은 읽기 전용 제공은 R1을 위반하지 않으므로 오너가 원하면 추가할 수 있는 선택지다. 합성 결정이 중지를 택했으므로 결함은 아니다.
6. **F01 예제 입력의 추적성.** `.claude/skills/design-spec/examples/feature/context.md:11`부터의 코드 읽기 맥락에는 기존 시험 범위가 없어, spec의 "세 시험" 사실을 예제 입력만으로는 확인할 수 없다. 실제 baseline과는 맞으므로 context에 한 줄 추가하면 된다.
7. **SQLite 백업 방식.** 거짓 단정은 사라졌지만 운영 담당이 정할 항목이라는 이월 표시도 없다. Q3에서 저장소 관리 책임이 확인됐으므로 선택 사항이다.
8. **후보 밖의 낡은 주석.** 북극성 주석 V3-07은 옛 스킬 문구를, V3-09는 옛 절 이름을 인용한다. 역사적 평가이며 receipt 밖이다.

**한계.** 해시를 재계산하지 못했고 테스트·eval을 실행하지 않았다. git diff를 볼 수 없어 CLAUDE.md와 `/spec` 명령의 이전 문구는 R1 세션의 읽기 내용으로 대조했다. adopter 워크트리의 git 상태는 확인하지 못했다. 작업 트리의 probe 디렉터리와 별도 실험 브랜치의 Sonnet 초안은 receipt 밖이라 읽지 않았다. 이 판정은 세 합성 예제와 양식·지침의 문서 설계 검토이며 사람의 승인이나 실제 이행·복구 실행의 증명이 아니다.
