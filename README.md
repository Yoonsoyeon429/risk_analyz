# breaker — 투자 리스크 분석

거래 한 건에 대해 **고점 추격 매수**, **과도한 금액 투자**, **충동 거래** 패턴을 규칙 기반으로 판정합니다.

## 요구 사항

- Python 3.10+

## 사용법

### 단일 거래 분석

`risk_analyzer.py`의 `TradeInput`에 평균 거래액·최근 1시간 거래 횟수·상승률 등을 넣고 `analyze_trade()`를 호출합니다.

### 샘플 일괄 실행

```bash
python3 batch_analyze.py
```

`sample_trades.json`을 시간순으로 읽어, 각 시점 이전 이력으로 평균 금액을 계산한 뒤 분석합니다.

## 설정

`risk_analyzer.py` 상단 상수로 임계값을 조정할 수 있습니다.

- `CHASE_CHANGE_RATE_MIN` — 상승률 기준(%)
- `AMOUNT_RATIO_MIN` — 평균 대비 배수
- `IMPULSE_TRADE_COUNT_MIN` — 1시간 내 거래 횟수

## GitHub에 올리기

로컬에서 첫 커밋까지 한 뒤, GitHub에서 새 저장소를 만든 다음:

```bash
git remote add origin https://github.com/<사용자명>/<저장소명>.git
git branch -M main
git push -u origin main
```

SSH를 쓰는 경우 `origin` URL을 `git@github.com:<사용자명>/<저장소명>.git` 형식으로 바꿉니다.
