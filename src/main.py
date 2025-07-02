# app.py
import streamlit as st
from recommend import df, recommend_songs

#import the get_lyrics function from lyrics file
from lyrics import get_lyrics,clean_lyrics

#importing spotify
from spotify_api import create_spotify_client, search_track

sp = create_spotify_client()

# Set custom Streamlit page config
st.set_page_config(
    page_title="Music Recommender 🎵",
    page_icon="🎧",  # You can also use a path to a .ico or .png file
    layout="centered"
)


st.title("🎶 Instant Music Recommender")

#song_list = sorted(df['song'].dropna().unique())
#selected_song = st.selectbox("🎵 Select a song:", song_list)

song_name = st.text_input("Enter any song name:")
artist_name = st.text_input("Enter the artist's name (Optional):")
if st.button("🚀 Recommend Similar Songs"):
    if song_name.strip()=="" :
        st.warning("Please enter a song name.")
    else:
        st.success(f"Searching for songs similar to {song_name}")

    raw_lyrics = get_lyrics(song_name, artist_name)
    lyrics = clean_lyrics(raw_lyrics)
    spotify_track = search_track(sp, song_name, artist_name)

    if spotify_track:
        st.markdown(f"▶️ [Open in Spotify]({spotify_track['external_urls']['spotify']})")
    else:
        st.warning("Spotify track not found.")

    if "Lyrics not found" not in lyrics:
        st.subheader("🎤Lyrics found.")
        st.text_area("Lyrics:", lyrics, height=250)

        recommendations = recommend_songs(lyrics)

        st.subheader("🎧 Recommended Songs Based on Lyrics:")
        for i,row in recommendations.iterrows():
            st.write(f"**{i+1}.{row['song']}** - *{row['artist']}*")
    else:
        st.error("❌ Could not find lyrics.")
