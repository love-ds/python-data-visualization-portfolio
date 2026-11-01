import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# =============================================================================
# 🏢 SYSTEM CONFIGURATION & GLOBAL PREFERENCES
# =============================================================================
st.set_page_config(
    page_title="IPL Executive Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Deep Corporate Clean UI Theme Engine
def apply_corporate_theme(fig, title_text=""):
    fig.update_layout(
        template="plotly_white",
        title={
            'text': f"<b>{title_text}</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(family="Arial Black", size=18, color="#111827"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        hovermode="x unified",
        margin=dict(l=50, r=30, t=70, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor="#E5E7EB",
            tickfont=dict(family="Calibri", size=12, color="#4B5563"),
            title_font=dict(family="Calibri", size=14, color="#111827")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            showline=True,
            linewidth=1,
            linecolor="#E5E7EB",
            tickfont=dict(family="Calibri", size=12, color="#4B5563"),
            title_font=dict(family="Calibri", size=14, color="#111827")
        ),
        font=dict(family="Calibri", size=13, color="#1F2937")
    )
    fig.update_traces(
        selector=dict(type="bar"), 
        textposition="outside", 
        marker_line_width=0,
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=13)
    )
    fig.update_traces(
        selector=dict(type="pie"), 
        hole=0.45, 
        textinfo="percent+label",
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=13)
    )
    return fig

# =============================================================================
# 📥 DATA INGESTION PIPELINE (CACHED)
# =============================================================================
@st.cache_data
def ingest_and_engineer_data(uploaded_stream):
    if uploaded_stream is not None:
        data = pd.read_csv(uploaded_stream)
    else:
        # Use clearly labeled synthetic data when no CSV is uploaded.
        np.random.seed(42)
        n = 400
        teams = ["Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bengaluru", "Kolkata Knight Riders", "Delhi Capitals", "Punjab Kings"]
        venues = ["Wankhede Stadium", "MA Chidambaram Stadium", "M. Chinnaswamy Stadium", "Eden Gardens", "Arjun Jaitley Stadium"]
        data = pd.DataFrame({
            "match_id": np.arange(1001, 1001 + n),
            "date": pd.date_range("2016-04-01", periods=n, freq="W"),
            "team1": np.random.choice(teams, n),
            "team2": np.random.choice(teams, n),
            "venue": np.random.choice(venues, n),
            "match_winner": np.random.choice(teams, n),
            "toss_winner": np.random.choice(teams, n),
            "toss_decision": np.random.choice(["bat", "field"], n),
            "first_ings_score": np.random.randint(130, 240, n),
            "second_ings_score": np.random.randint(110, 220, n),
            "player_of_the_match": np.random.choice(["Virat Kohli", "MS Dhoni", "RG Sharma", "AB de Villiers", "JJ Bumrah"], n),
            "top_scorer": np.random.choice(["Virat Kohli", "MS Dhoni", "RG Sharma", "AB de Villiers"], n),
            "highscore": np.random.randint(35, 130, n),
            "best_bowling": np.random.choice(["JJ Bumrah", "YS Chahal", "SP Narine", "Rashid Khan"], n),
            "best_bowling_figure": np.random.choice(["4-12", "3-22", "5-18", "4-25"], n)
        })
    
    # Precise deterministic Feature Extraction
    data["highest_wickets"] = data["best_bowling_figure"].str.extract(r"(\d+)").astype(int)
    data["year"] = pd.to_datetime(data["date"]).dt.year
    data["month"] = pd.to_datetime(data["date"]).dt.month_name()
    data["day"] = pd.to_datetime(data["date"]).dt.day_name()
    return data

# =============================================================================
# 🎛️ CONTROL INTERFACE (SIDEBAR)
# =============================================================================
st.sidebar.markdown("### 🗂️ Data Workspace")
uploaded_file = st.sidebar.file_uploader("Upload Target IPL Dataset", type=["csv"])

df_master = ingest_and_engineer_data(uploaded_file)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Global Filters")

# Filter Component 1: Multi-Season Time Slicing
available_seasons = sorted(df_master["year"].unique())
selected_seasons = st.sidebar.multiselect(
    "Select Tournament Seasons", 
    options=available_seasons, 
    default=available_seasons
)

# Apply runtime slice mutations safely
df = df_master[df_master["year"].isin(selected_seasons)]

