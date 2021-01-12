import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")
st.title('⚽️ Fantasy Premier League Explorer')
"""
## By Milan Patty
In this project I'm going to show you my interactive web application about the Fantasy Premier League(FPL) and how it gives user usefull insights about the best players and teams.
"""

# DT
df = pd.read_csv('merged_gw10.csv')

# Sidebar --------------------------------------------------------------------------------------------
st.sidebar.header('Filter data')

# Sidebar -  Gameweek Selection
selected_gw = st.sidebar.selectbox('Gameweek', list(range(1,18)))

# Sidebar - Team selection
sorted_unique_team = sorted(df['team'].unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
sorted_unique_pos = sorted(df['position'].unique())
selected_pos = st.sidebar.multiselect('Position', sorted_unique_pos, sorted_unique_pos)

# Sidebar - Player cost
min_selection, max_selection = st.sidebar.slider(
    "Player cost", min_value=30, max_value=130, value=[30, 130]
)

# Sidebar - Feature Selection
st.sidebar.subheader('Players with the most points')
show_players_wmp = st.sidebar.checkbox("Show graph 1")

st.sidebar.subheader('Players with the highest avg points per game')
show_players_avgp = st.sidebar.checkbox("Show graph 2")

st.sidebar.subheader('Team overview with the highest value')
show_teams_value = st.sidebar.checkbox("Show graph 3")

st.sidebar.subheader('Player overview: value vs total points')
player_value = st.sidebar.checkbox("Show graph 4")

# ----------------------------------------------------------------------------------------------------
# Filtering data
df_selected_team = df[ (df['value'] >= min_selection) &
    (df['value'] <= max_selection) &
    (df['team'].isin(selected_team)) &
    (df['position'].isin(selected_pos))]

st.subheader('The Fantasy Premier League Data:')
st.write('You selected GW', selected_gw)
st.dataframe(df_selected_team, width=2500, height=800)

# ----------------------------------------------------------------------------------------------------------
# Creating new subsets
new_df = df[['name','goals_scored', 'assists', 'minutes', 'yellow_cards','red_cards', 'clean_sheets', 'total_points']]
avg_points = new_df.groupby('name').sum()
avg_points['AVG_PPP'] = avg_points['total_points'] / max(df['GW'])
players_mp = avg_points.sort_values('total_points', ascending=False)

players_mp.reset_index(inplace=True)

# New Copy for visual
players_with_most_points = players_mp.copy()[:30].sort_values('total_points', ascending=False)

# Sorting the values
players_mp.sort_values('AVG_PPP', inplace=True, ascending=False)
players_mp = players_mp[:25]
players_mp.sort_values('AVG_PPP', inplace=True, ascending=True)
#st.subheader('Players with the most average points per gameweek')
#st.write(players_mp[:25])


# Latest GW
#latest_gw = df[df['GW'] == max(df['GW'])]
latest_gw = df[['name','goals_scored', 'assists', 'minutes', 'yellow_cards','red_cards', 'clean_sheets', 'total_points']]
pwmp = latest_gw.groupby('name').sum()
pwmp.reset_index(inplace=True)
pwmp.sort_values('total_points', inplace=True, ascending=False)
pwmp = pwmp[:25]
pwmp.sort_values('total_points', inplace=True, ascending=True)


teams = df[['team', 'total_points', 'value']]
teams_wmp = teams.groupby('team').sum()
teams_wmp.reset_index(inplace=True)

# Boxplot
box_plot = df[df['GW'] == max(df['GW'])]
box_plot.sort_values('team',ascending=True,inplace=True)

# Totalpoints vs player value
pvsv = df[['name', 'team', 'total_points', 'value']]
pvsv = pvsv.groupby(['name', 'team']).sum()
pvsv.reset_index(inplace=True)
pvsv.sort_values('team', inplace=True)

# Checkboxes ---------------------------------------------------------------------------------------------------------
if show_players_wmp:
    # Plot for players with the most points
    fig = px.bar(pwmp, x="total_points", y="name", title='Top 25 players with the most points')
    fig.update_traces(marker_color='#F63465')
    fig.update_layout(
        autosize=False,
        width=1500,
        height=800)
    st.plotly_chart(fig)

if show_players_avgp:
    fig2 = px.bar(players_mp, x="AVG_PPP", y="name", title='Top 25 players with the highest AVG points per game')
    fig2.update_traces(marker_color='#F63465')
    fig2.update_layout(
        autosize=False,
        width=1500,
        height=800)
    st.plotly_chart(fig2)

if show_teams_value:
    fig3 = px.box(box_plot,x='team', y="value", color="team",
             boxmode="overlay", points='all', title='Teams value overview with the latest gameweek data:')
    fig3.update_layout(
        autosize=False,
        width=1500,
        height=800)
    st.plotly_chart(fig3)

if player_value:
    fig4 = px.scatter(pvsv, x="value", y="total_points", color='team',text="name",log_x=False, title='Players: total points vs value')
    fig4.update_layout(
        autosize=False,
        width=1500,
        height=800)
    st.plotly_chart(fig4)