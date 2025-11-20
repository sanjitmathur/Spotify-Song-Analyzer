#.\.venv\Scripts\Activate.ps1
#streamlit run main.py --server.headless True
#streamlit run main.py

 
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
from dotenv import load_dotenv
import altair as alt
from datetime import datetime, timezone, timedelta

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://127.0.0.1:8501'
# Added 'playlist-modify-public' to allow playlist creation
SCOPE = "user-top-read user-read-recently-played playlist-modify-public" 

st.set_page_config(page_title="Spotify Song Analysis", page_icon=":musical_note:")
st.title("Analysis of Your Top Spotify Songs")

def get_spotify_token():
    if "token_info" in st.session_state:
        if st.session_state.token_info['expires_at'] < pd.Timestamp.now().timestamp():
            auth_manager = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
            st.session_state.token_info = auth_manager.refresh_access_token(st.session_state.token_info['refresh_token'])
        return st.session_state.token_info

    try:
        query_params = st.query_params.to_dict()
        auth_code = query_params.get("code")
    except:
        query_params = st.experimental_get_query_params()
        auth_code = query_params.get("code")
        if isinstance(auth_code, list) and len(auth_code) > 0:
            auth_code = auth_code[0]

    if not auth_code:
        auth_manager = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
        auth_url = auth_manager.get_authorize_url()
        
        try:
            with open("login_button.html", "r") as f:
                html_template = f.read()
            st.markdown(html_template.replace("{auth_url}", auth_url), unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("login_button.html file not found. Please ensure it is in the same directory.")
        
        st.stop()

    if auth_code:
        auth_manager = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
        try:
            token_info = auth_manager.get_access_token(auth_code, as_dict=True)
            st.session_state.token_info = token_info
            try:
                st.query_params.clear()
            except:
                st.experimental_set_query_params()
            st.rerun()
        except Exception as e:
            st.error(f"Error getting access token: {e}")
            st.stop()

if not CLIENT_ID or not CLIENT_SECRET:
    st.error("CLIENT_ID or CLIENT_SECRET is not set in your .env file.")
    st.stop()

token_info = get_spotify_token()

if token_info:
    st.success("You are successfully logged in!")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    try:
        recently_played = sp.current_user_recently_played(limit=50)
        
        total_duration_ms_30_days = 0
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        for item in recently_played['items']:
            played_at_dt = datetime.fromisoformat(item['played_at'])
            if played_at_dt > thirty_days_ago:
                total_duration_ms_30_days += item['track']['duration_ms']
            
        total_duration_minutes = (total_duration_ms_30_days / 1000) / 60
        
        st.metric(
            label="Total Listen Time (Last 30 Days)", 
            value=f"{total_duration_minutes:.2f} minutes",
            help="Calculated from your 50 most recently played tracks."
        )
        
        top_tracks_data = sp.current_user_top_tracks(limit=15, time_range='medium_term')
        
        if top_tracks_data and top_tracks_data['items']:
            
            tracks_info = []
            track_uris = [] # List to store URIs for playlist creation
            
            for item in top_tracks_data['items']:
                tracks_info.append({
                    'track_name': item['name'],
                    'artist': item['artists'][0]['name'],
                    'popularity': item['popularity'],
                })
                track_uris.append(item['uri'])
            
            df = pd.DataFrame(tracks_info)
            
            st.subheader("Your Top 15 Tracks by Popularity")
            
            df_chart = df[['track_name', 'popularity']]
            
            chart = alt.Chart(df_chart).mark_bar().encode(
                x=alt.X('track_name', title='Track Name', sort=None),
                y=alt.Y('popularity', title='Popularity')
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            st.subheader("Your Top 15 Tracks List")
            
            df_display = df[['track_name', 'artist', 'popularity']]
            df_display = df_display.rename(columns={
                'track_name': 'Track Name',
                'artist': 'Artist',
                'popularity': 'Popularity (0-100)'
            })
            
            df_display.index = range(1, len(df_display) + 1)
            
            st.dataframe(df_display, height=565)
            
            # Playlist Creation Section
            st.write("---")
            st.subheader("Save this list")
            
            # 1. Custom CSS to style the Streamlit button to match your HTML login button
            st.markdown("""
            <style>
            /* Target the main button inside the Streamlit container */
            div.stButton > button {
                background-color: #1DB954 !important;
                color: white !important;
                padding: 12px 30px !important;
                border-radius: 30px !important;
                border: 2px solid black !important;
                font-weight: 700 !important;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
                letter-spacing: 0.5px !important;
                -webkit-text-stroke: 0.3px black !important;
                text-shadow: 0 1px 2px rgba(0,0,0,0.15) !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease-in-out !important;
                min-width: 200px;
                display: block;
                margin: 0 auto; /* Center it if possible, though Streamlit layout controls this */
            }
            
            div.stButton > button:hover {
                background-color: #191414 !important;
                color: #1DB954 !important;
                border-color: #1DB954 !important;
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(0,0,0,0.2) !important;
                -webkit-text-stroke: 0px !important;
                text-shadow: 0 0 8px rgba(29, 185, 84, 0.4) !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # 2. Playlist Name Input
            default_playlist_name = f"My Top Tracks - {datetime.now().strftime('%Y-%m-%d')}"
            playlist_name_input = st.text_input("Name your playlist:", value=default_playlist_name)
            
            # 3. The Button (Styled by the CSS above)
            if st.button("Create Playlist on Spotify"):
                if not playlist_name_input.strip():
                    st.error("Please enter a playlist name.")
                else:
                    try:
                        user_id = sp.current_user()['id']
                        
                        # Create the playlist
                        playlist = sp.user_playlist_create(user_id, playlist_name_input, public=True)
                        
                        # Add tracks
                        sp.playlist_add_items(playlist['id'], track_uris)
                        
                        st.balloons()
                        st.success(f"Playlist '{playlist_name_input}' created successfully! Check your Spotify library.")
                    except Exception as e:
                        st.error(f"Failed to create playlist: {e}")
            
        else:
            st.write("Could not retrieve top tracks.")

    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Error fetching data from Spotify: {e}")