if df.empty:
    st.error("Data slice empty. Please adjust your global filter configurations.")
    st.stop()

# =============================================================================
# 📈 EXECUTIVE KPI FRAMEWORK
# =============================================================================
total_matches = df["match_id"].nunique()
total_teams = len(pd.unique(pd.concat([df["team1"], df["team2"]])))
total_venues = df["venue"].nunique()
highest_team_score = max(df["first_ings_score"].max(), df["second_ings_score"].max())
highest_individual_score = df["highscore"].max()

max_wickets_idx = df["highest_wickets"].idxmax()
best_bowling_fig = df.loc[max_wickets_idx, "best_bowling_figure"]
best_bowler_name = df.loc[max_wickets_idx, "best_bowling"]

# Render Core Workspace Header Matrix
st.title("🏏 IPL Analytics Executive Dashboard")
st.markdown("An institutional interface tracking performance distribution vectors across historic iterations.")

# =============================================================================
# 📊 RENDER CORRECTED KPI CARD GRID
# =============================================================================
# Unpack the list of 6 columns into 6 individual variables
col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)

# Assign each metric to its respective individual column variable
col_m1.metric("Total Matches", f"{total_matches:,}")
col_m2.metric("Unique Franchises", f"{total_teams}")
col_m3.metric("Stadium Footprint", f"{total_venues}")
col_m4.metric("Max Team Innings", f"{highest_team_score}")
col_m5.metric("Max Indiv Score", f"{highest_individual_score}")
col_m6.metric("Record Spell", f"{best_bowling_fig}", help=f"Delivered by {best_bowler_name}")


st.markdown("---")

# Navigation Hub
t1, t2, t3, t4 = st.tabs([
    "🛡️ Franchise Performance", 
    "🪙 Toss Dynamics", 
    "🏟️ Pitch & Venue Analytics", 
    "⚡ Athlete Analytics"
])


