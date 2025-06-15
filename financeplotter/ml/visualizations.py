"""
Machine learning visualization implementations for FinancePlotter
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, Union, List, Tuple
from sklearn.metrics import confusion_matrix, roc_curve, auc
from ..charts.base import Chart

def plot_predictions(
    data: pd.DataFrame,
    actual: str,
    predicted: str,
    title: str = None
) -> Chart:
    """
    Plot actual vs predicted values
    
    Args:
        data: DataFrame containing actual and predicted values
        actual: Column name for actual values
        predicted: Column name for predicted values
        title: Chart title
    
    Returns:
        Chart object
    """
    fig = go.Figure()
    
    # Plot actual values
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[actual],
            name='Actual',
            mode='lines',
            line=dict(width=2)
        )
    )
    
    # Plot predicted values
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[predicted],
            name='Predicted',
            mode='lines',
            line=dict(width=2, dash='dash')
        )
    )
    
    # Add error bands
    error = data[actual] - data[predicted]
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[predicted] + error.std(),
            fill=None,
            mode='lines',
            line_color='rgba(0,100,80,0.2)',
            name='Error Band'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[predicted] - error.std(),
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,100,80,0.2)',
            name='Error Band'
        )
    )
    
    fig.update_layout(
        title=title or 'Actual vs Predicted Values',
        xaxis_title='Time',
        yaxis_title='Value',
        showlegend=True
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart

def plot_decision_boundary(
    X: np.ndarray,
    y: np.ndarray,
    model,
    title: str = None,
    resolution: int = 100
) -> Chart:
    """
    Plot decision boundary for a classifier
    
    Args:
        X: Feature matrix
        y: Target vector
        model: Trained classifier
        title: Chart title
        resolution: Grid resolution for boundary
    
    Returns:
        Chart object
    """
    # Create mesh grid
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution)
    )
    
    # Predict on mesh grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Create figure
    fig = go.Figure()
    
    # Add decision boundary
    fig.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, resolution),
            y=np.linspace(y_min, y_max, resolution),
            z=Z,
            colorscale='RdBu',
            showscale=False
        )
    )
    
    # Add scatter points
    for label in np.unique(y):
        mask = y == label
        fig.add_trace(
            go.Scatter(
                x=X[mask, 0],
                y=X[mask, 1],
                mode='markers',
                name=f'Class {label}',
                marker=dict(size=8)
            )
        )
    
    fig.update_layout(
        title=title or 'Decision Boundary',
        xaxis_title='Feature 1',
        yaxis_title='Feature 2',
        showlegend=True
    )
    
    chart = Chart(pd.DataFrame(X), title)
    chart.fig = fig
    return chart

def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = None,
    labels: List[str] = None
) -> Chart:
    """
    Plot confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        title: Chart title
        labels: Class labels
    
    Returns:
        Chart object
    """
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Create figure
    fig = go.Figure()
    
    # Add heatmap
    fig.add_trace(
        go.Heatmap(
            z=cm,
            x=labels if labels else [f'Class {i}' for i in range(cm.shape[0])],
            y=labels if labels else [f'Class {i}' for i in range(cm.shape[0])],
            colorscale='Blues',
            showscale=True
        )
    )
    
    fig.update_layout(
        title=title or 'Confusion Matrix',
        xaxis_title='Predicted',
        yaxis_title='Actual'
    )
    
    chart = Chart(pd.DataFrame(cm), title)
    chart.fig = fig
    return chart

def plot_roc_curve(
    y_true: np.ndarray,
    y_score: np.ndarray,
    title: str = None
) -> Chart:
    """
    Plot ROC curve
    
    Args:
        y_true: True labels
        y_score: Predicted probabilities
        title: Chart title
    
    Returns:
        Chart object
    """
    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    # Create figure
    fig = go.Figure()
    
    # Add ROC curve
    fig.add_trace(
        go.Scatter(
            x=fpr,
            y=tpr,
            name=f'ROC (AUC = {roc_auc:.2f})',
            mode='lines',
            line=dict(width=2)
        )
    )
    
    # Add diagonal line
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            name='Random',
            mode='lines',
            line=dict(width=2, dash='dash')
        )
    )
    
    fig.update_layout(
        title=title or 'ROC Curve',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        showlegend=True
    )
    
    chart = Chart(pd.DataFrame({'fpr': fpr, 'tpr': tpr}), title)
    chart.fig = fig
    return chart 