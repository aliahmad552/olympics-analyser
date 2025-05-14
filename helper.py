
import numpy as np



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country



def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def nations_over_time(df):
    # Remove duplicate (Year, region)
    unique_nations_df = df.drop_duplicates(subset=['Year', 'region'])

    # Group and count
    nation_counts = unique_nations_df.groupby('Year')['region'].nunique().reset_index()
    nation_counts.rename(columns={'region': 'Number of Nations'}, inplace=True)

    return nation_counts

def events_counts(df):
    # Remove duplicates so we only count each event once per year
    events_df = df.drop_duplicates(subset=['Year', 'Event'])

    # Group by year and count unique events
    event_counts = events_df.groupby('Year')['Event'].nunique().reset_index()
    event_counts.rename(columns={'Event': 'Number of Events'}, inplace=True)
    return event_counts

def most_sucessful(df,sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x =  temp_df['Name'].value_counts().reset_index().head(14).merge(df,on = 'Name',how ='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medal'},inplace =True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_wise_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    x = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return x


def most_sucessful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medal'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df