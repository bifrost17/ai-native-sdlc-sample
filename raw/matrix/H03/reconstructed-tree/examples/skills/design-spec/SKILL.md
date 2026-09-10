---
name: design-spec
description: Explicitly selected workflow example for turning an accepted intent into requirements and design, carrying forward constraints, questions, and policy concerns.
disable-model-invocation: true
---
# 요구·설계 작성 예시

팀이나 사용자가 이 예시를 선택했을 때 사용한다. 대상 `intent.md`와 `PROJECT-POLICY.md`를 읽고,
프로젝트가 정한 통합 대상과 실제 승인 기록을 확인한다. `Status: draft.`만으로 미승인이라고 판단하지
않는다. 초안에서 진행하도록 허용한 지시가 있다면 그 범위와 이유를 기록한다.

`templates/spec.md`를 사용해 같은 변경 폴더에 `spec.md`를 쓴다. 요구는 사용자가 관측할 수 있는
결과로 적고 의도의 문제와 연결한다. 설계에는 선택의 이유, 기존 구성의 재사용, 필요한 데이터 흐름을
적는다. 의도의 제약을 빠뜨리지 않고 이어받으며, 미결 질문은 답변 또는 결정자를 둔 이월로 남긴다.

팀이 정한 관련 정책과 자료를 실제로 읽고 적용한다. 읽지 않은 자료를 적용했다고 쓰거나 확인할 수
없는 판을 지어내지 않는다. 팀이 스킬을 선택해 두었다면 필요한 작업에 활용할 수 있다.
정책 충돌, 빈 정책 값, 확인하지 못한 사실과 가정은 근거·영향·결정자를 붙여 우려로 기록한다.
양쪽 정책의 충돌을 임의로 승인하거나 조용히 해소하지 않는다.

검토자에게 의도와 spec을 함께 넘기고, 의도의 문제를 해결하는지와 미결 질문이 빠짐없이 이어졌는지
확인하게 한다. 이 작업으로 계획이나 코드를 작성하거나 spec을 승인하지 않는다.
