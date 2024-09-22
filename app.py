import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('ipl1.csv', low_memory=False, index_col=False)
st.set_page_config(layout='wide', page_title='IPL Analysis')
st.title('IPL Analysis by Milan Kulshrestha')

df1 = df[df['extras_type'] != 'wides']
temp_df = df1.groupby(['batter', 'season']).agg({
    'batsman_runs': 'sum',
    'is_wicket': 'sum',
    'ball': 'count'
}).reset_index()


temp_df['Average'] = temp_df['batsman_runs'] / temp_df['is_wicket']
temp_df['Strike_Rate'] = (temp_df['batsman_runs'] / temp_df['ball']) * 100

# Filter for bowler data
df2 = df[~df['extras_type'].isin(['legbyes', 'byes'])]
df2 = df[~df['dismissal_kind'].isin(['run out', 'retired hurt', 'retired out'])]

bowler_df = df2.groupby(['bowler', 'season']).agg({
    'total_runs': 'sum',
    'is_wicket': 'sum',
    'ball': 'count'
}).reset_index()


bowler_df['Average'] = bowler_df['total_runs'] / (bowler_df['ball'] / 6)
bowler_df['Strike_Rate'] = bowler_df['ball'] / bowler_df['is_wicket']

def analyse_batter(batter):
    total_runs = df[df['batter'] == batter]['batsman_runs'].sum()
    total_dismissal = df[df['batter'] == batter]['is_wicket'].sum()
    average = round(temp_df[temp_df['batter'] == batter]['batsman_runs'].sum() / temp_df[temp_df['batter'] == batter]['is_wicket'].sum(), 2)
    strike_rate = round((temp_df[temp_df['batter'] == batter]['batsman_runs'].sum() / temp_df[temp_df['batter'] == batter]['ball'].sum()) * 100, 2)
    season = temp_df[temp_df['batter'] == batter].shape[0]


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric('Total Runs', total_runs)
    with col2:
        st.metric('Total Dismissals', total_dismissal)
    with col3:
        st.metric('Average', average)
    with col4:
        st.metric('Strike Rate', strike_rate)
    with col5:
        st.metric('No. of Seasons Played', season)

    # Display the data and bar chart for the batter
    batter_data = temp_df[temp_df['batter'] == batter].reset_index(drop=True)
    st.write(f"Analysis for batter: {batter}")
    st.write(batter_data)

    fig = px.bar(batter_data, x='season', y='batsman_runs', color='season', title=f"{batter} Runs Analysis")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(batter_data, x='Strike Rate', y='Average', color='season', title=f"{batter} Runs Analysis")
    st.plotly_chart(fig, use_container_width=True)


def analyse_bowler(bowler):
    total_wickets = df[df['bowler'] == bowler]['is_wicket'].sum()
    total_runs = df[df['bowler'] == bowler]['total_runs'].sum()
    average = round(bowler_df[bowler_df['bowler'] == bowler]['total_runs'].sum() / (bowler_df[bowler_df['bowler'] == bowler]['ball'] / 6).sum(), 2)
    strike_rate = round(bowler_df[bowler_df['bowler'] == bowler]['ball'].sum() / bowler_df[bowler_df['bowler'] == bowler]['is_wicket'].sum(), 2)
    season = bowler_df[bowler_df['bowler'] == bowler].shape[0]


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric('Total Wickets', total_wickets)
    with col2:
        st.metric('Total Runs', total_runs)
    with col3:
        st.metric('Average', average)
    with col4:
        st.metric('Strike Rate', strike_rate)
    with col5:
        st.metric('No. of Seasons Played', season)


    bowler_data = bowler_df[bowler_df['bowler'] == bowler].reset_index(drop=True)
    st.write(f"Analysis for bowler: {bowler}")
    st.write(bowler_data)

    fig = px.bar(bowler_data, x='season', y='is_wicket', color='season', title=f"{bowler} Wicket Analysis")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(bowler_data, x='Strike_Rate', y='Average', color='season', title=f"{bowler} performance Analysis")
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.title('IPL Analysis')

options = st.sidebar.selectbox('Select One', ['Batsman', 'Bowler'])

if options == 'Batsman':
    bat = st.sidebar.selectbox('Select Batsman', sorted(df['batter'].unique().tolist()))
    btn1 = st.sidebar.button('Find Batsman Details')
    if btn1:
        st.title('Batsman Analysis')
        analyse_batter(bat)

elif options == 'Bowler':
    bowl = st.sidebar.selectbox('Select Bowler', sorted(df['bowler'].unique().tolist()))
    btn2 = st.sidebar.button('Find Bowler Details')
    if btn2:
        st.title('Bowler Analysis')
        analyse_bowler(bowl)
