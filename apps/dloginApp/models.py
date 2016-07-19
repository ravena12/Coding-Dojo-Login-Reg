from __future__ import unicode_literals
from django.db import models
from django.contrib  import messages
import re
import bcrypt 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

	def isValidReg(self, userInfo, request):
		passflag = True
		password = userInfo['password']
		if not EMAIL_REGEX.match(userInfo['email']):
			passflag = False
		if len(userInfo['first_name']) < 1:
			messages.error(request,"First name cannot be empty!")
			passflag = False
		if len(userInfo['last_name']) < 1:
			messages.error(request, "Last Name cannot be empty!")
			passflag = False
		if len(userInfo['email']) < 1:
			messages.error(request, "Email cannot be empty")
			passflag = False
		if len(userInfo['password']) < 1:
			messages.error(request, "Password cannot be empty!" )
			passflag = False
		if len(userInfo['confirm']) < 1:
			messages.error(request, "Password cannot be empty!")
			passflag = False
		if userInfo['password'] != userInfo['confirm']:
			messages.error(request,"Passwords must match")
			passflag = False

		if len(User.objects.filter(email = userInfo['email'])) > 0:
			messages.error(request, "You already exist") 
			passflag = False 
		#.filter will return an array of user objects     

		if passflag == True:
			messages.success(request, 'THANKS MAN please login now')
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			print hashed
			User.objects.create(email = userInfo['email'], first_name = userInfo['first_name'], last_name = userInfo ['last_name'], password = hashed)
		return passflag
 
 	def login(self, userInfo, request):
 		passflag = False
		if len(User.objects.filter(email = userInfo['email'])) >0:
			#user is the table objects is the table manager get is a method of the manager 
			#.get returns the user object and calling password gets the password on that object
			# we use email to find its relationship to the encrypted password  encrypted password since we do not know the value of said encrypted password
			hashed = User.objects.get(email = userInfo['email']).password
			hashed = hashed.encode('utf-8')
			password= userInfo['password']
			password = password.encode('utf-8')
			if bcrypt.hashpw(password, hashed) == hashed:
				passflag = True
		else:
			messages.error(request, 'Cannot be empty / does not match')
		return passflag
	


class User(models.Model):
	email = models.EmailField()
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now_add = True)
	userManager = UserManager()
	objects = models.Manager()

	#user manager is only for validation method.  
	#objects uses  get, filter, create stuffs 

