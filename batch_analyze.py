"""
과거 거래 배열로부터 각 시점의 avg_amount, 1시간 내 거래 횟수를 계산한 뒤
단일 거래 단위로 risk_analyzer.analyze_trade를 호출한다.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from risk_analyzer import TradeInput, analyze_trade, format_report


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def count_trades_in_window(
    times: list[datetime], current: datetime, window_seconds: int = 3600
) -> int:
    """current 시각을 포함해 [current - window, current] 구간의 거래 수."""
    start = current - timedelta(seconds=window_seconds)
    return sum(1 for t in times if start <= t <= current)


def main() -> None:
    path = Path(__file__).parent / "sample_trades.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    # 정렬: 시간순
    rows = sorted(raw, key=lambda x: parse_dt(x["date"]))
    amounts_before: list[int] = []
    all_times: list[datetime] = []

    print("=== 각 거래별 분석 (해당 시점 이전 이력으로 평균 거래액 산출) ===\n")

    for row in rows:
        at = parse_dt(row["date"])
        amount = int(row["amount"])
        change = float(row["price_change_5d"])
        t = row["type"]
        stock = row["stock"]

        # 평균 거래 금액: '이번 거래 직전까지' 완료된 거래들의 금액 평균 (첫 거래는 이전 없음 → 0이면 과도 패턴 비활성)
        if amounts_before:
            avg_amt = sum(amounts_before) / len(amounts_before)
        else:
            avg_amt = 0.0

        # 1시간 창: 이번 주문 시점까지의 타임스탬프만 반영 (이전 거래들 + 이번에 포함)
        times_for_window = all_times + [at]
        recent_1h = count_trades_in_window(times_for_window, at, 3600)

        inp = TradeInput(
            stock=stock,
            type=t,
            amount=amount,
            change_rate=change,
            at=at,
            avg_amount=avg_amt,
            recent_trade_count_1h=recent_1h,
        )
        analysis = analyze_trade(inp)
        print(f"--- {row['date']} | {stock} | {t} | {amount:,}원 ---")
        print(format_report(analysis))
        print()

        amounts_before.append(amount)
        all_times.append(at)


if __name__ == "__main__":
    main()
