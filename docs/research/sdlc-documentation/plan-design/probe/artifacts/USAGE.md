# 요청 CLI

Python 3.9 이상 표준 라이브러리만 사용한다. 모든 데이터는 합성이다.
`python3 tracker.py --data requests.json list`, `show R-101`, `complete R-101`을 사용한다.
`list --owner ID`는 owner 문자열이 정확히 같은 요청만 원래 순서로 출력한다(done 포함, 대소문자 구분).
`summary [--owner ID]`는 같은 정확 일치 규칙으로 선택한 요청의 open/done 건수를
`open\t{n}\ndone\t{n}\n` 형식으로 출력한다(파일 쓰기 없음).
complete 시험에는 데이터를 별도로 복사한다. 검증은 `python3 -m unittest discover -s tests -v`다.
