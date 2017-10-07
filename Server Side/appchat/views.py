from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import text

class ChatBot(generic.View):

	def get(self, request, *args, **kwargs):
		print self.request.GET
		if self.request.GET.get('hub.verify_token') == verication_token:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		message = json.loads(self.request.body.encode('utf-8'))

		for entry in message['entry']:
			for msg in entry.get('messaging'):
				print msg.get('message')

				if "text" in msg.get('message').keys():
					reply_to_message(msg.get('sender')['id'], msg.get('message')['text'])
				else:
					print "Some Error!!!"

		return HttpResponse("None")


def reply_to_message(user_id, message):
    access_token = '' #add your access token here
	url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

	resp = generate_response(message)
	send_resp = {"recipient":{"id":user_id}, "message":{"text": resp}}
	response_msg = json.dumps(send_resp)
	status = requests.post(url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def pollution_index(city, location):
	location = location.strip(' ')
	b = ''
	for i in location:
		if i == ' ':
			b+='%20'
		else:
			b+=i
	url = 'https://api.openaq.org/v1/measurements?city='+city+'&location='+b+'&date_from=2017-10-01&date_to=2017-10-07&parameter=pm10'
	result = requests.get(url).content
	result = json.loads(result)
	if result['meta']['found'] == 0:
		return 'No data found for this location.'
	else:
		return result['results'][-1]['value']

def generate_response(msg):
	msg= msg.split(',')
	location=msg[0]
	city=msg[1]
	result = pollution_index(city,location)
	if result != 'No data found for this location.':
		return 'Hi, The pm10 value for this location is '+str(result)
	else:
		return result
	
	
