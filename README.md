# Python Data Visualization Portfolio

Interactive dashboards and data preparation projects built with Python, Streamlit, pandas, NumPy, and Plotly.

## Projects

- **Sales Dashboard (`app.py`)** — Upload a CSV and explore sales and profit summaries. The app checks that the file contains the required columns and uses generated sample data when no file is uploaded.
- **IPL Analytics (`IPL_Streamlit_Dashboard.py`)** — Explore team, toss, venue, batting, and bowling metrics. Upload a compatible IPL CSV or use the generated sample data. Sample-data results are not historical IPL findings.
- **Market Pricing Demo (`market_app.py`)** — Demonstrates a data preparation workflow with simulated competitor records, USD-to-INR conversion, and sample target prices. It does not scrape live competitor websites.

## Setup

Use Python 3.10 or newer. Open a terminal in this folder and install the required packages:

    python -m pip install -r requirements.txt

Start a dashboard with one of these commands:

    streamlit run app.py
    streamlit run IPL_Streamlit_Dashboard.py
    streamlit run market_app.py

Keep `market_app.py` and `pipeline.py` together in the same folder.

## IPL data

The IPL dashboard expects columns such as `match_id`, `date`, `team1`, `team2`, `venue`, `match_winner`, `toss_winner`, `toss_decision`, `first_ings_score`, `second_ings_score`, `highscore`, `best_bowling`, and `best_bowling_figure`. Only upload data you have permission to share.
