import json
import re
import requests
import argparse
from prettytable import PrettyTable
import textwrap
from datetime import timedelta

# class Load:

    # def load_folder():
    
    # def read_metadata():

# get search results from search arguments
class Return_Results:

    def search_term(self):

        # submit search url to apple api and return results as JSON        
        values = {'term': term, 'country': country, 'media': media, 'entity': entity,
                    'attribute': attr, 'limit': limit}
        response = requests.get('https://itunes.apple.com/search?', params=values)

        results = response.json()
        results = results["results"]
        assert isinstance(results, object)
        return results
    
    def get_search_list(self): # display search results for entity=song or terms without entity
        pass
    
    def get_artists(self): # display search results for entity=artist
        pass
    
    # display search results for 
    def get_album(self):
        global artist_albums
        ar = PrettyTable()
        ar.field_names = ["Index", "Artist", "Album", "Tracks", "ID"]
        ar.align["Artist"] = "l"
        ar.align["Album"] = "l"
        ar.align["Tracks"] = "r"
        ar.align["ID"] = "r"
        artist_albums = {}
        for result in results:
            if result.get('wrapperType') == "artist":
                continue
            artist = result.get('artistName')
            album = result.get('collectionName')
            tracknum = result.get('trackCount')
            cid = result.get('collectionId')
            index = results.index(result) + 1
            ar.add_row([index, (textwrap.fill(artist, 40)), (textwrap.fill(album, 60)), tracknum, cid])
            artist_albums[(str(index))] = cid
        return ar
        return artist_albums
    
    def get_artwork_url(self): # get artwork url for downloading
        pass
    
    def get_audiobook(self): # get audiobook information if entity=audiobook
        pass
        
    # lookup results by id
    def get_id(self):
        lookup = {'id': id, 'country': country, 'entity': entity, 'attribute': attr,
                    'limit': limit}
        response = requests.get('https://itunes.apple.com/lookup?', params=lookup)
        
        results = response.json()
        results = results["results"]
        assert isinstance(results, object)
        return results
        
# display results from search terms
class Display_Results:

    # display albums by artist selected
    def display_artist_albums(self):
        daa = PrettyTable()
        daa.field_names = ["Index", "Album", "Artist", "Tracks", "Year", "Genre", "ID"]
        daa.align["Album"] = "l"
        daa.align["Artist"] = "l"
        daa.align["Tracks"] = "r"
        daa.align["ID"] = "r"
        
        artist_albums = {}
        
        for result in results:
            if result.get('wrapperType') == 'collection':
                album = result.get('collectionName')
                tracks = result.get('trackCount')
                artist = result.get('artistName')
                genre = result.get('primaryGenreName')
                year = result.get('releaseDate')
                # year = re.search("\d\d\d\d", year)
                # year = year.group()
                albumID = result.get('collectionId')
                albumID = str(albumID)
                index = results.index(result) + 1
                
                daa.add_row[(index, (textwrap.fill(album, 60)), (textwrap.fill(artist, 40)), tracks, year, genre, albumID)]
                artist_albums[(str(index))] = albumID
            return daa
            return artist_albums
    
    # display album tracklist when album selected
    def display_album(self):
        da = PrettyTable()
        da.field_names = ["#", "Title", "Artist", "Time", "Genre"]
        
        entity = "song"
        
        lookup = {'id': id, 'country': country, 'entity': entity, 'attribute': attr,
                    'limit': limit}
        response = requests.get('https://itunes.apple.com/lookup?', params=lookup)
        
        results = response.json()
        results = results["results"]
        for result in results:
            # if result.get('kind') == "song":
            num = str(result.get('trackNumber'))
            title = result.get('trackName')
            artist = result.get('artistName')
            time = result.get('trackTimeMillis')
            time = timedelta(milliseconds=time)
            time = str(time)
            time = str(time[3:7])
            genre = result.get('primaryGenreName')
            # print(f"{num} | {title} | {time} | {artist} | {genre}")
            da.add_row[(num, title, artist, time, genre)]
        return da
        
        
    # display audiobook information when audiobook found
    def display_audiobook(self):
        pass
    
    # display track search results
    def display_track_search(self):
        pass
    
class Choose:

    # use Userinput to choose which album to display from list
    def choose_album(self):
        pass
    
    # use Userinput to choose which artist to display from list
    def choose_artist(self):
        pass

class Save:

    # use eyeD3 library to save tags from track in album to MP3
    def save_to_mp3(self):
        pass



parser = argparse.ArgumentParser()
parser.add_argument("--term")
parser.add_argument("--country",
                    default="au")
parser.add_argument("--media")
parser.add_argument("--entity")
parser.add_argument("--attr")
parser.add_argument("--limit",
                    default="40")
parser.add_argument("--id")
args = parser.parse_args()

term = args.term
country = args.country
media = args.media
entity = args.entity
attr = args.attr
limit = str(args.limit)
id = str(args.id)

artist_albums = []

if args.id:
    results = Return_Results()
    results = results.get_id()
    da = Display_Results()
    da = da.display_album()
    print(da)
        

results = Return_Results()
results = results.search_term()

if args.entity == "album":
    ar = Return_Results().get_album()
    print(ar)
    
    new_search = input("Enter Album Index: ")
    id = artist_albums.get(new_search)
    print(id)