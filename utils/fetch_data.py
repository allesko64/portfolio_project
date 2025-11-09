import yfinance as yf
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

symbols = ["INFY.NS", "TCS.NS", "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS"]

for s in symbols:
    print(f"Fetching {s}...")
    try:
        ticker = yf.Ticker(s)
        df = ticker.history(period="10y", interval="1d")  # more reliable than yf.download

        if df.empty:
            print(f"⚠️ No data for {s}, skipping.")
            continue

        df_monthly = df.resample("M").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last"
        }).dropna()

        if df_monthly.empty:
            print(f"⚠️ {s} returned no monthly data after resampling, skipping.")
            continue

        path = f"data/{s.replace('.NS','')}_monthly.csv"
        df_monthly.to_csv(path)
        print(f"✅ Saved {path}")

    except Exception as e:
        print(f"❌ Error fetching {s}: {e}")

print("🎯 Done!")
