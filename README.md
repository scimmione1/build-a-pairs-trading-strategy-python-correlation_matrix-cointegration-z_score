# Forex Pairs Trading Strategy: Correlation Matrix, Cointegration & Z-Score Analysis

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A comprehensive implementation of statistical pairs trading strategy for forex markets using cointegration analysis, correlation matrices, and z-score normalization for signal generation.

## 📊 Project Overview

This project implements a quantitative pairs trading strategy that identifies statistically cointegrated forex pairs and generates trading signals based on mean-reversion principles. The analysis focuses on finding currency pairs that move together over time and trading their temporary divergences.

### Key Features

- **Cointegration Testing**: Statistical identification of long-term relationships between forex pairs
- **Correlation Analysis**: Heat map visualization of cross-correlations between currencies
- **Z-Score Normalization**: Signal generation based on standardized spread deviations
- **Backtesting Framework**: Complete performance analysis with risk metrics
- **Multi-Index Data Handling**: Efficient processing of multi-dimensional financial data

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas numpy yfinance statsmodels seaborn matplotlib scipy
```

### Required Libraries

```python
import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from statsmodels.regression.rolling import RollingOLS
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/forex-pairs-trading-strategy.git
cd forex-pairs-trading-strategy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Open the Jupyter notebook:
```bash
jupyter notebook build-a-pairs-trading-strategy-python-correlation_matrix-cointegration-z_score.ipynb
```

## 📈 Methodology

### 1. Data Collection & Processing
- **Source**: Yahoo Finance API via yfinance
- **Timeframe**: 2020-01-01 to 2025-08-01 (daily data)
- **Currency Pairs**: EURUSD, EURAUD, AUDUSD, NZDJPY, AUDJPY, CHFJPY, USDCHF, CADJPY

### 2. Cointegration Analysis
The project uses the Engle-Granger cointegration test to identify pairs with statistically significant long-term relationships:

```python
def find_cointegrated_pairs(data):
    # Implementation of cointegration testing
    # Returns: score_matrix, pvalue_matrix, pairs
```

### 3. Statistical Modeling

#### Regression Analysis
For each cointegrated pair, we perform OLS regression to determine the hedge ratio:

```
Y = α + β*X + ε
```

Where:
- **Y**: Dependent currency (e.g., NZDJPY)
- **X**: Independent currency (e.g., CADJPY)  
- **β**: Hedge ratio (optimal position sizing)
- **ε**: Error term (spread)

#### Z-Score Calculation
The spread is normalized using z-score for signal generation:

```
Z-Score = (Spread - μ) / σ
```

### 4. Trading Signals
- **Long Signal**: Z-score ≤ -1 (spread undervalued)
- **Short Signal**: Z-score ≥ +1 (spread overvalued)
- **Strong Signals**: Z-score ≥ ±2 for extreme conditions

## 📊 Results Summary

### Best Performing Pair: CADJPY/NZDJPY

| Metric | Value |
|--------|-------|
| **Hedge Ratio (β)** | 0.6433 |
| **R-squared** | 0.9375 (93.75%) |
| **Cointegration p-value** | 0.040 |
| **F-statistic** | 21,800 |
| **Spread Std Dev** | 1.9498 |

#### Key Insights:
- **Exceptional Explanatory Power**: 93.75% of NZDJPY variance explained by CADJPY
- **Strong Statistical Significance**: F-statistic of 21,800 with p-value ≈ 0.00
- **Stable Relationship**: Tight spread distribution supports mean-reversion trading
- **Optimal Hedge Ratio**: 0.64 provides precise position sizing

### Trading Performance
- **Signal Generation**: Z-score based entry/exit signals
- **Risk Management**: Standard deviation bands for position sizing
- **Backtesting**: Complete performance analysis with Sharpe ratio and drawdown metrics

## 📁 Project Structure

```
forex-pairs-trading-strategy/
│
├── README.md                                    # Project documentation
├── requirements.txt                             # Python dependencies
├── data/                                       # Data directory
│   └── forex_data.csv                         # Historical forex data
├── notebooks/
│   └── build-a-pairs-trading-strategy-python-correlation_matrix-cointegration-z_score.ipynb
└── results/                                   # Analysis outputs
    ├── correlation_heatmap.png
    ├── spread_analysis.png
    └── strategy_performance.png
```

## 🔧 Usage Example

```python
# Load and process data
data = load_forex_data()
data = clean_and_structure_data(data)

# Find cointegrated pairs
scores, pvalues, pairs = find_cointegrated_pairs(data)

# Analyze best pair
S1, S2 = data['CADJPY'], data['NZDJPY']
hedge_ratio, spread = calculate_spread(S1, S2)

# Generate trading signals
z_score = calculate_zscore(spread)
signals = generate_signals(z_score, threshold=1.0)

# Backtest strategy
performance = backtest_strategy(signals, spread)
```

## 📊 Visualizations

The notebook includes comprehensive visualizations:

1. **Correlation Heat Map**: Cross-correlation matrix of all currency pairs
2. **Spread Analysis**: Time series of price spreads with statistical bands
3. **Z-Score Evolution**: Normalized spread with trading signal thresholds
4. **Strategy Performance**: Cumulative returns and drawdown analysis
5. **Signal Distribution**: Trading entry/exit points visualization

## 🧪 Statistical Tests

- **Cointegration Test**: Engle-Granger test (p-value < 0.05)
- **Normality Tests**: Jarque-Bera and Omnibus tests
- **Autocorrelation**: Durbin-Watson statistic
- **Model Significance**: F-statistic and t-statistics

## ⚡ Performance Metrics

The strategy evaluation includes:

- **Total Return**: Cumulative strategy performance
- **Sharpe Ratio**: Risk-adjusted returns (annualized)
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Signal Frequency**: Trading signal generation rate
- **Win Rate**: Percentage of profitable trades

## 🔮 Future Enhancements

- [ ] Implementation of transaction costs and slippage
- [ ] Rolling window cointegration testing
- [ ] Machine learning enhanced signal generation
- [ ] Multi-timeframe analysis
- [ ] Portfolio optimization across multiple pairs
- [ ] Real-time trading system integration

## 📝 Research Papers & References

1. Engle, R. F., & Granger, C. W. (1987). Co-integration and error correction
2. Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. (2006). Pairs trading: Performance of a relative-value arbitrage rule
3. Avellaneda, M., & Lee, J. H. (2010). Statistical arbitrage in the US equities market

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is for educational and research purposes only. The strategies and analysis presented should not be considered as financial advice. Trading forex involves substantial risk and may not be suitable for all investors. Past performance does not guarantee future results.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourlinkedin)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Yahoo Finance for providing accessible financial data
- Statsmodels community for robust statistical tools
- Quantitative finance community for research and methodologies

---

⭐ **If you found this project helpful, please give it a star!** ⭐
