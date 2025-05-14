import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import helper
import preprocessor
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df,region_df)


st.sidebar.title("OLYMPICS Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Tally')

    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title('Medal Tally in ' + str(selected_year)+' Olympics')

    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title('Medal Tally of '+str(selected_country) + 'Olympics')
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title('Medal Tally of '+selected_country+ ' in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)


if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    total_hosts = df['City'].unique().shape[0]
    total_sports = df['Sport'].unique().shape[0]
    total_events = df['Event'].unique().shape[0]
    participants_country = df['region'].unique().shape[0]
    total_athletes = df['Name'].unique().shape[0]

    st.title('Total Statistics')

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Total Hosts")
        st.title(total_hosts)

    with col3:
        st.header("Total Sports")
        st.title(total_sports)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Total Events")
        st.title(total_events)

    with col2:
        st.header("Nations")
        st.title(participants_country)

    with col3:
        st.header("Total Athletes")
        st.title(total_athletes)

    st.header("Participants Over the Year")

    nation_counts = helper.nations_over_time(df)

    # Plotly chart

    fig = px.line(nation_counts,
                  x='Year',
                  y='Number of Nations',
                  markers=True)

    fig.update_layout(xaxis_title='Year',
                      yaxis_title='Number of Nations',
                      template='plotly_white',
                      hovermode='x unified')

    st.plotly_chart(fig)


    event_counts = helper.events_counts(df)


    st.header("Number of Events Over the Year")
    fig2 = px.line(event_counts,
                   x='Year',
                   y='Number of Events',
                   markers=True,
                   title='Number of Unique Olympic Events Over the Years')

    fig2.update_layout(xaxis_title='Year',
                       yaxis_title='Number of Events',
                       template='plotly_white',
                       hovermode='x unified')

    st.plotly_chart(fig2)

    # Remove duplicates to count each athlete once per year
    athletes_df = df.drop_duplicates(subset=['Year', 'Name'])

    # Group by year and count unique athlete names
    athlete_counts = athletes_df.groupby('Year')['Name'].nunique().reset_index()
    athlete_counts.rename(columns={'Name': 'Number of Athletes'}, inplace=True)

    fig3 = px.line(athlete_counts,
                   x='Year',
                   y='Number of Athletes',
                   markers=True,
                   title='Number of Athletes Participating Over the Years')

    fig3.update_layout(xaxis_title='Year',
                       yaxis_title='Number of Athletes',
                       template='plotly_white',
                       hovermode='x unified')

    st.plotly_chart(fig3)

    gender_df = df.drop_duplicates(subset=['Year', 'Name'])

    # Group by Year and Sex
    gender_counts = gender_df.groupby(['Year', 'Sex'])['Name'].count().reset_index()
    gender_counts.rename(columns={'Name': 'Count'}, inplace=True)

    # Plotly line chart with two lines (M and F)
    fig4 = px.line(gender_counts,
                   x='Year',
                   y='Count',
                   color='Sex',
                   markers=True,
                   title='Male vs Female Athlete Participation Over the Years')

    fig4.update_layout(xaxis_title='Year',
                       yaxis_title='Number of Athletes',
                       template='plotly_white',
                       hovermode='x unified')

    st.plotly_chart(fig4)

    st.header("No Of Events Over time(Every Sports)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])

    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)


    st.header("Most Successful Athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select Sport',sport_list)

    x = helper.most_sucessful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country_wise Medal Tally')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_counties = st.sidebar.selectbox('Select Country' , country_list)

    year_medal_df = helper.yearwise_medal_tally(df,selected_counties)

    fig5 = px.line(year_medal_df,
                   x='Year',
                   y='Medal',
                   )
    st.header(selected_counties + ' Medal Tally over the year')
    st.plotly_chart(fig5)

    st.header("Country wise analysis")
    pt = helper.country_wise_heatmap(df,selected_counties)
    fig,ax = plt.subplots(figsize= (30,30))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)


    st.header("Most Successful Players of " + selected_counties)
    temp_df = helper.most_sucessful_country_wise(df,selected_counties)
    st.table(temp_df)



if user_menu == 'Athlete-wise Analysis':
    st.header("Distribution of Age Over Medals")

    bins = np.arange(10, 60, 1)  # Age range from 10 to 60
    x1 = df['Age'].dropna()
    x2 = df[df['Medal'] == 'Gold']['Age'].dropna()
    x4 = df[df['Medal'] == 'Bronze']['Age'].dropna()
    x3 = df[df['Medal'] == 'Silver']['Age'].dropna()
    # Compute histograms
    hist_all, _ = np.histogram(x1, bins=bins, density=True)
    hist_gold, _ = np.histogram(x2, bins=bins, density=True)
    hist_silver, _ = np.histogram(x3, bins=bins, density=True)
    hist_bronze, _ = np.histogram(x4, bins=bins, density=True)

    # Compute bin centers for plotting
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Create line plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=bin_centers, y=hist_all, mode='lines', name='All Athletes'))
    fig.add_trace(go.Scatter(x=bin_centers, y=hist_gold, mode='lines', name='Gold Medalists'))
    fig.add_trace(go.Scatter(x=bin_centers, y=hist_silver, mode='lines', name='Silver Medalists'))
    fig.add_trace(go.Scatter(x=bin_centers, y=hist_bronze, mode='lines', name='Bronze Medalists'))

    fig.update_layout(
        title='Age Distribution of Athletes and Medalists',
        xaxis_title='Age',
        yaxis_title='Density',
        template='plotly_white'
    )

    st.plotly_chart(fig)



    st.header("Distribution of Age Over different Sport")
    # Create an empty figure
    fig = go.Figure()
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
                     'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
                     'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
                     'Alpinism', 'Aeronautics']
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        # Plot only if we have at least 2 values
        if len(gold_ages) > 2:
            # Get histogram bins
            counts, bins = np.histogram(gold_ages, bins=range(10, 60, 2))  # age range: 10 to 60
            bin_centers = 0.5 * (bins[1:] + bins[:-1])

            # Add as line plot
            fig.add_trace(go.Scatter(x=bin_centers, y=counts, mode='lines', name=sport))

    fig.update_layout(
        title='Age Distribution (Histogram-based Line) of Gold Medalists by Sport',
        xaxis_title='Age',
        yaxis_title='Count',
        template='plotly_white',
        height=600
    )
    st.plotly_chart(fig)





    st.header("Height and Weight For Particular Sport")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()

    selected_sport = st.selectbox('Select Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)

    fig,ax = plt.subplots(figsize = (15,10))
    ax =sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],hue = temp_df['Medal'],style = temp_df['Sex'],s = 100)

    st.pyplot(fig)