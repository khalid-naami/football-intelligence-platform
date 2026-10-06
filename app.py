"""Global Football Intelligence, League Analytics & Match Prediction Platform.

Covers Top 20 Global Leagues, Indian Super League (ISL), UEFA Champions League,
FIFA World Cup 2026, Continental Cups, Live Scores, Golden Boot, and H2H Match Predictor.
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.leagues_database import LeaguesManager, LEAGUES_DATABASE
from src.matches_engine import MatchesEngine
from src.players_stats import PlayersStatsManager
from src.h2h_predictor_engine import H2HPredictorEngine
from src.visualizer import (
    create_player_radar_chart,
    create_match_prediction_donut,
    create_standings_goal_diff_bar
)

# Page Setup
st.set_page_config(
    page_title="Global Football Intelligence & League Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sports Glassmorphism Dark CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981, #38bdf8, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #34d399;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #38bdf8;
    }
    .match-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.3rem;
        margin-bottom: 1.1rem;
    }
    .live-dot {
        height: 10px;
        width: 10px;
        background-color: #ef4444;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    .h2h-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 1.4rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.markdown("## ⚽ Competition Selector")
all_leagues = LeaguesManager.get_all_league_names()
chosen_league = st.sidebar.selectbox("Select League / Tournament:", all_leagues, index=0)
league_info = LeaguesManager.get_league_data(chosen_league)

# 10s Live Auto-Refresh
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Live Telemetry & Auto-Refresh")
auto_refresh_enabled = st.sidebar.toggle("10s Auto-Refresh (Live Matchday Sync)", value=True)
refresh_counter = 0
if auto_refresh_enabled:
    refresh_counter = st_autorefresh(interval=10000, limit=None, key="football_auto_refresh_10s")

if st.sidebar.button("🔄 Refresh Live Matchday Feed", key="btn_refresh_matches"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### 🏆 Tournament Metadata:
- **Confederation:** `{league_info['confederation']}`
- **Classification:** `{league_info['type']}`
- **Market Value:** `{league_info['market_value']}`
- **Defending Champion:** `{league_info['defending_champion']}`
- **Historical Giant:** `{league_info['most_successful']}`
""")

# Main Header
st.markdown('<div class="main-title">⚽ Global Football Intelligence & League Analytics Platform</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Top 20 Worldwide Leagues | Indian Super League (ISL) | UEFA Champions League | FIFA World Cup 2026 | Real-Time xG & H2H Engine — <b>{chosen_league}</b></div>', unsafe_allow_html=True)

# Live Status Badge
now_utc_str = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
if auto_refresh_enabled:
    st.markdown(f'<div class="live-badge">🟢 LIVE MATCHDAY TELEMETRY ACTIVE &bull; Auto-Refreshing every 10s &bull; Last Synced: {now_utc_str} &bull; Cycle #{refresh_counter}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="live-badge" style="background:rgba(148,163,184,0.1); border-color:rgba(148,163,184,0.3); color:#94a3b8;">⏸️ LIVE SYNC PAUSED &bull; Last Synced: {now_utc_str}</div>', unsafe_allow_html=True)

# Top KPI Metric Cards (5 Highlights)
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Competition</div>
        <div class="metric-value">{league_info['id']}</div>
        <div class="metric-sub">{league_info['country']}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Market Value</div>
        <div class="metric-value">💰 {league_info['market_value'].split()[0]}</div>
        <div class="metric-sub">{league_info['market_value'].split()[-1]}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Clubs / Squads</div>
        <div class="metric-value">🛡️ {league_info['teams_count']}</div>
        <div class="metric-sub">Participating Teams</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Goal Rate</div>
        <div class="metric-value">⚽ {league_info['avg_goals_per_game']}</div>
        <div class="metric-sub">Goals / Match Average</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Title Holder</div>
        <div class="metric-value">👑 {league_info['defending_champion'].split()[0]}</div>
        <div class="metric-sub">{league_info['defending_champion'][:18]}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs (5 Modules)
tabs = st.tabs([
    "🏆 Standings & Form Guide",
    "⚡ Live Match Center & Scores",
    "👟 Golden Boot & Playmakers",
    "🎯 H2H Match Predictor Engine",
    "🌟 Elite Player Radar Profiles"
])

# ----------------- TAB 1: Standings -----------------
with tabs[0]:
    st.markdown(f"### 🏆 Official Table & Standings — {chosen_league}")
    df_standings = LeaguesManager.get_standings_df(chosen_league)

    if not df_standings.empty:
        st.dataframe(df_standings.rename(columns={
            "rank": "Rank",
            "team": "Club / National Team",
            "p": "MP",
            "w": "W",
            "d": "D",
            "l": "L",
            "gf": "GF",
            "ga": "GA",
            "gd": "GD",
            "pts": "Points",
            "form": "Recent Form",
            "status": "Qualification / Status"
        }), use_container_width=True, hide_index=True)

        st.markdown("---")
        fig_gd = create_standings_goal_diff_bar(df_standings, chosen_league)
        st.plotly_chart(fig_gd, use_container_width=True)

