"""
투자 리스크 분석: 단일 거래 입력에 대해 위험 패턴을 조건식으로 판정한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal

# --- 임계값 (정책에 맞게 조정) ---
CHASE_CHANGE_RATE_MIN = 7.0  # 최근 N일 상승률이 이 값(%) 이상이면 고점 추격 후보
AMOUNT_RATIO_MIN = 2.0  # 평균 거래액 대비 배수
IMPULSE_TRADE_COUNT_MIN = 2  # 1시간 내 이 횟수 이상이면 충동 거래


TradeSide = Literal["buy", "sell", "매수", "매도"]


@dataclass
class TradeInput:
    """한 건의 거래 + 맥락 지표 (모두 채워서 전달)."""

    stock: str
    type: TradeSide
    amount: int
    change_rate: float  # 최근 N일 상승률 (%)
    at: datetime
    avg_amount: float  # 사용자 평균 거래 금액
    recent_trade_count_1h: int  # 해당 시점 기준 최근 1시간 내 거래 횟수(보통 본 건 포함)
    avg_trade_count_7d: float | None = None  # 참고용, 패턴 판정에는 미사용


@dataclass
class RiskAnalysis:
    patterns: list[str]
    reasons: list[str]
    warning_message: str


def _is_buy(t: TradeSide) -> bool:
    return str(t).lower() in ("buy", "매수")


def analyze_trade(inp: TradeInput) -> RiskAnalysis:
    patterns: list[str] = []
    reasons: list[str] = []

    # 1) 고점 추격 매수: 매수이면서 최근 상승률이 기준 이상
    if _is_buy(inp.type) and inp.change_rate >= CHASE_CHANGE_RATE_MIN:
        patterns.append("고점 추격 매수")
        reasons.append(
            f"최근 상승률이 {inp.change_rate}%로, 기준({CHASE_CHANGE_RATE_MIN}%) 이상인 상태에서 매수했습니다."
        )

    # 2) 과도한 금액: 평균 대비 배수 (매수·매도 공통으로 금액 리스크로 볼 수 있음; 요구는 '거래 금액')
    if inp.avg_amount > 0 and inp.amount >= inp.avg_amount * AMOUNT_RATIO_MIN:
        patterns.append("과도한 금액 투자")
        reasons.append(
            f"이번 거래 금액 {inp.amount:,}원이 평균 거래 금액 {inp.avg_amount:,.0f}원의 "
            f"{AMOUNT_RATIO_MIN}배({inp.avg_amount * AMOUNT_RATIO_MIN:,.0f}원) 이상입니다."
        )

    # 3) 충동 거래: 짧은 시간 내 반복
    if inp.recent_trade_count_1h >= IMPULSE_TRADE_COUNT_MIN:
        patterns.append("충동 거래")
        reasons.append(
            f"최근 1시간 안에 {inp.recent_trade_count_1h}번 거래했습니다(기준 {IMPULSE_TRADE_COUNT_MIN}회 이상)."
        )

    warning = _build_warning(patterns, inp)
    return RiskAnalysis(patterns=patterns, reasons=reasons, warning_message=warning)


def _build_warning(patterns: list[str], inp: TradeInput) -> str:
    if not patterns:
        return (
            f"이번 입력 기준으로는 정의된 위험 패턴(상승률 {CHASE_CHANGE_RATE_MIN}% 이상 매수, "
            f"평균의 {AMOUNT_RATIO_MIN}배 이상 금액, 1시간 {IMPULSE_TRADE_COUNT_MIN}회 이상 거래)에 해당하지 않습니다."
        )

    parts: list[str] = []
    if "고점 추격 매수" in patterns:
        parts.append(
            "이미 단기간에 크게 오른 구간에서 사는 쪽으로 들어가 있습니다. "
            "추가로 붙일수록 평균 단가만 위로 밀릴 수 있습니다."
        )
    if "과도한 금액 투자" in patterns:
        parts.append(
            "평소 쓰는 금액보다 큰 액수가 한 번에 나갔습니다. "
            "같은 방향으로 조금만 틀어져도 체감 손실이 커집니다."
        )
    if "충동 거래" in patterns:
        parts.append(
            "짧은 시간 안에 거래가 여러 번 이어졌습니다. "
            "한 박자 쉬었다가, 지금 포지션만 기준으로 다시 보시는 편이 낫습니다."
        )

    tail = f" ({inp.stock}, {inp.type}, {inp.amount:,}원)"
    return " ".join(parts).strip() + tail


def format_report(analysis: RiskAnalysis) -> str:
    p = ", ".join(analysis.patterns) if analysis.patterns else "없음"
    reasons_block = "\n".join(f"- {r}" for r in analysis.reasons) if analysis.reasons else "- (해당 없음)"
    return (
        "[분석 결과]\n"
        f"- 패턴: {p}\n\n"
        "[이유]\n"
        f"{reasons_block}\n\n"
        "[경고 메시지]\n"
        f"- {analysis.warning_message}\n"
    )
