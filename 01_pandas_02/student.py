import pandas as pd
import json

"""
    ASSIGNMENT 1 (STUDENT VERSION):
    Using pandas to explore youtube trending data from GB (GBvideos.csv and GB_category_id.json) and answer the questions.
"""

def Q1():
    """
    1. How many rows are there in the GBvideos.csv after removing duplications?
    """
    vdo_df = pd.read_csv('/data/GBvideos.csv')
    vdo_df = vdo_df.drop_duplicates()
    num_rows = vdo_df.shape[0]  
    return num_rows

def Q2(vdo_df):
    '''
    2. How many videos have "dislikes" more than "likes"? Make sure that you count only unique titles!
    '''
    filter_likes = vdo_df.dislikes > vdo_df.likes
    vdo_df_filtered = vdo_df[filter_likes]

    unique_titles = vdo_df_filtered.drop_duplicates(subset='title')
    
    num_unique_titles = unique_titles.shape[0]
    
    return num_unique_titles

def Q3(vdo_df):
    '''
        3. How many VDO that are trending on 22 Jan 2018 with comments more than 10,000 comments?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - The trending date of vdo_df is represented as 'YY.DD.MM'. For example, January 22, 2018, is represented as '18.22.01'.
    '''
    from datetime import datetime, timezone
    vdo_df['trending_dt'] = pd.to_datetime(vdo_df['trending_date'], format='%y.%d.%m', errors='coerce', utc=True)

    filter_date = datetime(2018, 1, 22, tzinfo=timezone.utc)

    vdo_df_title_date_comments = vdo_df[(vdo_df['trending_dt'] == filter_date) & (vdo_df['comment_count'] > 10000)][['title', 'trending_dt', 'comment_count']]

    description = vdo_df_title_date_comments['comment_count'].describe()
    count_value = description['count']

    return int(count_value)

def Q4(vdo_df):
    '''
        4. Which trending date that has the minimum average number of comments per VDO?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # Convert 'trending_date' to datetime format
    vdo_df['trending_dt'] = pd.to_datetime(vdo_df['trending_date'], format='%y.%d.%m', errors='coerce', utc=True)

    vdo_groupby_date = vdo_df.groupby('trending_dt')['comment_count'].mean().reset_index()

    vdo_groupby_date_df = vdo_groupby_date.sort_values(by='comment_count')

    min_date = vdo_groupby_date_df.iloc[0]['trending_dt']

    formatted_date = min_date.strftime('%y.%d.%m')

    return (formatted_date)

def Q5(vdo_df):
    '''
        5. Compare "Sports" and "Comedy", how many days that there are more total daily views of VDO in "Sports" category than in "Comedy" category?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - You must load the additional data from 'GB_category_id.json' into memory before executing any operations.
            - To access 'GB_category_id.json', use the path '/data/GB_category_id.json'.
    '''
    with open('US_category_id.json') as gb:
        cat = json.load(gb)

    cat_list = []

    for i in cat['items']:
        cat_list.append((int(i['id']), i['snippet']['title']))

    cat_df = pd.DataFrame(cat_list, columns = ['id', 'category'])

    t = vdo_df.merge(cat_df, left_on = "category_id", right_on = "id")

    t_groupby_date_category = t.groupby(['trending_dt', 'category'])['views'].sum().reset_index()

    t_groupby_date_category

    pivot_df = t_groupby_date_category.pivot(index='trending_dt', columns='category', values='views').fillna(0)

    sports_comedy_comparison = pivot_df[['Sports', 'Comedy']].copy()
    sports_comedy_comparison['Sports > Comedy'] = sports_comedy_comparison['Sports'] > sports_comedy_comparison['Comedy']

    days_sports_more_than_comedy = sports_comedy_comparison['Sports > Comedy'].sum()

    return days_sports_more_than_comedy
