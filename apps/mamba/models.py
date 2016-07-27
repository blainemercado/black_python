from __future__ import unicode_literals

from django.db import models
import bcrypt
from datetime import date, datetime

class UserManager(models.Manager):
	def validName(self, name, username):
		if len(name) < 3:
			return(False, "Name must be at least 3 characters")
		if len(username) < 3:
			return(False, "Username must be at least 3 character")
		if len(User.objects.filter(username=username)) > 0:
			return(False, "Sorry, that Username has already been taken")
		return True
	def validPass(self, pass1, pass2):
		if len(pass1) < 8:
			return(False, "Password must be at least 8 characters")
		if pass2 == pass1:
			return True
		else:
			return(False, "Passwords do not match")
	def validDate(self, date_hired):
		if len(date_hired) == 0:
			return(False, "Please enter a date prior to today")
		date_hired = datetime.strptime(date_hired,'%m/%d/%Y')
		if datetime.today() > date_hired:
			return (True, date_hired)
		else:
			return(False, "Please enter a date prior to today")
	def validate(self, name, username, pass1, pass2, date_hired):
		nameResults = User.userManager.validName(name, username)
		if nameResults==True:
			pass
		else:
			return nameResults
		passResults = User.userManager.validPass(pass1, pass2)
		if passResults==True:
			pass
		else:
			return passResults
		dateResults = User.userManager.validDate(date_hired)
		if dateResults[0]==True:
			date_hired=dateResults[1]
		else:
			return dateResults
		pass1 = pass1.encode(encoding="utf-8", errors="strict")
		hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
		currentUser = User.objects.create(name=name, username=username, password=hashed, date_hired=date_hired)
		return(True, currentUser)
	def login(self, username, pass1):
		if len(User.objects.filter(username=username)) == 0:
			return (False, "username")
		else:
			userInfo = User.objects.filter(username=username)
		if bcrypt.hashpw(pass1.encode(encoding="utf-8", errors="strict"), userInfo[0].password.encode(encoding="utf-8", errors="strict")) == userInfo[0].password.encode(encoding="utf-8", errors="strict"):
			return True
		else:
			return (False, "pass")

class WishListManager(models.Manager):
	def create(self, item, id):
		if len(item) < 1:
			return (False, "Please enter a item")
		added_by = User.objects.get(id=id)
		WishList.objects.create(item=item, added_by=added_by)
		return True
	def remove(self, id, user):
		wishlist = WishList.objects.get(id=id)
		user = User.objects.get(id=user)
		wishlist.wished_by.remove(user)
		return True
	def addWish(self, id, user):
		wishlist = WishList.objects.get(id=id)
		user = User.objects.get(id=user)
		wishlist.wished_by.add(user)
		return True
	def delete(self, id):
		WishList.objects.filter(id=id).delete()
		return True

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	date_hired = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()
	objects = models.Manager()

class WishList(models.Model):
	item = models.CharField(max_length=200)
	added_by = models.ForeignKey(User)
	wished_by = models.ManyToManyField(User, related_name='User2')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	wishListManager = WishListManager()
	objects = models.Manager()



