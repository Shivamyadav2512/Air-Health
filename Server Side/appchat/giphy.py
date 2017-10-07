import requests
import json

def get_gif(query):
	url = 'http://api.giphy.com/v1/gifs/search?q=' + query + '&api_key=dc6zaTOxFJmzC'
	r = requests.get(url)

	data = r.json()['data']

	res = data[0]['url']
	link = data[0]['images']['fixed_height']['url']
	return res, link


if __name__ == '__main__':
	print get_gif('many cat')
