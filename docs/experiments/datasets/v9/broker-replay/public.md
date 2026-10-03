# 사내 요청 브로커의 알림 재접속

owner와 observer가 연결이 끊긴 뒤 놓친 요청 알림을 다시 읽을 수 있게 하려 한다. 현재 제품은
`app/README.md`, HTTP API와 기존 시험으로 설명돼 있다. 과거 ACK 기록은 현재 계약이 아니다.

`GET /requests/{id}/notifications?subscriber=owner|observer&after=N`에서 durable events를 반환한다.
`seq`는 요청 안에서 유일하고 증가하는 정수이고, `kind`는 created/claimed/acknowledged/final이다.
after=0은 전체, 이후 cursor는 그보다 큰 seq만 반환한다. 같은 조회는 같은 결과이며 재접속/서버
재시작에서도 순서와 내용이 유지돼야 한다. 반복 claim/ACK는 같은 사실을 중복 기록하지 않는다.
ACK는 수신 확인이며 작업은 running이다. final만 끝낸다. observer는 claim/final 권한이 없다.
기존 요청 상태·API·SQLite 데이터와 호환돼야 한다. 잘못된 subscriber나 음수/비정수 cursor는 400,
없는 request는 404다. 그 밖의 중요한 가시성/오류 결정을 질문하거나 spec에서 드러내라.

실제 HTTP와 DB를 통과하는 좁은 검증을 먼저 잡고 구현 순서·실제 파일·기존 계약과 회귀를 연결한다.
제품 지침과 채택한 작성/feedback 스킬, 선택 hook 안내를 읽는다. 먼저 intent·spec·plan을 작성해
설명하고 구현은 다음 대화에서 요청한다. 대형 플랫폼/인증 서버/새 상태 장부는 도입하지 않는다.
