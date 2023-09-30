from flask import Flask , render_template,request , jsonify
# import requests
import pandas as pd
import numpy as np
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


app = Flask(__name__)


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[:9]
    new_m=music.iloc[[i[0] for i in distances]].copy()
    recommended_music_names = []
    img = []
    for i in distances:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        img.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        # recommended_music_names.append(music.iloc[i[0]].song)
    new_m['img']=img  
    return new_m[['artist','song','img']]

music=pickle.load(open('music.pkl','rb'))
music=pd.DataFrame(music)
similarity=pickle.load(open('similarity.pkl','rb'))
s=np.array(music.sort_values('song'))



@app.route("/")
def index():
    return render_template('index.html',title='music Recommendation',s=s)

@app.route("/music/<music>")
def pred(music):    
    data=recommend(music)
    m_music = data.iloc[0,:]
    data = data.iloc[1:,:]
    return render_template('music.html',title=music,musics=data.T.to_dict(), m_data= m_music.to_dict() , s=s)
    # return jsonify(data)
    



if __name__=="__main__":
    app.run(debug=True)