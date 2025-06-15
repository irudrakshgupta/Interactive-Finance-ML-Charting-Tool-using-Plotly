"""
FinancePlotter - Interactive financial and machine learning visualizations
"""

__version__ = "0.1.0"

from .charts import (
    create_candlestick,
    create_line,
    create_bar,
    create_area,
    create_scatter
)
from .indicators import (
    add_sma,
    add_ema,
    add_rsi,
    add_macd,
    add_bollinger_bands
)
from .ml import (
    plot_predictions,
    plot_decision_boundary,
    plot_confusion_matrix,
    plot_roc_curve
)

__all__ = [
    # Chart creation functions
    'create_candlestick',
    'create_line',
    'create_bar',
    'create_area',
    'create_scatter',
    
    # Technical indicators
    'add_sma',
    'add_ema',
    'add_rsi',
    'add_macd',
    'add_bollinger_bands',
    
    # ML visualization functions
    'plot_predictions',
    'plot_decision_boundary',
    'plot_confusion_matrix',
    'plot_roc_curve'
] 