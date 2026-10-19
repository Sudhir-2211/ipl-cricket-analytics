"""Automated unit tests for IPL Cricket Analytics."""

import pytest
import pandas as pd
from src.analytics import IPLAnalytics


@pytest.fixture(scope="module")
def analytics():
    return IPLAnalytics()


def test_data_loading(analytics):
    assert not analytics.matches_df.empty
    assert len(analytics.matches_df) >= 1000
    assert not analytics.batting_df.empty
    assert not analytics.bowling_df.empty
    assert "player" in analytics.batting_df.columns
    assert "wickets" in analytics.bowling_df.columns


def test_seasons_list(analytics):
    seasons = analytics.get_seasons()
    assert 2008 in seasons
    assert 2024 in seasons
    assert len(seasons) == 17


def test_points_table_sanity(analytics):
    pts = analytics.get_points_table(2023)
    assert not pts.empty
    assert "Played" in pts.columns
    assert "Won" in pts.columns
    assert "Points" in pts.columns
    assert (pts["Played"] == pts["Won"] + pts["Lost"]).all()
    assert (pts["Points"] == pts["Won"] * 2).all()
    # Check descending order by Points
    assert list(pts["Points"]) == sorted(list(pts["Points"]), reverse=True)


def test_championship_titles(analytics):
    titles = analytics.get_championship_titles()
    assert not titles.empty
    assert "Mumbai Indians" in titles["Franchise"].values
    assert "Chennai Super Kings" in titles["Franchise"].values
    # Total titles across 17 seasons must equal 17
    assert titles["Titles Won"].sum() == 17


def test_team_head_to_head(analytics):
    res = analytics.get_team_head_to_head("Mumbai Indians", "Chennai Super Kings")
    assert res["total_matches"] > 0
    assert res["team1_wins"] + res["team2_wins"] == res["total_matches"]
    assert res["team1_win_pct"] >= 0.0 and res["team1_win_pct"] <= 100.0


def test_toss_impact(analytics):
    toss = analytics.get_toss_impact()
    assert toss["total_matches"] > 1000
    assert 0 <= toss["toss_and_match_win_pct"] <= 100
    assert 0 <= toss["decision_field_pct"] <= 100
    assert toss["chasing_wins"] + toss["defending_wins"] == toss["total_matches"]


def test_top_batsmen(analytics):
    top_runs = analytics.get_top_batsmen("runs", limit=5)
    assert len(top_runs) == 5
    # Virat Kohli is career leading run scorer (> 8000 runs)
    assert top_runs.iloc[0]["player"] == "Virat Kohli"
    assert top_runs.iloc[0]["runs"] >= 8000


def test_top_bowlers(analytics):
    top_wickets = analytics.get_top_bowlers("wickets", limit=5)
    assert len(top_wickets) == 5
    # Yuzvendra Chahal is all-time leading wicket taker (> 200 wickets)
    assert top_wickets.iloc[0]["player"] == "Yuzvendra Chahal"
    assert top_wickets.iloc[0]["wickets"] >= 200


def test_venue_scoring_trends(analytics):
    venues = analytics.get_venue_scoring_trends()
    assert not venues.empty
    assert "avg_1st_innings" in venues.columns
    assert (venues["avg_1st_innings"] > 140).all()
    assert (venues["avg_1st_innings"] < 220).all()
