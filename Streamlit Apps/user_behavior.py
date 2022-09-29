import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px



engine = pyodbc.connect("Driver={SQL Server Native Client 11.0};""Server=LAPTOP-V3754MEK;""Database=Spotify;""Trusted_Connection=yes;")
cursor = engine.cursor()
query = pd.read_sql('''SELECT DISTINCT dt.track_name, dt.artist_name, af.*
FROM audio_features2 af 
JOIN dim_tracks dt ON af.uri = dt.track_uri2''', engine)
query['music_key'] = query['music_key'].map({0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F', 6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'})
query['modal'] = query['modal'].map({'0': 'Minor', '1': 'Major'})
query['time_signature'] = query['time_signature'].map({'3': '3/4', '4': '4/4', '5': '5/4', '6': '6/4', '7': '7/4'})
query2 = pd.melt(query, id_vars=['uri'], var_name='metrics', value_name='score', value_vars=['instrumentalness', 'danceability', 'energy', 'speechiness', 'acousticness', 'valence', 'liveness'])

st.set_page_config(page_title='User Behavior App', layout='centered')

st.markdown(""" <style> 
                        .title { font-size: 45px;
                                 text-align: center;}
                        .header { font-size: 20px;
                                  padding-left: 35px;
                                  font-weight: bold;}
                        .header2 { font-size: 20px;
                                   padding-left: 33px;
                                   font-weight: bold;}
                        .header3 { font-size: 20px;
                                   padding-left: 25px;
                                   font-weight: bold;}
                        .header4 { font-size: 20px;
                                   padding-left: 0px;
                                   font-weight: bold;}
                        .ban-font { font-size: 30px;
                                    padding-left: 8px;}
                        .ban-font2 { font-size: 30px;
                                  padding-left: 25px;}
                        .ban-font3 { font-size: 30px;
                                     padding-left: 0px;}
                        .ban-font4 { font-size: 30px;
                                     padding-left: 30px;}
                                  
                </style>""", unsafe_allow_html=True)



artists = query['artist_name'].drop_duplicates()
artists = artists.sort_values()
artist_choice = st.sidebar.selectbox('Choose an Artist:', artists)
tracks = query['track_name'].loc[query['artist_name'] == artist_choice]
tracks = tracks.sort_values()
track_choice = st.sidebar.selectbox('Choose a Song', tracks)
empty = st.sidebar.text('')
output = query['uri'].loc[(query['track_name'] == track_choice) & (query['artist_name'] == artist_choice)].values
output_bpm = query['tempo'].loc[(query['track_name'] == track_choice) & (query['artist_name'] == artist_choice)].values
output_bpm = output_bpm.astype(float)
output_key = query['music_key'].loc[(query['track_name'] == track_choice) & (query['artist_name'] == artist_choice)].values
output_mode = query['modal'].loc[(query['track_name'] == track_choice) & (query['artist_name'] == artist_choice)].values
output_sig = query['time_signature'].loc[(query['track_name'] == track_choice) & (query['artist_name'] == artist_choice)].values
uri_output = st.sidebar.selectbox('Select the URI:', options=(output))

page_title = st.markdown('''<h1 class="title"">What's Your Audio Aura?</h1>''', unsafe_allow_html=True)
empty_line = st.text('')
empty_line2 = st.text('')
empty_line3 = st.text('')
empty_line4 = st.text('')
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col3:
    filters_txt = st.subheader('Metrics')
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    bpm_ban = st.markdown(f'''<p class="header">BPM</p><p class="ban-font">{output_bpm}</p>''', unsafe_allow_html=True)
with col2:
    key_ban = st.markdown(f'''<p class="header2">Key</p><p class="ban-font2">{output_key}</p>''', unsafe_allow_html=True)
with col3:
    mode_ban = st.markdown(f'''<p class="header3">Mode</p><p class="ban-font3">{output_mode}</p>''', unsafe_allow_html=True)
with col4:
    sig_ban = st.markdown(f'''<p class="header4">Time Signature</p><p class="ban-font4">{output_sig}</p>''', unsafe_allow_html=True)

fig = px.bar_polar(query2.loc[query2['uri'] == uri_output], theta='metrics', r='score', range_r=[0.0,1.0], hover_name='metrics', hover_data={'score':True, 'metrics':False}, width=750, height=600, color_continuous_scale='YlGn', color='score', template='plotly')
st.plotly_chart(fig)

with st.container():
    st.markdown('''<h3>Metric Definitions</h3>\n<ul><li><b>Instrumentalness<br> Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. \n</li>
    <li>Danceability<br> Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. \n</li>
    <li>Energy<br> A measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.  \n</li>
    <li>Speechiness<br> This detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.</li>
    <li>Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. \n</li>
    <li>Valence<br> A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).  \n</li>
    <li>Liveness<br> Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.  \n</li>''', unsafe_allow_html=True)

    

    