# ----------------- TAB 2: Live Match Center -----------------
with tabs[1]:
    st.markdown(f"### ⚡ Real-Time Live Match Center & Matchday Telemetry — {chosen_league}")
    
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        match_filter = st.radio(
            "Filter Fixtures:",
            ["All Fixtures", "🔴 Live Matches", "🟢 Finished (FT)", "🕒 Upcoming Matches"],
            horizontal=True,
            key="match_status_filter"
        )
    with col_f2:
        st.markdown(f"<div style='text-align:right; font-size:0.85rem; color:#34d399; padding-top:14px;'>🟢 <b>10s Live Sync Active</b> (Cycle #{refresh_counter})</div>", unsafe_allow_html=True)

    matches_list = MatchesEngine.get_league_matches(chosen_league)

    if match_filter == "🔴 Live Matches":
        displayed_matches = [m for m in matches_list if m.get("status") == "LIVE"]
    elif match_filter == "🟢 Finished (FT)":
        displayed_matches = [m for m in matches_list if m.get("status") == "FT"]
    elif match_filter == "🕒 Upcoming Matches":
        displayed_matches = [m for m in matches_list if m.get("status") == "UPCOMING"]
    else:
        displayed_matches = matches_list

    if not displayed_matches:
        st.info(f"No matches currently matching the '{match_filter}' filter in {chosen_league}. Switch to 'All Fixtures' to view the complete schedule.")
    else:
        for m in displayed_matches:
            is_live = m["status"] == "LIVE"
            if is_live:
                status_badge = f'<span style="background:#ef4444; color:white; padding:4px 10px; border-radius:6px; font-weight:800; font-size:0.85rem;"><span class="live-dot"></span>LIVE {m["minute"]}</span>'
            elif m["status"] == "FT":
                status_badge = '<span style="background:#10b981; color:white; padding:4px 10px; border-radius:6px; font-weight:700; font-size:0.85rem;">🟢 FULL TIME</span>'
            else:
                status_badge = f'<span style="background:#334155; color:#94a3b8; padding:4px 10px; border-radius:6px; font-weight:600; font-size:0.85rem;">🕒 {m["minute"]}</span>'

            home_logo_html = f'<img src="{m.get("home_logo", "")}" style="width:44px; height:44px; object-fit:contain; margin-right:10px;" referrerpolicy="no-referrer" onerror="this.style.display=\'none\';"/>' if m.get("home_logo") else ''
            away_logo_html = f'<img src="{m.get("away_logo", "")}" style="width:44px; height:44px; object-fit:contain; margin-left:10px;" referrerpolicy="no-referrer" onerror="this.style.display=\'none\';"/>' if m.get("away_logo") else ''

            events_html = ""
            if m.get("events"):
                events_html = f"<div style='font-size:0.85rem; color:#cbd5e1; border-top:1px solid rgba(148,163,184,0.15); margin-top:0.9rem; padding-top:0.7rem;'><b>⚽ Match Timeline & Events:</b> " + ' &bull; '.join(m['events']) + "</div>"

            card_html = (
                f'<div class="match-card">'
                f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.9rem; border-bottom:1px solid rgba(148,163,184,0.12); padding-bottom:0.6rem;">'
                f'<span style="color:#94a3b8; font-size:0.85rem;">🏟️ {m.get("stadium", "Main Stadium")} | 👨‍⚖️ {m.get("referee", "FIFA Elite")}</span>'
                f'{status_badge}'
                f'</div>'
                f'<div style="display:flex; justify-content:space-between; align-items:center; text-align:center;">'
                f'<div style="width:38%; display:flex; align-items:center; justify-content:flex-end;">'
                f'<div style="text-align:right;">'
                f'<h3 style="margin:0; color:#f8fafc; font-size:1.3rem;">{m["home_team"]}</h3>'
                f'<span style="color:#38bdf8; font-size:0.85rem;">xG: {m.get("xg_home", 0.0)} &bull; Poss: {m.get("possession_home", 50)}%</span>'
                f'</div>'
                f'{home_logo_html}'
                f'</div>'
                f'<div style="width:24%; text-align:center;">'
                f'<div style="font-size:2.4rem; font-weight:900; color:#f59e0b; letter-spacing:2px; line-height:1;">{m["score_home"]} - {m["score_away"]}</div>'
                f'<div style="display:flex; height:5px; border-radius:3px; overflow:hidden; margin:8px auto 0; width:120px; background:#334155;">'
                f'<div style="width:{m.get("possession_home", 50)}%; background:#38bdf8;"></div>'
                f'<div style="width:{m.get("possession_away", 50)}%; background:#f59e0b;"></div>'
                f'</div>'
                f'</div>'
                f'<div style="width:38%; display:flex; align-items:center; justify-content:flex-start;">'
                f'{away_logo_html}'
                f'<div style="text-align:left;">'
                f'<h3 style="margin:0; color:#f8fafc; font-size:1.3rem;">{m["away_team"]}</h3>'
                f'<span style="color:#f59e0b; font-size:0.85rem;">Poss: {m.get("possession_away", 50)}% &bull; xG: {m.get("xg_away", 0.0)}</span>'
                f'</div>'
                f'</div>'
                f'</div>'
                f'{events_html}'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

# ----------------- TAB 3: Golden Boot & Playmakers -----------------
with tabs[2]:
    st.markdown(f"### 👟 Golden Boot & Playmaker Rankings — {chosen_league}")
    
    col_gb1, col_gb2 = st.columns(2)
    with col_gb1:
        st.markdown("#### ⚽ Top Goalscorers (Golden Boot)")
        df_scorers = PlayersStatsManager.get_top_scorers_df(chosen_league)
        if not df_scorers.empty:
            st.dataframe(df_scorers.rename(columns={
                "rank": "Rank",
                "player": "Player",
                "team": "Club",
                "goals": "Goals ⚽",
                "pens": "Pens",
                "matches": "MP",
                "xg": "xG",
                "mins_per_goal": "Mins / Goal"
            }), use_container_width=True, hide_index=True)

    with col_gb2:
        st.markdown("#### 🪄 Top Playmakers (Assists & Key Passes)")
        df_assists = PlayersStatsManager.get_top_assists_df(chosen_league)
        if not df_assists.empty:
            st.dataframe(df_assists.rename(columns={
                "rank": "Rank",
                "player": "Player",
                "team": "Club",
                "assists": "Assists 🪄",
                "key_passes": "Key Passes",
                "big_chances_created": "Big Chances"
            }), use_container_width=True, hide_index=True)

# ----------------- TAB 4: H2H Match Predictor -----------------
with tabs[3]:
    st.markdown("### 🎯 Head-to-Head (H2H) & Match Probability Predictor")
    st.markdown("Simulate any matchup using bivariate Poisson Expected Goals (xG) distribution modeling.")

    df_current_teams = LeaguesManager.get_standings_df(chosen_league)
    team_names = df_current_teams["team"].tolist() if not df_current_teams.empty else ["Arsenal", "Manchester City", "Real Madrid", "FC Barcelona", "Mohun Bagan Super Giant", "Mumbai City FC"]

    p_c1, p_c2 = st.columns(2)
    with p_c1:
        selected_home = st.selectbox("Select Home Team:", team_names, index=0)
    with p_c2:
        selected_away = st.selectbox("Select Away Team:", team_names, index=min(1, len(team_names)-1))

    odds_data = H2HPredictorEngine.calculate_match_odds(selected_home, selected_away)

    h_col1, h_col2 = st.columns([1, 1.2])
    with h_col1:
        fig_donut = create_match_prediction_donut(
            selected_home,
            selected_away,
            odds_data["home_win_prob"],
            odds_data["draw_prob"],
            odds_data["away_win_prob"]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with h_col2:
        st.markdown(f"""
        <div class="h2h-card">
            <h4>📊 Match Statistical Prognosis:</h4>
            - <b>Projected Expected Goals (xG):</b> <code>{selected_home} {odds_data['home_xg']} - {odds_data['away_xg']} {selected_away}</code><br>
            - <b>Over 2.5 Goals Probability:</b> <b>{odds_data['over_2_5_prob']}%</b><br>
            - <b>Both Teams to Score (BTTS):</b> <b>{odds_data['btts_prob']}%</b><br>
            <hr style="border-color: rgba(245, 158, 11, 0.2);">
            <h4>🎲 Most Probable Correct Scorelines:</h4>
        """, unsafe_allow_html=True)
        
        for sc in odds_data["top_scorelines"]:
            st.markdown(f"- **Scoreline `{sc['score']}`**: **{sc['prob']}%** calculated likelihood")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 5: Elite Player Radar Profiles -----------------
with tabs[4]:
    st.markdown("### 🌟 Elite Player Performance Radar & Technical Attributes")
    st.markdown("Interactive 6-axis performance comparison evaluating Pace, Shooting, Passing, Dribbling, Defending, and Physicality.")

    radar_players = PlayersStatsManager.get_radar_players()
    chosen_player = st.selectbox("Select Featured World-Class Player:", radar_players, index=0)

    p_metrics = PlayersStatsManager.get_player_radar_metrics(chosen_player)
    
    r_c1, r_c2 = st.columns([1.2, 1])
    with r_c1:
        fig_radar = create_player_radar_chart(chosen_player, p_metrics)
        st.plotly_chart(fig_radar, use_container_width=True)

    with r_c2:
        st.markdown(f"#### 📋 Technical Evaluation: {chosen_player}")
        for attr, score in p_metrics.items():
            st.progress(score / 100.0, text=f"{attr}: {score} / 100")
