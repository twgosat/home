import numpy as np
import pandas as pd
import pytest

from cuanlens import indicators as ind


def test_sma_matches_manual():
    s = pd.Series([1.0, 2, 3, 4, 5])
    out = ind.sma(s, 3)
    assert out.isna().sum() == 2
    assert out.iloc[-1] == pytest.approx(4.0)


def test_rsi_all_gains_is_100_and_flat_is_50():
    up = pd.Series(np.arange(1.0, 60.0))
    assert ind.rsi(up).iloc[-1] == pytest.approx(100.0)
    flat = pd.Series([10.0] * 60)
    assert ind.rsi(flat).iloc[-1] == pytest.approx(50.0)


def test_rsi_all_losses_is_0():
    down = pd.Series(np.arange(100.0, 40.0, -1))
    assert ind.rsi(down).iloc[-1] == pytest.approx(0.0)


def test_rsi_matches_hand_computed_wilder_seed():
    # 14 changes: 8 of +1 and 6 of -1 -> avg_gain 8/14, avg_loss 6/14 -> RS 4/3 -> RSI 57.142857
    deltas = [1] * 8 + [-1] * 6
    close = pd.Series(np.concatenate([[100.0], 100.0 + np.cumsum(deltas)]))
    r = ind.rsi(close, 14)
    assert r.iloc[:14].isna().all()
    assert r.iloc[14] == pytest.approx(100 - 100 / (1 + 8 / 6))


def test_rsi_second_step_uses_wilder_recursion():
    deltas = [1] * 8 + [-1] * 6 + [2]
    close = pd.Series(np.concatenate([[100.0], 100.0 + np.cumsum(deltas)]))
    avg_gain = (8 / 14 * 13 + 2) / 14
    avg_loss = (6 / 14 * 13 + 0) / 14
    expected = 100 - 100 / (1 + avg_gain / avg_loss)
    assert ind.rsi(close, 14).iloc[15] == pytest.approx(expected)


def test_macd_hist_is_line_minus_signal():
    close = pd.Series(np.linspace(100, 150, 120) + np.sin(np.arange(120)))
    m = ind.macd(close)
    both = m.dropna()
    assert not both.empty
    assert (both["hist"] - (both["macd"] - both["signal"])).abs().max() < 1e-9


def test_bollinger_pct_b_bounds_on_constant_series_is_nan():
    bb = ind.bollinger(pd.Series([5.0] * 40))
    assert bb["pct_b"].isna().all()  # zero width must not divide by zero


def test_atr_positive_and_scales_with_range():
    idx = pd.RangeIndex(60)
    close = pd.Series(100.0, index=idx)
    narrow = ind.atr(close + 1, close - 1, close).iloc[-1]
    wide = ind.atr(close + 3, close - 3, close).iloc[-1]
    assert narrow == pytest.approx(2.0) and wide == pytest.approx(6.0)


def test_volume_ratio_excludes_today_from_baseline():
    vol = pd.Series([100.0] * 25 + [300.0])
    assert ind.volume_ratio(vol).iloc[-1] == pytest.approx(3.0)


def test_max_drawdown():
    assert ind.max_drawdown(pd.Series([100.0, 120, 60, 90])) == pytest.approx(-0.5)
    assert np.isnan(ind.max_drawdown(pd.Series(dtype=float)))


def test_volatility_zero_for_constant_growth():
    close = pd.Series(100 * 1.01 ** np.arange(50))
    assert ind.annualized_volatility(close) == pytest.approx(0.0, abs=1e-9)


def test_atr_wilder_recursion():
    idx = pd.RangeIndex(20)
    close = pd.Series(100.0, index=idx)
    high, low = close + 1, close - 1  # TR = 2 everywhere
    high.iloc[-1], low.iloc[-1] = 104.0, 96.0  # last TR = 8
    expected = (2 * 13 + 8) / 14
    assert ind.atr(high, low, close, 14).iloc[-1] == pytest.approx(expected)