# =============================================================================
# 🛡️ TAB 1: FRANCHISE PERFORMANCE VIEW
# =============================================================================
with t1:
    st.subheader("Franchise Performance Metrics")
    
    # Clean pill selection interface for layout navigation
    team_view_mode = st.pills(
        "Select Metric Focus Matrix",
        options=[
            "Win Metrics & Ratios", 
            "Innings Score Margins", 
            "Chasing vs Defending Efficiency"
        ],
        default="Win Metrics & Ratios"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- METRIC OPTION 1: WIN DISTRIBUTIONS ---
    if team_view_mode == "Win Metrics & Ratios":
        # Split into exactly 2 columns to prevent overlapping plots
        col1, col2 = st.columns(2)
        
        # Ingestion calculations
        team_wins = df["match_winner"].value_counts().reset_index()
        team_wins.columns = ["Team", "Matches Won"]
        
        matches_played = pd.concat([df["team1"], df["team2"]]).value_counts().reset_index()
        matches_played.columns = ["Team", "Matches Played"]
        
        team_perf = pd.merge(matches_played, team_wins, on="Team", how="left").fillna(0)
        team_perf["Win Percentage"] = ((team_perf["Matches Won"] / team_perf["Matches Played"]) * 100).round(2)
        team_perf = team_perf.sort_values(by="Win Percentage", ascending=False)
        
        with col1:
            fig_wins = px.bar(
                team_wins, 
                x="Team", 
                y="Matches Won", 
                color="Matches Won", 
                text="Matches Won",
                color_continuous_scale="Blugrn"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_wins, "Total Absolute Wins by Franchise"), 
                use_container_width=True,
                key="tab1_total_wins"
            )
            
        with col2:
            fig_ratio = px.bar(
                team_perf, 
                x="Team", 
                y="Win Percentage", 
                color="Win Percentage", 
                text="Win Percentage",
                color_continuous_scale="Mint"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_ratio, "Proportional Win Ratios (%) per Franchise"), 
                use_container_width=True,
                key="tab1_win_ratios"
            )

    # --- METRIC OPTION 2: SCORE MARGINS ---
    elif team_view_mode == "Total & Innings Run Distributions":
        col1, col2 = st.columns(2)
        
        first_ings = df.groupby("team1", as_index=False)["first_ings_score"].agg(["sum", "mean"])
        first_ings.columns = ["Team", "Runs_1st_Sum", "Avg_1st"]
        
        second_ings = df.groupby("team2", as_index=False)["second_ings_score"].agg(["sum", "mean"])
        second_ings.columns = ["Team", "Runs_2nd_Sum", "Avg_2nd"]
        
        runs_combined = pd.merge(first_ings, second_ings, on="Team", how="outer").fillna(0)
        runs_combined["Total Runs"] = runs_combined["Runs_1st_Sum"] + runs_combined["Runs_2nd_Sum"]
        runs_combined = runs_combined.sort_values(by="Total Runs", ascending=False)
        
        with col1:
            fig_tot_runs = px.bar(
                runs_combined, 
                x="Team", 
                y="Total Runs", 
                color="Total Runs", 
                text="Total Runs",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_tot_runs, "Cumulative Aggregated Runs Contributed"), 
                use_container_width=True,
                key="tab1_cum_runs"
            )
            
        with col2:
            avg_melted = pd.melt(
                runs_combined, 
                id_vars=["Team"], 
                value_vars=["Avg_1st", "Avg_2nd"], 
                var_name="Innings", 
                value_name="Average Score"
            )
            avg_melted["Innings"] = avg_melted["Innings"].map({"Avg_1st": "1st Innings Target", "Avg_2nd": "2nd Innings Target"})
            
            fig_avg_profile = px.bar(
                avg_melted, 
                x="Team", 
                y="Average Score", 
                color="Innings", 
                barmode="group",
                color_discrete_sequence=["#1E3A8A", "#10B981"]
            )
            st.plotly_chart(
                apply_corporate_theme(fig_avg_profile, "Target Profile Density: 1st vs 2nd Innings"), 
                use_container_width=True,
                key="tab1_avg_targets"
            )

    # --- METRIC OPTION 3: STRATEGY BALANCES ---
    elif team_view_mode == "Chasing vs Defending Efficiency":
        # Render as a wide-format standalone chart to give it optimal layout breathing room
        bat_first_wins = df[df["team1"] == df["match_winner"]].groupby("team1").size().reset_index(name="Wins_Bat_First").rename(columns={"team1": "Team"})
        chasing_wins = df[df["team2"] == df["match_winner"]].groupby("team2").size().reset_index(name="Wins_Chasing").rename(columns={"team2": "Team"})
        
        strat_df = pd.merge(bat_first_wins, chasing_wins, on="Team", how="outer").fillna(0)
        
        fig_strat = px.bar(
            strat_df, 
            x="Team", 
            y=["Wins_Bat_First", "Wins_Chasing"], 
            barmode="group",
            labels={"value": "Matches Won", "variable": "Strategic Play"},
            color_discrete_sequence=["#3B82F6", "#F59E0B"]
        )
        st.plotly_chart(
            apply_corporate_theme(fig_strat, "Defending Totals vs Chasing Targets Strategic Success Matrix"), 
            use_container_width=True,
            key="tab1_strat_play"
        )

