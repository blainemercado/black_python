from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse

import re

# Create your views here.
def index(request):
	return render(request, 'mamba/index.html')

def register(request):
	valid = User.userManager.validate(request.POST['name'], request.POST['username'], request.POST['pass1'], request.POST['pass2'], request.POST['date_hired'])
	if valid[0]==True:
		request.session['username'] = valid[1].username
		request.session['id'] = valid[1].id
		return redirect('/dashboard')
	else:
		messages.info(request, valid[1])
		return redirect('/')

def login(request):
	if User.userManager.login(request.POST['username'], request.POST['pass1']) == True:
		user = User.objects.filter(username=request.POST['username'])
		request.session['username'] = user[0].username
		request.session['id'] = user[0].id
		return redirect('/dashboard')
	else:
		messages.warning(request, 'Username and Password do not match')
		return redirect('/')

def logout(request):
	del request.session['id']
	del request.session['username']
	return redirect('/')

def dashboard(request):
	if 'id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['id'])
	context = {
		"mywish": WishList.objects.filter(added_by=user).order_by('added_by'),
		"mywishes": WishList.objects.filter(wished_by=user).order_by('added_by'),
		"otherwish": WishList.objects.exclude(added_by=user).exclude(wished_by=user).order_by('added_by')
	}
	return render(request, 'mamba/dashboard.html', context)

def create(request):
	if 'id' not in request.session:
		return redirect('/')
	return render(request, 'mamba/create.html')

def add(request, id):
	if request.method != 'POST':
		return redirect('/')
	item = request.POST['item']
	added = WishList.wishListManager.create(item, id)
	if added == True:
		return redirect(reverse('mamba_dashboard'))
	return redirect(reverse('mamba_create'))

def addWish(request, id):
	WishList.wishListManager.addWish(id, request.session['id'])
	return redirect(reverse('mamba_dashboard'))

def remove(request, id):
	WishList.wishListManager.remove(id, request.session['id'])
	return redirect(reverse('mamba_dashboard'))

def delete(request, id):
	WishList.wishListManager.delete(id)
	return redirect(reverse('mamba_dashboard'))

def item(request, id):
	if 'id' not in request.session:
		return redirect('/')
	context = {
	 "item": WishList.objects.filter(id=id)
	}
	return render(request, 'mamba/item.html', context)


