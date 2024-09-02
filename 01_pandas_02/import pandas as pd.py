import pandas as pd
import json

"""
    ASSIGNMENT 1 (STUDENT VERSION):
    Using pandas to explore youtube trending data from GB (GBvideos.csv and GB_category_id.json) and answer the questions.
"""


def Q1():
    """
        1. How many rows are there in the GBvideos.csv after removing duplications?
        - To access 'GBvideos.csv', use the path '/data/GBvideos.csv'.
    """
    df = pd.read_csv('/data/GBvideos.csv')
    # print(df.shape)
    df.drop_duplicates(inplace=True)
    ans = df.shape[0]
    print(ans)
    return ans


def Q2(vdo_df):
    '''
        2. How many VDO that have "dislikes" more than "likes"? Make sure that you count only unique title!
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    ans = vdo_df[vdo_df.dislikes > vdo_df.likes].title.nunique()
    print(ans)
    return ans


def Q3(vdo_df):
    '''
        3. How many VDO that are trending on 22 Jan 2018 with comments more than 10,000 comments?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - The trending date of vdo_df is represented as 'YY.DD.MM'. For example, January 22, 2018, is represented as '18.22.01'.
    '''
    # TODO: Paste your code here
    ans = vdo_df[vdo_df.trending_date.str.contains('18.22.01') & (vdo_df.comment_count > 10000)].shape[0]
    print(ans)
    return ans


def Q4(vdo_df):
    '''
        4. Which trending date that has the minimum average number of comments per VDO?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # TODO:  Paste your code here
    dfDate = vdo_df.groupby('trending_date')
    ans = dfDate.comment_count.mean().sort_values().index[0]
    print(ans)
    return ans


def Q5(vdo_df):
    '''
        5. Compare "Sports" and "Comedy", how many days that there are more total daily views of VDO in "Sports" category than in "Comedy" category?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - You must load the additional data from 'GB_category_id.json' into memory before executing any operations.
            - To access 'GB_category_id.json', use the path '/data/GB_category_id.json'.
    '''
    # TODO:  Paste your code here
    with open('/data/GB_category_id.json') as fd:
        cat = json.load(fd)
    cat_list = []
    for d in cat['items']:
        cat_list.append((int(d['id']), d['snippet']['title']))

    cat_df = pd.DataFrame(cat_list, columns=['id', 'category'])
    df_merge = pd.merge(vdo_df, cat_df, left_on='category_id', right_on='id')
    group = df_merge.groupby('category')
    sports = group.get_group('Sports').groupby('trending_date').views.sum()
    comedy = group.get_group('Comedy').groupby('trending_date').views.sum()

    sport_comedy = pd.merge(sports, comedy, on='trending_date', how='left').rename(
        columns={'views_x': 'sports', 'views_y': 'comedy'})
    ans = sport_comedy[sport_comedy.sports > sport_comedy.comedy].shape[0]
    return ans
