from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	#return HttpResponse("<h2>Hey!</h2>");
	return render(request, 'homepage/Justpage.html')

