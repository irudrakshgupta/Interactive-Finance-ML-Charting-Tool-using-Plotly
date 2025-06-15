"""
Example usage of FinancePlotter
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from financeplotter import (
    create_candlestick,
    add_sma,
    add_rsi,
    add_macd,
    plot_predictions,
    plot_confusion_matrix,
    plot_roc_curve
)

def main():
    # Download sample data
    data = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
    
    # Create candlestick chart with indicators
    chart = create_candlestick(
        data,
        title='Apple Inc. (AAPL) Stock Price',
        volume=True
    )
    
    # Add technical indicators
    chart = add_sma(chart, period=20)
    chart = add_rsi(chart)
    chart = add_macd(chart)
    
    # Add interactive features
    chart.add_range_slider()
    chart.add_zoom_pan()
    chart.add_tooltips()
    
    # Show the chart
    chart.show()
    
    # Save as HTML
    chart.write_html('apple_stock_analysis.html')
    
    # Example of ML visualization
    # Create some sample data for classification
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Train a simple classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Get predictions
    y_pred = model.predict(X)
    y_score = model.predict_proba(X)[:, 1]
    
    # Plot confusion matrix
    cm_chart = plot_confusion_matrix(y, y_pred, title='Sample Classification Results')
    cm_chart.show()
    
    # Plot ROC curve
    roc_chart = plot_roc_curve(y, y_score, title='Sample ROC Curve')
    roc_chart.show()

if __name__ == '__main__':
    main() 