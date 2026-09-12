#!/usr/bin/env bash
# skills/brand/SKILL.md 3단계가 부르는 기계적 훑기. policies/brand.md 의 B1·B2·B3·B4·B6·B7 중
# 「낱말·기호로 잡히는 것」만 잡는다. **잡히지 않았다고 통과가 아니다** — B5 와 문장의 뜻,
# 존댓말·한 문장 한 뜻은 사람과 스킬이 본다(권고적 통제).
# 정책이 든 낱말은 B1 「최고의·완벽한」, B2 「보장합니다·무조건·즉시」, B4 「처리중·완료」 뿐이다.
# 나머지 패턴은 같은 꼴이라 함께 잡는 것 — 조항이 아니라 적용이다(SKILL.md 의 각 조항 절 참고).
# 알려진 사각(고치지 않고 적어 둔다): 점 찍은 날짜 `26.9.10` 은 IP·버전 번호와 구분할 수 없어 보지 않는다.
#   인용문 안의 위반("고객이 이렇게 말했다: 무조건…")도 구분하지 못한다.
# 사용: bash check-brand-copy.sh <파일…>
# rc: 0 = 걸린 것 없음 · 1 = 걸림 · 2 = 사용법 오류 또는 **검사 자체가 실패**(초록으로 위장하지 않는다)
set -u
[ $# -ge 1 ] || { echo "사용: $0 <파일…>" >&2; exit 2; }
for f in "$@"; do
  [ -f "$f" ] || { echo "없는 파일: $f" >&2; exit 2; }
  [ -r "$f" ] || { echo "읽을 수 없는 파일: $f" >&2; exit 2; }
  # 이진 파일은 검사하지 않는다. 조용히 초록을 내는 것보다 거절하는 편이 낫다
  n_all=$(wc -c < "$f" | tr -d ' ')
  n_txt=$(LC_ALL=C tr -d '\000' < "$f" | wc -c | tr -d ' ')
  if [ "$n_all" != "$n_txt" ]; then
    echo "이진 파일이라 검사하지 않는다(초록이 아니다): $f" >&2; exit 2
  fi
done

hits=0
failed=0

# report <조항> <왜> <패턴> <예외패턴|""> <파일>
report() {
  clause="$1"; why="$2"; pat="$3"; except="$4"; file="$5"
  out=$(grep -a -nE -- "$pat" "$file" 2>&1); rc=$?
  if [ "$rc" -ge 2 ]; then
    echo "검사 실패($clause · $file): $out" >&2   # 빨간 것을 초록이라 하지 않는다
    failed=1; return 0
  fi
  [ "$rc" -eq 0 ] || return 0
  if [ -n "$except" ]; then
    out=$(printf '%s\n' "$out" | grep -a -vE -- "$except") || return 0
    [ -n "$out" ] || return 0
  fi
  printf '%s\n' "$out" | while IFS= read -r line; do echo "$file:$line  ← $clause $why"; done
  return 1
}

report_emoji() { # macOS grep 에 -P 가 없다 — UTF-8 바이트 앞머리로 본다
  file="$1"
  out=$(LC_ALL=C grep -a -n -e $'\xF0\x9F' -e $'\xE2\x98' -e $'\xE2\x99' -e $'\xE2\x9A' \
        -e $'\xE2\x9B' -e $'\xE2\x9C' -e $'\xE2\x9D' -e $'\xE2\x9E' -e $'\xE2\xAC' \
        -e $'\xE2\xAD' -e $'\xE3\x8A' -- "$file" 2>&1); rc=$?
  if [ "$rc" -ge 2 ]; then echo "검사 실패(B7 이모지 · $file): $out" >&2; failed=1; return 0; fi
  [ "$rc" -eq 0 ] || return 0
  printf '%s\n' "$out" | while IFS= read -r line; do echo "$file:$line  ← B7 이모지"; done
  return 1
}

for f in "$@"; do
  report "B1" "과장·감탄" '최고의|최상의|완벽한|완벽하게|엄청난|어마어마한' '' "$f" || hits=1
  # B2: 같은 줄에 근거 조항(제N조·법령)이 붙어 있으면 정책이 허용한다 → 예외
  report "B2" "확약 표현" \
    '보장합니다|보장해 ?드립니다|무조건|즉시|반드시|확실히|100% *(보장|지급|환급)' \
    '제 ?[0-9]+ ?조|시행령|약관에 따라' "$f" || hits=1
  report "B3" "사과 단독" '불편을 (드려|끼쳐) 죄송합니다' '' "$f" || hits=1
  # B4: 상태 어휘 밖. 청구 상태가 아닌 자리(영업 종료·마감일·본인인증 완료…)는 예외로 뺀다
  report "B4" "상태 어휘 밖" \
    '처리 ?중|검토 ?중|진행 ?중|확인 ?중|접수완료|처리완료|입금완료|정산완료|서류미비|반려|추가요청|청구중|(^|[^급])완료|종료|마감|상태[^가-힣]{0,4}(신청|등록|보류|취소|끝)' \
    '영업 ?종료|통화 ?종료|세션 ?종료|연결 ?종료|마감일|마감 ?시각|인증 ?완료|가입 ?완료|업로드 ?완료|제출 ?완료|설치 ?완료' \
    "$f" || hits=1
  # B6: 날짜 꼴 / 금액 꼴 / 시각 꼴. 점 찍은 날짜는 위 「알려진 사각」 참고
  report "B6" "날짜·금액·시각 꼴" \
    '[0-9]{4}년 ?[0-9]{1,2}월|[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}|[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}|오전 ?[0-9]{1,2}시|오후 ?[0-9]{1,2}시|[0-9]+ ?만원|[0-9]+ ?억원|₩|[0-9]+ ?KRW|[0-9]{4,}원' \
    '' "$f" || hits=1
  # B7 느낌표: 한글 뒤의 느낌표만 본다(코드의 `!=`·shebang·마크다운 이미지는 뺀다)
  report "B7" "느낌표" '[가-힣] ?!' '' "$f" || hits=1
  report_emoji "$f" || hits=1
done

if [ "$failed" -eq 1 ]; then
  echo "brand: 검사가 실패한 항목이 있다 — 위 stderr 를 보라. 통과로 읽지 마라." >&2
  exit 2
fi
if [ "$hits" -eq 0 ]; then
  echo "brand: 걸린 것 없음 (낱말·기호로 잡히는 것만 본 것이다 — B5·존댓말·문장의 뜻은 사람이 본다)"
  exit 0
fi
echo "brand: 위 줄들이 정책 조항에 걸렸다. 고치거나, 근거 조항을 붙이거나, spec 의 Flagged concerns 로 올려라." >&2
exit 1
