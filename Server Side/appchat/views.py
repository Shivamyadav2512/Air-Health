from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from testing import predict 
import requests
import json
#import urllib2
import text


# Create your views here.

def testing(request):
	return HttpResponse("Testing successful...")


class CommonUrl(generic.View):

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello")


class ChatBot(generic.View):

	def get(self, request, *args, **kwargs):
		print self.request.GET
		if self.request.GET.get('hub.verify_token') == '123456789':
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
	access_token = 'EAABtDsMCTOQBADzY7CdSsmfILOyusZCPo4LxqaTIau8ew9ZA5CDwDVGfJycWNamxSHRoZBu0cZALDKrYW2Im1dd8KSdhL5zrw3dCnDWpq7BUNgPSI2m9cMGvi6sYxSszrgYHIOlF7ZCQP8raWmQscYjlVfAJ5utEw3WVPQ9Xi3TaL5Jzj7ugh'
	url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

	resp = generate_response(message)
	#send_resp = {"recipient":{"id":user_id}, "message":{"text":resp, "attachment":{"type":"image", "payload":{"url": attach_link}}}}
	send_resp = {"recipient":{"id":user_id}, "message":{"text": resp}}
	response_msg = json.dumps(send_resp)
	status = requests.post(url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def pm10(city, location):
	location = location.strip(' ')
	b = ''
	for i in location:
		if i == ' ':
			b+='%20'
		else:
			b+=i
	url = 'https://api.openaq.org/v1/measurements?city='+city+'&location='+b+'&parameter=pm10'
	result = requests.get(url).content
	result = json.loads(result)
	prediction = predict(result)
	if result['meta']['found'] == 0:
		return 'No data found for this location.'
	else:
		return 'The pm10 value for this region is ' + str(result['results'][0]['value']) + ' and the predicted pm10 value for next hour is '+str(prediction)

def generate_response(msg):
    listy = msg.split(',')
    location=listy[0]
    city=listy[1]
    return pm10(city,location)
  
	
