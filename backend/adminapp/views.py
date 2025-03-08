import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def admin(request):
	return HttpResponse(
	json.dumps({"message":"Admin Application"}),
     content_type="Application/json"
	)
