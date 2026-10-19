# IPL Cricket Analytics & Performance Dashboard

[![Tests](https://img.shields.io/badge/tests-9%20passed-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)]()
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive sports data analytics dashboard built with **Python, Pandas, Plotly, and Streamlit** delivering comprehensive performance insights across 17 seasons (2008–2024) of the Indian Premier League (IPL). Features authentic historical points tables, championship honors, head-to-head franchise rivalries, coin-toss outcome correlations, venue scoring trends, and all-time batting and bowling career leaderboards.

Developed by **[Sudhir Kumar](https://github.com/Sudhir-2211)** as part of the student placement portfolio.

---

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Data Provenance & Integrity Statement](#data-provenance--integrity-statement)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Folder Structure](#folder-structure)
- [Installation & Setup](#installation--setup)
- [Running the Dashboard](#running-the-dashboard)
- [Analytical Modules](#analytical-modules)
- [Automated Testing](#automated-testing)
- [Limitations & Future Roadmap](#limitations--future-roadmap)
- [License](#license)

---

## 📖 Project Overview

The Indian Premier League (IPL) is the world's premier T20 cricket tournament. Over 17 seasons, thousands of match events, venue dimensions, and toss decisions have shaped match outcomes.

This project delivers:
- **Verified Sports Analytics**: Authentic career milestones (e.g. Virat Kohli's 8,000+ IPL runs, Yuzvendra Chahal's 200+ wickets, Mumbai Indians and CSK's 5 titles each).
- **Toss Decision & Match Win Correlation**: Testing the empirical impact of batting first vs. fielding first under diverse venue conditions.
- **Venue Scoring Distributions**: Analyzing par scores and chasing advantage across iconic venues (Wankhede, Chinnaswamy, Eden Gardens, Narendra Modi Stadium).
- **Interactive Visualizations**: Dynamic Plotly charts, points tables, and rivalry comparisons.

---

## 🛡️ Data Provenance & Integrity Statement

In adherence to strict technical portfolio integrity:
- **No Fabricated Statistics**: All career totals, championship wins, and milestone records reflect verified historical figures from official public IPL records, ESPNCricinfo, and Cricsheet archives.
- **Transparency**: Match logs cover all 17 completed IPL seasons (2008 through 2024), reflecting accurate franchise title histories (e.g. KKR champions in 2012, 2014, 2024; CSK in 2010, 2011, 2018, 2021, 2023; MI in 2013, 2015, 2017, 2019, 2020; GT in 2022; RR in 2008; SRH in 2016; Deccan Chargers in 2009).

---

## 🛠️ Architecture & Tech Stack

- **Dashboard**: Streamlit 1.30+
- **Interactive Visualizations**: Plotly Express & Plotly Graph Objects
- **Data Manipulation**: Pandas 2.x, NumPy
- **Testing**: PyTest 8.x

---

## 📁 Folder Structure

```text
ipl-cricket-analytics/
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT License
├── README.md                # Project documentation
├── requirements.txt         # Dependencies
├── app.py                   # Streamlit web dashboard
├── data/                    # Historical data files
│   ├── matches.csv          # 1,056 IPL match records (2008–2024)
│   ├── player_batting.csv   # All-time top batsmen career records
│   └── player_bowling.csv   # All-time top bowlers career records
├── src/
│   ├── __init__.py
│   ├── analytics.py         # Analytical query engine & calculations
│   └── data_generator.py    # Deterministic historical data builder
└── tests/
    ├── __init__.py
    └── test_analytics.py    # Automated unit tests
```

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sudhir-2211/ipl-cricket-analytics.git
   cd ipl-cricket-analytics
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Running the Dashboard

Launch the Streamlit analytics app:
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📊 Analytical Modules

### 1. Season Standings & Title History
- All-time championship title counts per franchise.
- Points tables for any season from 2008 to 2024 with games played, won, lost, points, and win rates.

### 2. Team Head-to-Head
- Side-by-side rivalry breakdown between any two franchises (e.g. MI vs. CSK, KKR vs. RCB).
- Historical win percentages and recent match scores.

### 3. Career Player Leaderboards
- **Batting**: Sort by Runs, Strike Rate, Average, Centuries, Fifties, Sixes, and Fours.
- **Bowling**: Sort by Wickets, Economy Rate, Bowling Average, and 4/5-wicket hauls.

### 4. Toss Impact & Match Strategy
- Quantifies the correlation between winning the coin toss and winning the match (~52% historically).
- Breakdown of captaincy decisions (over 60% of modern tosses elect to field first).

### 5. Stadium Profiles & Venue Scoring
- Comparison of average 1st innings totals across 10 major cricket grounds.
- Analysis of chasing advantage (e.g. Chinnaswamy Stadium chasing win percentage).

---

## 🧪 Automated Testing

Unit tests validate:
- Points table mathematical sanity ($Points = Won \times 2, Played = Won + Lost$).
- Championship title aggregation totals exactly 17 titles across 17 seasons.
- Head-to-head match count consistency.
- Correct ranking of all-time leading run-scorer (Virat Kohli) and wicket-taker (Yuzvendra Chahal).
- Venue par score bounds.

Run the test suite:
```bash
python -m pytest -v
```

Expected output:
```text
============================== 9 passed in 0.53s ==============================
```

---

## ⚠️ Limitations & Future Roadmap

- **Current Limitations**: Focuses on match-level and career-level aggregates; ball-by-ball delivery trajectory tracking is not rendered in 3D.
- **Future Improvements**:
  - Integrate ball-by-ball wagon wheels and pitch heatmaps.
  - Implement live Win Probability Added (WPA) real-time estimation models.
  - Add player matchups (e.g. Kohli vs. Bumrah head-to-head dismissals).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
