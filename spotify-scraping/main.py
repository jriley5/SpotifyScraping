import json
from timeit import default_timer as timer
import requests
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import os.path
from timeit import default_timer as timer

# this script is fed a list of playlists and their track counts, and dumps the album art as images to /images,
# and dumps a list of SpotifySong objects to json
# resize.py converts these images to 512x512 and turns grayscale images to RGB

save_path = "change this to directory for saving images"


class SpotifySong:
    def __init__(self, id_num, track_uri, track_name, artist_name, album,
                 artist_genres, artist_pop, cover_art, track_pop):
        self.id_num = id_num
        self.track_uri = track_uri
        self.track_pop = track_pop
        self.cover_art = cover_art
        self.album = album
        self.artist_genres = artist_genres
        self.artist_pop = artist_pop
        self.artist_name = artist_name
        self.track_name = track_name


# Authentication - without user
cid = "6eda2f310b924b8b88b5b9ee61204d0e"
secret = "0e944dd3956045fbba7a607110ff74c7"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# extract track URIs from playlist link
playlist_URIs = []
playlist_track_counts = []
master_song_list = []
current_track_id = 0

# read playlists and track counts from file
with open('playlists.txt') as f:
    for line in f:
        split = line.split()
        playlist_URIs.append(split[0].split("/")[-1].split("?")[0])
        playlist_track_counts.append(int(split[1]))


# saves album art given a SpotifySong object
def save_album_art(track_name, cover_art_url, counter):
    art_filename = str.zfill(str(counter), 6) + "-" + track_name
    completeName = os.path.join(save_path, art_filename)
    response = requests.get(cover_art_url)
    file = open(completeName, "wb")
    file.write(response.content)
    file.close()


print("beginning scrape of playlist(s)...")


# scrape a single playlist
def scrape_playlist(uri, num_tracks):
    global master_song_list, current_track_id
    print("number of tracks: " + str(num_tracks))

    # Spotify only lets us access 100 tracks at a time, so we have to use the
    # "offset" param to iterate through large playlists
    num_repeats = max(int(num_tracks / 100), 1)

    for r in range(num_repeats):
        start = timer()
        current_offset = 100 * r

        print(str(current_offset) + " tracks processed")

        for track in sp.playlist_tracks(uri, offset=current_offset)["items"]:

            # There's a lot of info we can grab from each track.
            # A slightly different problem for our project could have involved using
            # artist names or genre tags as input for our GAN.

            if current_track_id <= 1548:
                current_track_id += 1
                continue

            # URI
            track_uri = track["track"]["uri"]
            #
            if track_uri[0:13] == "spotify:local":
                current_track_id += 1
                continue

            # Track name
            track_name = track["track"]["name"]
            track_name = track_name.replace('/', "")

            # Info we decided we didn't want...

            # Main Artist
            # artist_uri = track["track"]["artists"][0]["uri"]
            # artist_info = sp.artist(artist_uri)
            #
            # Name, popularity, genre
            # artist_name = track["track"]["artists"][0]["name"]
            # artist_pop = artist_info["popularity"]
            # artist_genres = artist_info["genres"]
            # print(track_name)
            # # Album
            # album = track["track"]["album"]["name"]
            try:
                cover_art = track["track"]['album']['images'][0]['url']
            except IndexError:
                print("no cover art")

            # # Popularity of the track
            # track_pop = track["track"]["popularity"]

            # s = SpotifySong(current_track_id, track_uri, track_name, artist_name, album, artist_genres, artist_pop,
            #                 cover_art, track_pop)
            save_album_art(track_name, cover_art, current_track_id)
            #
            # master_song_list.append(s)
            current_track_id += 1

        end = timer()
        print("TIME: processed last 100 songs in " + str(end - start) + " seconds")

    print("finished this playlist")


# loop through all playlists and scrape
for i in range(len(playlist_URIs)):
    scrape_playlist(playlist_URIs[i], playlist_track_counts[i])

# This program is also able to dump all of the above song info to json.
# We opted out of this once we gathered our 30k image dataset, but could be useful in other problems.

# json_string = json.dumps(master_song_list, default=vars, indent=4)
# with open('json_data.json', 'w') as outfile:
#     outfile.write(json_string)


print("Finished scraping!")
