"""
Machine learning visualization functions for FinancePlotter
"""

from .visualizations import (
    plot_predictions,
    plot_decision_boundary,
    plot_confusion_matrix,
    plot_roc_curve
)

__all__ = [
    'plot_predictions',
    'plot_decision_boundary',
    'plot_confusion_matrix',
    'plot_roc_curve'
] 