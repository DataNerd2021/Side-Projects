from asyncio.windows_events import NULL
from logging import PlaceHolder
from pydoc import plain
from select import select
from turtle import width
import streamlit as st 
import pandas as pd




    



# Set page title and layout options
st.set_page_config(page_title='Spotify Playlist Challenge', layout='centered')

# Set page header
st.title('Most Popular Playlist Challenge')

# set challenge description
st.text('The purpose of this challenge is to make the most popular playlist with a MAXIMUM of\n10 songs and 1 artist from our database of 2,262,355 songs derived from over\n1,000,000 Spotify Playlists. Here is the points break down: \n\t\tPopularity Rank:   \t\tPoints:\n   \t\t    1 - 1,000  \t\t\t  500\n  \t\t  1,001 - 5,000  \t\t  250\n   \t\t  5,001 - 10,000  \t\t  100\n       \t\t 10,001 - 24,999   \t\t   50\n    \t\t     25,000+    \t\t   25')


# import datasets
df1 = pd.read_csv("C:\\Users\\Chase\\OneDrive\\Documents\\Career Development\\Pandas Practice\\Streamlit\\tracks2.csv")
df2 = pd.read_csv("C:\\Users\\Chase\\OneDrive\\Documents\\Career Development\\Pandas Practice\\Streamlit\\tracks3.csv")
df3 = pd.read_csv("C:\\Users\\Chase\\OneDrive\\Documents\\Career Development\\Pandas Practice\\Streamlit\\tracks4.csv", nrows=150000)
df = pd.concat([df1, df2, df3])
df = df.rename(columns={'track_name': "Track Name", 'album_name': "Album Name", 'artist_name':"Artist Name", 'points':'Points'})
data = {'Track Name': [''], 'Artist Name': [''], 'Album Name': ['']}

# define variable for search results dataset

data = pd.DataFrame(data)



# define search parameter buttons
radio_btn = st.radio('Search by:', options=['Artist', 'Album', 'Track'], horizontal=True)


# if the user chooses to search by Artist

if radio_btn == 'Artist':
    artist_search = st.text_input('Enter Search Here:', placeholder='Enter artist name...')
    df_results = df[df['Artist Name'].str.startswith(artist_search.title(), na=False)]
    select_item = st.multiselect('Select Rows', df_results['Artist Name'].index[:1000]) 
    artist_results = st.dataframe(df_results[['Track Name', 'Album Name', 'Artist Name']])
    st.write('#### Your Playlist:')
    select_item = pd.DataFrame(select_item)
    select_item = select_item.merge(df_results, how='left', left_on=0, right_on=df_results.index)
    select_item['rank'] = select_item['rank'].astype('int64')
    select_item = pd.DataFrame(select_item)
    select_item = select_item[['Track Name', 'Album Name', 'Artist Name', 'Points']]
    
    items_selected = st.dataframe(select_item)
    total_points = select_item['Points'].sum()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit_btn = st.button('Submit')
        if submit_btn:
            with col2:
                st.write(f'### Total Points: {total_points}')
elif radio_btn == 'Album':
    album_search = st.text_input('Enter Search Here:', placeholder='Enter album name...')
    df_results = df[df['Album Name'].str.startswith(album_search.title(), na=False)]
    select_item = st.multiselect('Select Rows', df_results['Album Name'].index[:1000]) 
    artist_results = st.dataframe(df_results[['Track Name', 'Album Name', 'Artist Name']])
    st.write('#### Your Playlist:')
    select_item = pd.DataFrame(select_item)
    select_item = select_item.merge(df_results, how='left', left_on=0, right_on=df_results.index)
    select_item['rank'] = select_item['rank'].astype('int64')
    select_item = pd.DataFrame(select_item)
    select_item = select_item[['Track Name', 'Album Name', 'Artist Name', 'Points']]
    
    items_selected = st.dataframe(select_item)
    total_points = select_item['Points'].sum()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit_btn = st.button('Submit')
        if submit_btn:
            with col2:
                st.write(f'### Total Points: {total_points}')
if radio_btn == 'Track':
    track_search = st.text_input('Enter Search Here:', placeholder='Enter track name...')
    df_results = df[df['Track Name'].str.startswith(track_search.title(), na=False)]
    select_item = st.multiselect('Select Rows', df_results['Track Name'].index[:1000]) 
    artist_results = st.dataframe(df_results[['Track Name', 'Album Name', 'Artist Name']])
    st.write('#### Your Playlist:')
    select_item = pd.DataFrame(select_item)
    select_item = select_item.merge(df_results, how='left', left_on=0, right_on=df_results.index)
    select_item['rank'] = select_item['rank'].astype('int64')
    select_item = pd.DataFrame(select_item)
    select_item = select_item[['Track Name', 'Album Name', 'Artist Name', 'Points']]
    
    items_selected = st.dataframe(select_item)
    total_points = select_item['Points'].sum()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit_btn = st.button('Submit')
        if submit_btn:
            with col2:
                st.write(f'### Total Points: {total_points}')
    

