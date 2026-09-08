"""claims_status — 사슬 0002 의 예제 구현(표준 라이브러리만).

모듈 셋으로 자른다. 자르는 기준은 「무엇이 하나여야 하는가」이고, 그것이 곧
결정론 백스톱(scripts/check_endpoints.sh)이 재는 축이다:

    records.py    상류 claims-core 접근 + TTL 캐시   — 상류 레코드는 여기서만 나온다
    response.py   RESPONSE_FIELDS + build_response() — 응답은 여기서만 조립된다
    routes.py     라우트 등록 + 핸들러               — 등록은 여기서만 일어난다

이 파일에는 로직을 두지 않는다. 패키지를 임포트하는 것만으로 라우트가 등록되거나
캐시가 채워지는 부작용이 생기면, 무엇이 언제 일어났는지 아무도 못 센다.
"""
