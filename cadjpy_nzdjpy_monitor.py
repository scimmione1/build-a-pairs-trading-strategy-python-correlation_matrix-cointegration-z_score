#!/usr/bin/env python3
"""
CADJPY/NZDJPY Pairs Trading Monitor
==================================

Real-time monitoring script for the CADJPY/NZDJPY forex pair.
Downloads latest data from Yahoo Finance, calculates z-score, and provides trading signals.

Author: Your Name
Date: August 2025
"""

import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import warnings
from datetime import datetime, timedelta
import time

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class ForexPairsMonitor:
    def __init__(self, lookback_days=1460):  # ~4 years of data
        """
        Initialize the monitor with default parameters
        
        Args:
            lookback_days (int): Number of days of historical data to use for calculations
        """
        self.lookback_days = lookback_days
        self.pair1 = 'CADJPY=X'
        self.pair2 = 'NZDJPY=X'
        self.alert_threshold = 0.8  # Alert when z-score approaches ±1
        
        # Store calculated parameters
        self.hedge_ratio = None
        self.spread_mean = None
        self.spread_std = None
        self.last_zscore = None
        
        print(f"🔍 Forex Pairs Monitor Initialized")
        print(f"📊 Monitoring: {self.pair1} / {self.pair2}")
        print(f"📅 Using {lookback_days} days of historical data")
        print(f"⚠️  Alert threshold: ±{self.alert_threshold}")
        print("-" * 50)

    def download_data(self):
        """Download fresh data from Yahoo Finance"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days)
            
            print(f"📥 Downloading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Download data for both pairs
            data = yf.download([self.pair1, self.pair2], 
                              start=start_date.strftime('%Y-%m-%d'), 
                              end=end_date.strftime('%Y-%m-%d'),
                              progress=False)
            
            # Extract Close prices
            if len(data.columns.levels) > 1:  # Multi-index columns
                cadjpy = data['Close'][self.pair1].dropna()
                nzdjpy = data['Close'][self.pair2].dropna()
            else:  # Single pair downloaded
                cadjpy = data['Close'].dropna()
                nzdjpy = data['Close'].dropna()
            
            # Align the data (same dates)
            aligned_data = pd.DataFrame({
                'CADJPY': cadjpy,
                'NZDJPY': nzdjpy
            }).dropna()
            
            if len(aligned_data) < 100:
                raise ValueError("Insufficient data points for analysis")
            
            print(f"✅ Downloaded {len(aligned_data)} data points")
            return aligned_data
            
        except Exception as e:
            print(f"❌ Error downloading data: {e}")
            return None

    def calculate_cointegration(self, data):
        """Test for cointegration between the pairs"""
        try:
            cadjpy = data['CADJPY']
            nzdjpy = data['NZDJPY']
            
            # Perform cointegration test
            coint_score, p_value, critical_values = coint(cadjpy, nzdjpy)
            
            print(f"📈 Cointegration Test Results:")
            print(f"   Score: {coint_score:.4f}")
            print(f"   P-value: {p_value:.4f}")
            print(f"   Critical Values: {critical_values}")
            
            if p_value < 0.05:
                print(f"✅ Pairs are cointegrated (p-value < 0.05)")
                return True, coint_score, p_value
            else:
                print(f"⚠️  Pairs may not be cointegrated (p-value >= 0.05)")
                return False, coint_score, p_value
                
        except Exception as e:
            print(f"❌ Error in cointegration test: {e}")
            return False, None, None

    def calculate_regression_and_spread(self, data):
        """Calculate regression parameters and spread"""
        try:
            cadjpy = data['CADJPY']
            nzdjpy = data['NZDJPY']
            
            # Perform OLS regression: NZDJPY = α + β * CADJPY + ε
            cadjpy_with_const = sm.add_constant(cadjpy)
            model = sm.OLS(nzdjpy, cadjpy_with_const).fit()
            
            # Extract parameters
            self.hedge_ratio = model.params['CADJPY']
            intercept = model.params['const']
            r_squared = model.rsquared
            
            # Calculate spread
            spread = nzdjpy - self.hedge_ratio * cadjpy
            self.spread_mean = spread.mean()
            self.spread_std = spread.std()
            
            print(f"📊 Regression Results:")
            print(f"   Hedge Ratio (β): {self.hedge_ratio:.4f}")
            print(f"   Intercept (α): {intercept:.4f}")
            print(f"   R-squared: {r_squared:.4f}")
            print(f"   Spread Mean: {self.spread_mean:.4f}")
            print(f"   Spread Std: {self.spread_std:.4f}")
            
            return spread
            
        except Exception as e:
            print(f"❌ Error in regression calculation: {e}")
            return None

    def calculate_zscore(self, spread):
        """Calculate current z-score"""
        try:
            current_spread = spread.iloc[-1]  # Most recent spread value
            zscore = (current_spread - self.spread_mean) / self.spread_std
            self.last_zscore = zscore
            
            return zscore
            
        except Exception as e:
            print(f"❌ Error calculating z-score: {e}")
            return None

    def check_trading_signals(self, zscore):
        """Check for trading signals and generate alerts"""
        
        print(f"\n🎯 Current Z-Score: {zscore:.4f}")
        print("-" * 30)
        
        # Strong signals (immediate action)
        if zscore >= 2.0:
            print(f"🔴 STRONG SHORT SIGNAL! Z-score = {zscore:.4f}")
            print(f"   📉 Spread is extremely overvalued")
            print(f"   💡 Consider shorting NZDJPY and buying CADJPY")
            
        elif zscore <= -2.0:
            print(f"🟢 STRONG LONG SIGNAL! Z-score = {zscore:.4f}")
            print(f"   📈 Spread is extremely undervalued") 
            print(f"   💡 Consider buying NZDJPY and shorting CADJPY")
            
        # Regular signals
        elif zscore >= 1.0:
            print(f"🟠 SHORT SIGNAL: Z-score = {zscore:.4f}")
            print(f"   📉 Spread is overvalued")
            
        elif zscore <= -1.0:
            print(f"🟡 LONG SIGNAL: Z-score = {zscore:.4f}")
            print(f"   📈 Spread is undervalued")
            
        # Approaching signals (alerts)
        elif abs(zscore) >= self.alert_threshold:
            direction = "SHORT" if zscore > 0 else "LONG"
            print(f"⚠️  APPROACHING {direction} SIGNAL!")
            print(f"   Z-score = {zscore:.4f} (threshold ±{self.alert_threshold})")
            print(f"   🔔 Monitor closely for entry opportunity")
            
        # Neutral zone
        else:
            print(f"😴 NEUTRAL: Z-score = {zscore:.4f}")
            print(f"   📊 Spread is within normal range")
            
        print("-" * 30)

    def generate_position_sizing(self, zscore):
        """Generate position sizing recommendations"""
        if abs(zscore) >= 1.0:
            # Simple position sizing based on z-score magnitude
            base_size = min(abs(zscore), 3.0)  # Cap at 3x
            position_multiplier = base_size / 3.0
            
            print(f"\n💰 Position Sizing Recommendation:")
            print(f"   Base Position Multiplier: {position_multiplier:.2f}x")
            print(f"   Hedge Ratio: {self.hedge_ratio:.4f}")
            
            if zscore > 0:  # Short signal
                print(f"   📉 Short {position_multiplier:.2f} units NZDJPY")
                print(f"   📈 Long {position_multiplier * self.hedge_ratio:.2f} units CADJPY")
            else:  # Long signal
                print(f"   📈 Long {position_multiplier:.2f} units NZDJPY") 
                print(f"   📉 Short {position_multiplier * self.hedge_ratio:.2f} units CADJPY")

    def run_analysis(self):
        """Run complete analysis pipeline"""
        print(f"\n🚀 Starting Analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Download data
        data = self.download_data()
        if data is None:
            return False
        
        # Step 2: Test cointegration
        is_cointegrated, coint_score, p_value = self.calculate_cointegration(data)
        
        # Step 3: Calculate regression and spread
        spread = self.calculate_regression_and_spread(data)
        if spread is None:
            return False
        
        # Step 4: Calculate z-score
        zscore = self.calculate_zscore(spread)
        if zscore is None:
            return False
        
        # Step 5: Generate signals
        self.check_trading_signals(zscore)
        
        # Step 6: Position sizing
        self.generate_position_sizing(zscore)
        
        print("=" * 60)
        return True

    def run_continuous_monitoring(self, interval_minutes=60):
        """Run continuous monitoring with specified interval"""
        print(f"\n🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                success = self.run_analysis()
                if success:
                    print(f"\n⏰ Next check in {interval_minutes} minutes...")
                else:
                    print(f"\n❌ Analysis failed, retrying in {interval_minutes} minutes...")
                
                # Wait for next iteration
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Error in continuous monitoring: {e}")

def main():
    """Main function to run the monitor"""
    print("🎯 CADJPY/NZDJPY Pairs Trading Monitor")
    print("=====================================")
    
    # Initialize monitor
    monitor = ForexPairsMonitor(lookback_days=1460)  # ~4 years
    
    # Run single analysis
    print("\n1️⃣  Running single analysis...")
    monitor.run_analysis()
    
    # Ask user if they want continuous monitoring
    print("\n" + "="*60)
    response = input("\n🔄 Would you like to start continuous monitoring? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        try:
            interval = int(input("📅 Enter monitoring interval in minutes (default 60): ") or "60")
            monitor.run_continuous_monitoring(interval_minutes=interval)
        except ValueError:
            print("❌ Invalid interval, using default 60 minutes")
            monitor.run_continuous_monitoring(interval_minutes=60)
    else:
        print("👋 Single analysis complete. Goodbye!")

if __name__ == "__main__":
    main()
