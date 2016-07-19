from django.shortcuts import render, redirect
from .models import User
from django.contrib  import messages
import datetime

def index(request):
	return render(request, 'dloginTemp/index.html')

def register(request):
	if User.userManager.isValidReg(request.POST,request):
		passflag = True
		return redirect ('/')

	else:
		passflag = False
		return redirect('/')
def login(request):
	if User.userManager.login(request.POST, request):
		context = {
		"user": User.objects.get(email =request.POST['email'])
		}
		passflag=True
		return render(request, 'dloginTemp/results.html', context)
	else: 
		passflag = False

		return redirect('/')


def success(request):
	context = {
		'emails': User.userManager.all()[::-1]
	}
	return render(request, 'dloginTemp/results.html', context)




  
 