"""IPL Cricket Analytics Engine.

Provides analytical queries, points table computations, head-to-head metrics,
toss impact calculations, and player rankings.
Author: Sudhir Kumar (GitHub: Sudhir-2211)
"""

import os
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np


class IPLAnalytics:
    """Core analytics engine for Indian Premier League historical records."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        self.data_dir = data_dir
        self.matches_df = pd.read_csv(os.path.join(data_dir, "matches.csv"))
        self.batting_df = pd.read_csv(os.path.join(data_dir, "player_batting.csv"))
        self.bowling_df = pd.read_csv(os.path.join(data_dir, "player_bowling.csv"))

    def get_seasons(self) -> List[int]:
        """Returns sorted list of available IPL seasons."""
        return sorted(self.matches_df["season"].unique().tolist())

    def get_teams(self) -> List[str]:
        """Returns sorted list of all active franchises."""
        teams = set(self.matches_df["team1"].unique()).union(set(self.matches_df["team2"].unique()))
        return sorted(list(teams))

    def get_points_table(self, season: int) -> pd.DataFrame:
        """Computes points table for a specific IPL season."""
        df_season = self.matches_df[self.matches_df["season"] == season]
        if df_season.empty:
            return pd.DataFrame()

        teams = set(df_season["team1"].unique()).union(set(df_season["team2"].unique()))
        table_rows = []

        for team in sorted(teams):
            played = len(df_season[(df_season["team1"] == team) | (df_season["team2"] == team)])
            won = len(df_season[df_season["winner"] == team])
            lost = played - won
            pts = won * 2
            win_pct = round((won / played) * 100.0, 1) if played > 0 else 0.0

            table_rows.append({
                "Team": team,
                "Played": played,
                "Won": won,
                "Lost": lost,
                "Points": pts,
                "Win %": win_pct,
            })

        points_df = pd.DataFrame(table_rows)
        return points_df.sort_values(by=["Points", "Win %"], ascending=False).reset_index(drop=True)

    def get_championship_titles(self) -> pd.DataFrame:
        """Returns count of IPL titles per franchise."""
        # Known official champion records (2008 to 2024)
        champions_history = [
            {"Season": 2008, "Champion": "Rajasthan Royals", "Runner-Up": "Chennai Super Kings"},
            {"Season": 2009, "Champion": "Sunrisers Hyderabad", "Runner-Up": "Royal Challengers Bengaluru"},
            {"Season": 2010, "Champion": "Chennai Super Kings", "Runner-Up": "Mumbai Indians"},
            {"Season": 2011, "Champion": "Chennai Super Kings", "Runner-Up": "Royal Challengers Bengaluru"},
            {"Season": 2012, "Champion": "Kolkata Knight Riders", "Runner-Up": "Chennai Super Kings"},
            {"Season": 2013, "Champion": "Mumbai Indians", "Runner-Up": "Chennai Super Kings"},
            {"Season": 2014, "Champion": "Kolkata Knight Riders", "Runner-Up": "Punjab Kings"},
            {"Season": 2015, "Champion": "Mumbai Indians", "Runner-Up": "Chennai Super Kings"},
            {"Season": 2016, "Champion": "Sunrisers Hyderabad", "Runner-Up": "Royal Challengers Bengaluru"},
            {"Season": 2017, "Champion": "Mumbai Indians", "Runner-Up": "Rising Pune Supergiant"},
            {"Season": 2018, "Champion": "Chennai Super Kings", "Runner-Up": "Sunrisers Hyderabad"},
            {"Season": 2019, "Champion": "Mumbai Indians", "Runner-Up": "Chennai Super Kings"},
            {"Season": 2020, "Champion": "Mumbai Indians", "Runner-Up": "Delhi Capitals"},
            {"Season": 2021, "Champion": "Chennai Super Kings", "Runner-Up": "Kolkata Knight Riders"},
            {"Season": 2022, "Champion": "Gujarat Titans", "Runner-Up": "Rajasthan Royals"},
            {"Season": 2023, "Champion": "Chennai Super Kings", "Runner-Up": "Gujarat Titans"},
            {"Season": 2024, "Champion": "Kolkata Knight Riders", "Runner-Up": "Sunrisers Hyderabad"},
        ]
        df_champ = pd.DataFrame(champions_history)
        titles = df_champ["Champion"].value_counts().reset_index()
        titles.columns = ["Franchise", "Titles Won"]
        return titles

    def get_team_head_to_head(self, team1: str, team2: str) -> Dict[str, Any]:
        """Computes head-to-head match records between two teams."""
        mask = (
            ((self.matches_df["team1"] == team1) & (self.matches_df["team2"] == team2)) |
            ((self.matches_df["team1"] == team2) & (self.matches_df["team2"] == team1))
        )
        h2h_matches = self.matches_df[mask]
        total_matches = len(h2h_matches)

        if total_matches == 0:
            return {
                "total_matches": 0,
                "team1_wins": 0,
                "team2_wins": 0,
                "team1_win_pct": 0.0,
                "team2_win_pct": 0.0,
                "matches": pd.DataFrame(),
            }

        t1_wins = int((h2h_matches["winner"] == team1).sum())
        t2_wins = int((h2h_matches["winner"] == team2).sum())

        return {
            "total_matches": total_matches,
            "team1": team1,
            "team2": team2,
            "team1_wins": t1_wins,
            "team2_wins": t2_wins,
            "team1_win_pct": round((t1_wins / total_matches) * 100.0, 1),
            "team2_win_pct": round((t2_wins / total_matches) * 100.0, 1),
            "recent_matches": h2h_matches.sort_values(by="season", ascending=False).head(5),
        }

    def get_toss_impact(self, season: Optional[int] = None) -> Dict[str, Any]:
        """Analyzes correlation between winning the coin toss and winning the match."""
        df = self.matches_df if season is None else self.matches_df[self.matches_df["season"] == season]
        total = len(df)
        if total == 0:
            return {"total_matches": 0, "toss_and_match_win_pct": 0.0, "decision_field_pct": 0.0}

        toss_and_match_wins = int((df["toss_winner"] == df["winner"]).sum())
        field_decisions = int((df["toss_decision"] == "field").sum())
        chasing_wins = int((df["won_by"] == "wickets").sum())
        defending_wins = int((df["won_by"] == "runs").sum())

        return {
            "total_matches": total,
            "toss_and_match_wins": toss_and_match_wins,
            "toss_and_match_win_pct": round((toss_and_match_wins / total) * 100.0, 1),
            "decision_field_count": field_decisions,
            "decision_field_pct": round((field_decisions / total) * 100.0, 1),
            "decision_bat_count": total - field_decisions,
            "decision_bat_pct": round(((total - field_decisions) / total) * 100.0, 1),
            "chasing_wins": chasing_wins,
            "chasing_win_pct": round((chasing_wins / total) * 100.0, 1),
            "defending_wins": defending_wins,
            "defending_win_pct": round((defending_wins / total) * 100.0, 1),
        }

    def get_venue_scoring_trends(self) -> pd.DataFrame:
        """Computes scoring averages and boundary frequencies across venues."""
        summary = (
            self.matches_df.groupby("venue")
            .agg(
                matches_played=("match_id", "count"),
                avg_1st_innings=("first_innings_score", "mean"),
                highest_1st_innings=("first_innings_score", "max"),
                chasing_wins=("won_by", lambda x: (x == "wickets").sum()),
            )
            .reset_index()
        )
        summary["avg_1st_innings"] = summary["avg_1st_innings"].round(1)
        summary["chasing_win_pct"] = (
            (summary["chasing_wins"] / summary["matches_played"]) * 100.0
        ).round(1)
        return summary.sort_values(by="matches_played", ascending=False).reset_index(drop=True)

    def get_top_batsmen(self, sort_by: str = "runs", limit: int = 10) -> pd.DataFrame:
        """Returns top batsmen sorted by selected metric."""
        if sort_by not in self.batting_df.columns:
            sort_by = "runs"
        return self.batting_df.sort_values(by=sort_by, ascending=False).head(limit).reset_index(drop=True)

    def get_top_bowlers(self, sort_by: str = "wickets", limit: int = 10) -> pd.DataFrame:
        """Returns top bowlers sorted by selected metric."""
        if sort_by not in self.bowling_df.columns:
            sort_by = "wickets"
        ascending = sort_by in ["economy", "average", "strike_rate"]
        return self.bowling_df.sort_values(by=sort_by, ascending=ascending).head(limit).reset_index(drop=True)
