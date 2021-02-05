# Interact 
# Description: 
Interact is program which, when given the name of an artist, will produce the average
number of words in their songs and also produce a Standard Deviation of words in their songs.

# Installation And Usage:
- clone Repository
- cd to file location
- run pip install -r requirements.txt 
- Api endpoint to get artist: http://musicbrainz.org/ws/2/release-group/?query=artist
- Api to get artist lyrics: https://api.lyrics.ovh/v1/
- Exmample usage of average words in an artist songs : python3 -m artist artist_name beyonce --average  
- Example of standard deviation for words in artist songs: python3 -m artist artist_name beyonce --stdev

