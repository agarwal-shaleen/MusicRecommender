from dotenv import load_dotenv
import os
import lyricsgenius

load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

def get_lyrics(song, artist=""):
    try:
        result = genius.search_song(song,artist)
        if result:
            return result.lyrics
        else:
            return "Lyrics not found."
    except Exception as e:
        return f"Error: {str(e)}"

def clean_lyrics(lyrics):
    lines = lyrics.split("\n")
    clean_lines = []
    for line in lines:
        # skipping non-lyric lines
        if"Lyrics" in line or "Translations" in line or "Read More" in line: continue
        clean_lines.append(line)

    return "\n".join(clean_lines).strip()