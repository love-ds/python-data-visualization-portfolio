import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json

# =============================================================================
# 🛰️ PHASE 1: WEB SCRAPING & LIVE API INGESTION
# =============================================================================

def fetch_live_exchange_rate():
    """
    Fetches real-time USD to INR exchange rates using a free public REST API.
    Fallback hardcoded baseline avoids breaking execution during rate limits.
    """
    try:
        url = "https://er-api.com"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["rates"]["INR"]
    except Exception:
        pass
    return 84.50  # Stable institutional baseline fallback

def harvest_competitor_prices():
    """
    Simulates a highly robust web scraping harvest pipeline engine.
    Extracts unstructured data fields and passes them to the cleaning array.
    """
    # High-fidelity baseline dataset simulating harvested raw web elements
    # In a live production environment, this parses live requests/BeautifulSoup text
    np.random.seed(101)
    n_products = 50
    
    mock_raw_web_data = {
        "SKU": [f"PROD-{i:03d}" for i in range(1, n_products + 1)],
        "Product_Name": np.random.choice(["Enterprise Cloud Server", "Managed Database Instance", "AI Model Core API", "NVMe Storage Block", "Load Balancer Unit"], n_products),
        "Competitor_Name": np.random.choice(["ApexCloud", "VertexData", "QuantumHost"], n_products),
        "Raw_Price_USD": np.random.uniform(10, 500, n_products).round(2),
        "Availability": np.random.choice(["In Stock", "Out of Stock", "Limited Stock", None], n_products),
    }
    
    df_harvested = pd.DataFrame(mock_raw_web_data)
    
    # Introduce intentional unstructured discrepancies to prove cleaning skills
    df_harvested.loc[::5, "Raw_Price_USD"] = np.nan  # Corrupted data elements
    return df_harvested

# =============================================================================
# ⚙️ PHASE 2: AUTOMATED ETL PIPELINE ENGINE
# =============================================================================

def run_etl_pipeline():
    """
    Executes structural cleaning, standardisation, and currency sync vectors.
    """
    # 1. Extract
    raw_df = harvest_competitor_prices()
    inr_rate = fetch_live_exchange_rate()
    
    # 2. Transform
    cleaned_df = raw_df.copy()
    
    # Handle missing value records intelligently
    median_price = cleaned_df["Raw_Price_USD"].median()
    cleaned_df["Raw_Price_USD"] = cleaned_df["Raw_Price_USD"].fillna(median_price)
    cleaned_df["Availability"] = cleaned_df["Availability"].fillna("Unknown")
    
    # Live Cross-Currency Synchronization Calculations
    cleaned_df["Price_INR"] = (cleaned_df["Raw_Price_USD"] * inr_rate).round(2)
    
    # Advanced Derived Vectors (Internal Pricing Logic vs Competitor Target)
    cleaned_df["Our_Target_Price_INR"] = (cleaned_df["Price_INR"] * 0.92).round(2)  # Under-cutting strategy
    cleaned_df["Price_Delta_INR"] = (cleaned_df["Price_INR"] - cleaned_df["Our_Target_Price_INR"]).round(2)
    
    return cleaned_df, inr_rate


