# For help check out:
# https://github.com/willamesoares/lyrics-crawler
# https://github.com/johnwmillr/LyricsGenius

import requests
from bs4 import BeautifulSoup
import re

TOKEN = 'HIniJH6wMUbXlDpq8M9TaXmJ3KJtdqcTOkzejahqagZLBzgE8YtMYe8O0P_HwvM_'
base_url = 'http://api.genius.com'
headers = {'Authorization': 'Bearer ' + TOKEN}

def get_song_path(artist_name, song_title):
	search_url = base_url + '/search'
	
	data = {'q': song_title}
	response = requests.get(search_url, params=data, headers=headers)
	json = response.json()
	for hit in json['response']['hits']:
		if artist_name in hit['result']['primary_artist']['name']:
			return hit['result']['api_path']
	return None

def get_lyrics(song_api_path):
	song_url = base_url + song_api_path
	response = requests.get(song_url, headers=headers)
	json = response.json()
	path = json['response']['song']['path']
	page_url = 'http://genius.com' + path
	page = requests.get(page_url)
	html = BeautifulSoup(page.text, 'html.parser')
	# Remove script tags that they put in the middle of the lyrics
	[h.extract() for h in html('script')]
	lyrics = html.find('div', class_='lyrics').get_text()
	return lyrics

f = open('songs_list.txt', 'r')
songs = f.read().split('\n')
f.close()
songs = [s for s in songs if len(s) > 0]
not_founds = []

for i in range(len(songs)):
	title = songs[i]
	print(str(i + 1) + '/' + str(len(songs)) + '\t' + title)
	path = get_song_path('twenty one pilots', title)
	if path:
		lyrics = get_lyrics(path)
		lyrics = re.sub('\[.*\]\n', '', lyrics)
		f = open('Dataset/' + str(i + 1).zfill(3) + '_ ' + title + '.txt', 'w')
		f.write(lyrics)
		f.close()
	else:
		print('\t\tNot found.')
		not_founds.append((i, title))

print('Done.')
print('The following were not found:')
for i in not_founds:
	print('\t{}. {}'.format(i[0], i[1]))