# =============================================================================
# 🪙 TAB 2: TOSS DYNAMICS VIEW
# =============================================================================
with t2:
    st.subheader("Decision Mechanics & Match Impact Analytics")
    
    # Checkbox filter in dashboard space to isolate specific match conditions
    show_toss_percentage = st.toggle("Switch Chart View to Percentages", value=False)
    
    # 2-column breakdown: Left for Team distributions, Right for global pie proportions
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        # TOSS WINS BY TEAM
        toss_wins = df["toss_winner"].value_counts().reset_index()
        toss_wins.columns = ["Team", "Toss Wins"]
        
        fig_toss_team = px.bar(
            toss_wins, 
            x="Team", 
            y="Toss Wins", 
            color="Toss Wins", 
            text="Toss Wins",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(
            apply_corporate_theme(fig_toss_team, "Absolute Toss Wins by Franchise"), 
            use_container_width=True,
            key="tab2_toss_wins"
        )
        
    with col2:
        # CAPTAIN DECISION PIE CHART
        toss_dec = df["toss_decision"].value_counts().reset_index()
        toss_dec.columns = ["Decision", "Count"]
        
        toss_dec_title = "Captain Strategic Choices Post-Toss"
        if show_toss_percentage:
            toss_dec_title += " (Ratio Distribution)"
            
        fig_toss_pie = px.pie(
            toss_dec, 
            names="Decision", 
            values="Count",
            color_discrete_sequence=["#1D4ED8", "#10B981"]
        )
        st.plotly_chart(
            apply_corporate_theme(fig_toss_pie, toss_dec_title), 
            use_container_width=True,
            key="tab2_toss_pie"
        )
        
    st.markdown("---")
    
    # Single structural column breakout row at the bottom for impact correlation
    st.markdown("#### The Toss Victory Correlation Vector")
    df["toss_match_result"] = np.where(df["toss_winner"] == df["match_winner"], "Toss Winner Won Match", "Toss Winner Lost Match")
    toss_imp = df["toss_match_result"].value_counts().reset_index()
    toss_imp.columns = ["Result", "Matches"]
    
    fig_impact = px.bar(
        toss_imp,
        x="Result",
        y="Matches",
        color="Result",
        text="Matches",
        color_discrete_map={"Toss Winner Won Match": "#059669", "Toss Winner Lost Match": "#DC2626"}
    )
    # Constrain the size here explicitly so a 1-row item doesn't look stretched or overlapping
    fig_impact.update_layout(height=450)
    st.plotly_chart(
        apply_corporate_theme(fig_impact, "Did Winning the Toss Direct the Eventual Match Outcome?"), 
        use_container_width=True,
        key="tab2_toss_impact"
    )


# =============================================================================
# 🏟️ TAB 3: PITCH & VENUE ANALYTICS VIEW
# =============================================================================
with t3:
    st.subheader("Stadium Workloads & Pitch Character Vector")
    
    # Contextual dynamic operational filter built directly within the tab layout
    venue_analysis_focus = st.selectbox(
        "Isolate Ground Condition Matrix",
        options=[
            "Total Matches Allocated per Venue", 
            "Pitch Behavior (First vs Second Innings Target Ratios)"
        ],
        key="tab3_analysis_focus_select"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- METRIC OPTION 1: ABSOLUTE GROUND WORKLOADS ---
    if venue_analysis_focus == "Total Matches Allocated per Venue":
        # Group and rank stadiums by usage density
        venue_matches = df["venue"].value_counts().reset_index()
        venue_matches.columns = ["Venue", "Matches Hosted"]
        
        fig_venue_load = px.bar(
            venue_matches,
            x="Venue",
            y="Matches Hosted",
            color="Matches Hosted",
            text="Matches Hosted",
            color_continuous_scale="Cividis"
        )
        # Give a slight angle to x-axis ticks to handle long stadium titles cleanly
        fig_venue_load.update_xaxes(tickangle=-45)
        st.plotly_chart(
            apply_corporate_theme(fig_venue_load, "Distribution Profile of Matches Hosted across Stadiums"),
            use_container_width=True,
            key="tab3_venue_load_graph"
        )
        
    # --- METRIC OPTION 2: TARGET PROFILES & INNINGS CHARACTER ---
    elif venue_analysis_focus == "Pitch Behavior (First vs Second Innings Target Ratios)":
        df["total_match_runs"] = df["first_ings_score"] + df["second_ings_score"]
        
        venue_runs = df.groupby("venue").agg(
            Avg_Total=("total_match_runs", "mean"),
            Avg_1st=("first_ings_score", "mean"),
            Avg_2nd=("second_ings_score", "mean")
        ).reset_index().sort_values(by="Avg_Total", ascending=False)
        
        # Melt dataframe down to stack vectors structurally side-by-side
        melted_venues = pd.melt(
            venue_runs, 
            id_vars=["venue"], 
            value_vars=["Avg_1st", "Avg_2nd"], 
            var_name="Innings Type", 
            value_name="Runs Matrix"
        )
        melted_venues["Innings Type"] = melted_venues["Innings Type"].map({
            "Avg_1st": "1st Innings Target Average", 
            "Avg_2nd": "2nd Innings Target Average"
        })
        melted_venues.rename(columns={"venue": "Venue"}, inplace=True)
        
        fig_pitch_char = px.bar(
            melted_venues,
            x="Venue",
            y="Runs Matrix",
            color="Innings Type",
            barmode="group",
            color_discrete_sequence=["#1F2937", "#10B981"]
        )
        fig_pitch_char.update_xaxes(tickangle=-45)
        st.plotly_chart(
            apply_corporate_theme(fig_pitch_char, "Pitch Character Vector: Defending Targets vs Chasing Thresholds"),
            use_container_width=True,
            key="tab3_pitch_behavior_graph"
        )

# =============================================================================
# ⚡ TAB 4: ATHLETE ANALYTICS VIEW
# =============================================================================
with t4:
    st.subheader("Athlete Performance Metrics & Profiles")
    
    # In-tab selector separating disciplines to optimize system memory footprint
    athlete_focus = st.selectbox(
        "Choose Athlete Discipline Matrix",
        options=["Batting Dominance Index", "Bowling Performance Matrix"],
        key="tab4_discipline_focus_select"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- METRIC OPTION 1: BATTING DOMINANCE INDEX ---
    if athlete_focus == "Batting Dominance Index":
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 run-scorers aggregation
            top_runs = df.groupby("top_scorer", as_index=False)["highscore"].sum().sort_values(by="highscore", ascending=False).head(10)
            fig_bat_runs = px.bar(
                top_runs, 
                x="top_scorer", 
                y="highscore", 
                color="highscore", 
                labels={"top_scorer": "Player", "highscore": "Aggregate Runs"},
                color_continuous_scale="Purples"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_bat_runs, "Top 10 Athlete Aggregate Run Leaders"), 
                use_container_width=True,
                key="tab4_bat_runs_graph"
            )
            
        with col2:
            # Top 10 individual high scores
            top_scores = df.groupby("top_scorer", as_index=False)["highscore"].max().sort_values(by="highscore", ascending=False).head(10)
            fig_bat_peaks = px.bar(
                top_scores, 
                x="top_scorer", 
                y="highscore", 
                color="highscore", 
                labels={"top_scorer": "Player", "highscore": "Peak Personal Score"},
                color_continuous_scale="RdPu"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_bat_peaks, "Top 10 Peak Innings Records"), 
                use_container_width=True,
                key="tab4_bat_peaks_graph"
            )
            
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            # Systemic distribution profile histogram
            fig_dist = px.histogram(
                df, 
                x="highscore", 
                nbins=20, 
                title="Systemic Distribution Spread of Top Individual Scores",
                color_discrete_sequence=["#4B5563"]
            )
            st.plotly_chart(
                apply_corporate_theme(fig_dist, "Systemic Highscore Distribution Density"), 
                use_container_width=True,
                key="tab4_highscore_dist_graph"
            )
            
        with col4:
            # Innings quality indexing over chronological progression
            yearly_high = df.groupby("year", as_index=False)["highscore"].mean()
            fig_trend = px.line(
                yearly_high, 
                x="year", 
                y="highscore", 
                markers=True,
                color_discrete_sequence=["#D97706"]
            )
            st.plotly_chart(
                apply_corporate_theme(fig_trend, "Chronological Innings Quality Trend (Average Innings Score)"), 
                use_container_width=True,
                key="tab4_innings_trend_graph"
            )

    # --- METRIC OPTION 2: BOWLING PERFORMANCE MATRIX ---
    elif athlete_focus == "Bowling Performance Matrix":
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 wicket-takers aggregation
            top_wickets = df.groupby("best_bowling", as_index=False)["highest_wickets"].sum().sort_values(by="highest_wickets", ascending=False).head(10)
            fig_bowl_w = px.bar(
                top_wickets, 
                x="best_bowling", 
                y="highest_wickets", 
                color="highest_wickets", 
                labels={"best_bowling": "Bowler", "highest_wickets": "Total Wickets Taken"},
                color_continuous_scale="Teal"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_bowl_w, "Top 10 Aggregate Wicket Takers"), 
                use_container_width=True,
                key="tab4_bowl_wickets_graph"
            )
            
        with col2:
            # Most frequent best bowlers matching original logic
            most_best_bowler = df["best_bowling"].value_counts().reset_index().head(10)
            most_best_bowler.columns = ["Bowler", "Matches as Primary Bowler"]
            
            fig_bowl_freq = px.bar(
                most_best_bowler, 
                x="Bowler", 
                y="Matches as Primary Bowler", 
                color="Matches as Primary Bowler",
                color_continuous_scale="Oranges"
            )
            st.plotly_chart(
                apply_corporate_theme(fig_bowl_freq, "Bowlers Finishing Most Frequently with Best Figures"), 
                use_container_width=True,
                key="tab4_bowl_freq_graph"
            )

