"""Usage:
  artist.py artist_name <artist_name> [--average] [--stdev]
  artist.py -h | --help |
"""


import requests
import json
import re
import xmltodict
import json
import statistics
from docopt import docopt


class ArtistManager:

    song_titles = None
    titles_endpoint = 'http://musicbrainz.org/ws/2/release-group/?query=artist'
    lyrics_endpoint = 'https://api.lyrics.ovh/v1/'
    lyrics_file_name = 'songsfile.csv'

    def __init__(self, artist):
        self.artist = artist
        self.write_lyrics_to_file()

    def get_titles(self):
        titles = []
        r = requests.get(
            f'{self.titles_endpoint}:{self.artist}'
        )
        resp = xmltodict.parse(r.content)
        data = json.dumps(resp)
        song_data = json.loads(data)['metadata']
        releases = song_data['release-group-list']['release-group']
        for release in releases:
            release_list = release['release-list']
            release_list = release_list['release-list'] if \
                'release-list' in release_list else \
                release_list['release']

            if type(release_list) is dict:
                title = release_list['title']

            if type(release_list) is list:
                for item in release_list:
                    title = item['title']

            title = re.sub(r'\W+', ' ', title)
            titles.append(title)

        return list(set(titles))

    def get_lyrics(self):
        lyrics_list = []

        self.song_titles = self.get_titles()
        for title in self.song_titles:
            response = requests.get(
                f"{self.lyrics_endpoint}{self.artist}/{title}")
            lyrics = response.json()["lyrics"]
            clean = re.sub(r'\n\s*\n', '\n', lyrics).strip()
            lyrics_list.append(clean)
        return lyrics_list

    def write_lyrics_to_file(self):

        self.song_titles = self.get_titles()
        lyrics = self.get_lyrics()

        with open(self.lyrics_file_name, 'w') as file_obj:
            file_obj.write("".join(str(item) for item in lyrics))

    def count_lyrics_words(self):
        file_obj = open(self.lyrics_file_name, 'r')
        lyrics_words_gen = (len(line.split()) for line in file_obj if not (
            line.startswith("VERSE") or line.startswith("CHORUS")))
        return lyrics_words_gen

    def get_lyrics_words_average(self):
        average = sum(self.count_lyrics_words()) / len(self.song_titles)
        return int(average)

    def get_stdev(self):
        words_count = self.count_lyrics_words()
        return statistics.stdev(words_count)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    artist_name = arguments["<artist_name>"]
    artist = ArtistManager(artist_name)
    if arguments["--average"]:
        average = artist.get_lyrics_words_average()
        ave_str = f"Average words for {artist_name} lyrics is {average}"
        print(ave_str)
    elif arguments["--stdev"]:
        stdev = artist.get_stdev()
        stdev_str = f"Standard Deviation for {artist_name} lyrics is {stdev}"
        print(stdev_str)
    else:
        print("Command not found")
        
#pip freeze > sample.txt

#clone repo
# cd to file location
# run pip install -r requirements.txt 
# python3 -m nhs artist_name beyonce --average  || python3 -m nhs artist_name beyonce --average or

