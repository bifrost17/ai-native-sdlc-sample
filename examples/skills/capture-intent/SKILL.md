---
name: capture-intent
description: Explicitly selected workflow example for turning an originator's idea, ticket, or incident into an intent document using this project's artifact template.
disable-model-invocation: true
---
# 의도 기록 예시

팀이나 사용자가 이 예시를 선택했을 때 사용한다. 제안자의 언어로 문제, 사용자, 범위, 제약과 성공의
의미를 확인한다. 답이 얇은 곳은 구체적인 관측이나 사례를 묻고, 답할 수 없는 것은 결정자를 남긴다.

해결책부터 제안받았다면 그 해결책이 필요한 문제를 확인한다. 제안자가 특정 해결책을 제약으로
유지하겠다고 한 경우에는 그 결정을 제약으로 기록한다.

프로젝트의 `templates/intent.md`를 사용해 합의된 변경 폴더에 `intent.md`를 쓴다. 첫 변경인지,
번호가 이미 있는지는 `intent/`에서 확인한다. 제안자의 사실을 대신 만들지 않으며, 양식의 빈칸은
실제 내용이나 답을 기다리는 질문으로 바꾼다. 사고나 결함이면 입력, 기대와 실제 결과, 재현 방법,
관측 시각을 아는 범위에서 기록한다.

초안을 제안자에게 보여 사실과 기대를 확인한다. 제안자가 없는 비대화형 작업이면 누가 확인해야
하는지 인계한다. 승인과 다음 단계의 진행은 프로젝트의 `docs/PROCESS.md`를 따른다.
이 작업으로 요구·설계, 구현 계획, 코드를 만들거나 문서를 승인하지 않는다.
