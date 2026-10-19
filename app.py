"""Interactive IPL Cricket Analytics Dashboard.

Author: Sudhir Kumar (GitHub: Sudhir-2211)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.analytics import IPLAnalytics

# Page configuration
st.set_page_config(
    page_title="IPL Cricket Analytics | Sudhir Kumar",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #D97706;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">🏏 IPL Cricket Analytics & Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Interactive historical cricket intelligence covering 17 seasons (2008–2024): franchise standings, head-to-head records, toss impact, and player leaderboards.</div>',
    unsafe_allow_html=True,
)

analytics = IPLAnalytics()
seasons = analytics.get_seasons()
teams = analytics.get_teams()

# Sidebar: Global Filter
st.sidebar.header("🎯 Analytics Controls")
selected_season = st.sidebar.selectbox("Select IPL Season", ["All Seasons"] + seasons, index=len(seasons))

# Main Tabs
tab_summary, tab_h2h, tab_players, tab_toss, tab_venues, tab_provenance = st.tabs([
    "🏆 Season Standings & Champions",
    "⚔️ Team Head-to-Head",
    "🏏 Player Leaderboards",
    "🪙 Toss Impact Analysis",
    "🏟️ Venue Scoring Trends",
    "ℹ️ Data Provenance & Ethics",
])

# Tab 1: Season Summary & Championship
with tab_summary:
    st.subheader("Franchise Championship Honours (2008–2024)")
    titles_df = analytics.get_championship_titles()

    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.dataframe(titles_df, use_container_width=True)
    with col_t2:
        fig_titles = px.bar(
            titles_df,
            x="Franchise",
            y="Titles Won",
            color="Titles Won",
            text="Titles Won",
            color_continuous_scale="Viridis",
        )
        fig_titles.update_traces(textposition="outside")
        fig_titles.update_layout(margin=dict(t=20, b=20, l=20, r=20), coloraxis_showscale=False)
        st.plotly_chart(fig_titles, use_container_width=True)

    st.markdown("---")
    if selected_season != "All Seasons":
        st.subheader(f"Season {selected_season} Points Table")
        pts_df = analytics.get_points_table(int(selected_season))
        st.dataframe(pts_df, use_container_width=True)
    else:
        st.subheader("Season-by-Season Points Tables")
        sample_season = st.selectbox("Select Season to View Table", seasons, index=len(seasons) - 1)
        pts_df = analytics.get_points_table(int(sample_season))
        st.dataframe(pts_df, use_container_width=True)

# Tab 2: Head-to-Head
with tab_h2h:
    st.subheader("Franchise Head-to-Head Rivalry Comparison")
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        team1 = st.selectbox("Select Team 1", teams, index=0)
    with h_col2:
        team2 = st.selectbox("Select Team 2", [t for t in teams if t != team1], index=0)

    h2h = analytics.get_team_head_to_head(team1, team2)

    if h2h["total_matches"] > 0:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(f"{team1} Wins", f"{h2h['team1_wins']}", delta=f"{h2h['team1_win_pct']}% Win Rate")
        with c2:
            st.metric("Total Matches Played", f"{h2h['total_matches']}")
        with c3:
            st.metric(f"{team2} Wins", f"{h2h['team2_wins']}", delta=f"{h2h['team2_win_pct']}% Win Rate")

        # Visual Comparison Bar
        comp_df = pd.DataFrame([
            {"Franchise": team1, "Wins": h2h["team1_wins"]},
            {"Franchise": team2, "Wins": h2h["team2_wins"]},
        ])
        fig_h2h = px.bar(
            comp_df,
            x="Franchise",
            y="Wins",
            color="Franchise",
            text="Wins",
            color_discrete_sequence=["#1E3A8A", "#D97706"],
        )
        fig_h2h.update_traces(textposition="outside")
        fig_h2h.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_h2h, use_container_width=True)

        st.write("#### 📜 Recent Encounters")
        st.dataframe(h2h["recent_matches"][["season", "date", "venue", "toss_winner", "toss_decision", "winner", "won_by", "margin"]], use_container_width=True)
    else:
        st.info("No recorded matches between the selected franchises.")

# Tab 3: Player Leaderboards
with tab_players:
    st.subheader("All-Time Career Player Leaderboards")
    p_role = st.radio("Select Role", ["🏏 Batting Milestones", "🎯 Bowling Milestones"], horizontal=True)

    if "Batting" in p_role:
        metric = st.selectbox("Sort Batting By", ["runs", "strike_rate", "average", "centuries", "sixes", "fours"])
        top_batsmen = analytics.get_top_batsmen(sort_by=metric, limit=15)
        st.dataframe(top_batsmen, use_container_width=True)

        fig_bat = px.bar(
            top_batsmen.head(10),
            x="player",
            y=metric,
            color="team",
            text=metric,
            labels={"player": "Batsman", metric: metric.replace("_", " ").title()},
            title=f"Top 10 Batsmen by {metric.replace('_', ' ').title()}",
        )
        fig_bat.update_traces(textposition="outside")
        fig_bat.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_bat, use_container_width=True)

    else:
        metric = st.selectbox("Sort Bowling By", ["wickets", "economy", "average", "strike_rate", "four_wickets"])
        top_bowlers = analytics.get_top_bowlers(sort_by=metric, limit=15)
        st.dataframe(top_bowlers, use_container_width=True)

        fig_bowl = px.bar(
            top_bowlers.head(10),
            x="player",
            y=metric,
            color="team",
            text=metric,
            labels={"player": "Bowler", metric: metric.replace("_", " ").title()},
            title=f"Top 10 Bowlers by {metric.replace('_', ' ').title()}",
        )
        fig_bowl.update_traces(textposition="outside")
        fig_bowl.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_bowl, use_container_width=True)

# Tab 4: Toss Impact
with tab_toss:
    st.subheader("Does Winning the Toss Decide the Match?")
    season_val = None if selected_season == "All Seasons" else int(selected_season)
    toss_stats = analytics.get_toss_impact(season=season_val)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Matches", f"{toss_stats['total_matches']}")
    with m2:
        st.metric("Toss & Match Win %", f"{toss_stats['toss_and_match_win_pct']}%")
    with m3:
        st.metric("Elected to Field %", f"{toss_stats['decision_field_pct']}%")
    with m4:
        st.metric("Chasing Team Win %", f"{toss_stats['chasing_win_pct']}%")

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.write("#### Toss Decision Distribution")
        fig_dec = px.pie(
            values=[toss_stats["decision_field_count"], toss_stats["decision_bat_count"]],
            names=["Field First", "Bat First"],
            hole=0.45,
            color_discrete_sequence=["#059669", "#DC2626"],
        )
        st.plotly_chart(fig_dec, use_container_width=True)

    with t_col2:
        st.write("#### Match Outcome: Defending vs Chasing")
        fig_out = px.pie(
            values=[toss_stats["defending_wins"], toss_stats["chasing_wins"]],
            names=["Defending (Won by Runs)", "Chasing (Won by Wickets)"],
            hole=0.45,
            color_discrete_sequence=["#D97706", "#2563EB"],
        )
        st.plotly_chart(fig_out, use_container_width=True)

# Tab 5: Venues
with tab_venues:
    st.subheader("Stadium Scoring Patterns & Chasing Advantage")
    venue_df = analytics.get_venue_scoring_trends()
    st.dataframe(venue_df, use_container_width=True)

    fig_venue = px.scatter(
        venue_df,
        x="avg_1st_innings",
        y="chasing_win_pct",
        size="matches_played",
        text="venue",
        color="chasing_win_pct",
        color_continuous_scale="Plasma",
        labels={"avg_1st_innings": "Average 1st Innings Total", "chasing_win_pct": "Chasing Win %"},
        title="Venue Profile: 1st Innings Par Score vs Chasing Advantage",
    )
    fig_venue.update_traces(textposition="top center")
    fig_venue.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_venue, use_container_width=True)

# Tab 6: Provenance
with tab_provenance:
    st.subheader("Data Sources, Integrity & Responsible Analytics")
    st.markdown(
        """
        ### 📋 Dataset Source & Provenance
        - **Historical Career Player Records**: Sourced from official public Indian Premier League records and ESPNCricinfo statistical archives (2008–2024). Player statistics for top run-getters (e.g., Virat Kohli: 8,004 runs, Shikhar Dhawan: 6,769 runs) and top wicket-takers (e.g., Yuzvendra Chahal: 205 wickets) reflect verified official standings.
        - **Match Logs**: Public match summaries matching official BCCI / Cricsheet historical schedules from Season 1 (2008) through Season 17 (2024).
        - **Integrity Notice**: In accordance with academic and placement integrity standards, all figures are strictly based on authentic public sports databases.
        """
    )
