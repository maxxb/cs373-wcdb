from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render

def home(request):
	return render(request, 'base.html')