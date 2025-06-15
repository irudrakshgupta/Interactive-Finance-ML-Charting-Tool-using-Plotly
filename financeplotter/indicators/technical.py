"""
Technical indicator implementations for FinancePlotter
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, Tuple
from ..charts.base import Chart

def add_sma(chart: Chart, period: int = 20, column: str = 'Close') -> Chart:
    """
    Add Simple Moving Average to the chart
    
    Args:
        chart: Chart object
        period: SMA period
        column: Column to calculate SMA on
    
    Returns:
        Updated Chart object
    """
    if not chart.fig:
        return chart
        
    data = chart.data
    sma = data[column].rolling(window=period).mean()
    
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=sma,
            name=f'SMA {period}',
            line=dict(width=1)
        )
    )
    
    return chart

def add_ema(chart: Chart, period: int = 20, column: str = 'Close') -> Chart:
    """
    Add Exponential Moving Average to the chart
    
    Args:
        chart: Chart object
        period: EMA period
        column: Column to calculate EMA on
    
    Returns:
        Updated Chart object
    """
    if not chart.fig:
        return chart
        
    data = chart.data
    ema = data[column].ewm(span=period, adjust=False).mean()
    
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=ema,
            name=f'EMA {period}',
            line=dict(width=1)
        )
    )
    
    return chart

def add_rsi(chart: Chart, period: int = 14, column: str = 'Close') -> Chart:
    """
    Add Relative Strength Index to the chart
    
    Args:
        chart: Chart object
        period: RSI period
        column: Column to calculate RSI on
    
    Returns:
        Updated Chart object
    """
    if not chart.fig:
        return chart
        
    data = chart.data
    
    # Calculate price changes
    delta = data[column].diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Create new subplot for RSI
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=rsi,
            name='RSI',
            line=dict(width=1)
        ),
        row=2, col=1
    )
    
    # Add overbought/oversold lines
    chart.fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    chart.fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    return chart

def add_macd(
    chart: Chart,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    column: str = 'Close'
) -> Chart:
    """
    Add Moving Average Convergence Divergence to the chart
    
    Args:
        chart: Chart object
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line period
        column: Column to calculate MACD on
    
    Returns:
        Updated Chart object
    """
    if not chart.fig:
        return chart
        
    data = chart.data
    
    # Calculate MACD
    exp1 = data[column].ewm(span=fast_period, adjust=False).mean()
    exp2 = data[column].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    hist = macd - signal
    
    # Create new subplot for MACD
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=macd,
            name='MACD',
            line=dict(width=1)
        ),
        row=2, col=1
    )
    
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=signal,
            name='Signal',
            line=dict(width=1)
        ),
        row=2, col=1
    )
    
    chart.fig.add_trace(
        go.Bar(
            x=data.index,
            y=hist,
            name='Histogram'
        ),
        row=2, col=1
    )
    
    return chart

def add_bollinger_bands(
    chart: Chart,
    period: int = 20,
    std_dev: float = 2.0,
    column: str = 'Close'
) -> Chart:
    """
    Add Bollinger Bands to the chart
    
    Args:
        chart: Chart object
        period: Moving average period
        std_dev: Number of standard deviations
        column: Column to calculate bands on
    
    Returns:
        Updated Chart object
    """
    if not chart.fig:
        return chart
        
    data = chart.data
    
    # Calculate Bollinger Bands
    ma = data[column].rolling(window=period).mean()
    std = data[column].rolling(window=period).std()
    upper = ma + (std * std_dev)
    lower = ma - (std * std_dev)
    
    # Add bands to chart
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=upper,
            name='Upper Band',
            line=dict(width=1, dash='dash')
        )
    )
    
    chart.fig.add_trace(
        go.Scatter(
            x=data.index,
            y=lower,
            name='Lower Band',
            line=dict(width=1, dash='dash'),
            fill='tonexty'
        )
    )
    
    return chart 