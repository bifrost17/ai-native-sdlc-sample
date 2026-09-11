# Intent: 담당자의 업무 요청을 골라서 조회
Author: 합성 요청자 F01. Status: draft.

## Problem
작은 팀이 로컬 CLI의 혼합 목록에서 특정 담당자의 요청을 매번 눈으로 골라내고 있다.

## Proposed outcome
담당자 ID로 목록을 좁혀 보고 전체 목록을 직접 고르는 수고를 줄이고 싶다.

## Affected users and systems
요청을 확인하는 작은 팀, tracker.py와 requests.json. 현재 Python 3.9 이상 표준 라이브러리만
사용하며 외부 서비스·계정·네트워크는 없다.

## Constraints
기존 list/show/complete 명령과 JSON 필드를 유지한다. 조회는 파일을 변경하지 않는다.
업무 코드는 2~4파일 이내의 작은 변경이고 시험·문서는 별도다.

## Open questions
- Q1 완료된 요청과 파일 순서를 어떻게 다룰지 요청자에게 확인한다.
- Q2 미배정·없는 담당자·ID 일치 방식을 요청자에게 확인한다.
- Q3 원하는 명령 사용법을 요청자에게 확인한다.
