from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'mamba_index'),
	url(r'^register$', views.register, name = 'mamba_index'),
	url(r'^login$', views.login, name = 'mamba_login'),
	url(r'^logout$', views.logout, name = 'mamba_logout'),
	url(r'^dashboard$', views.dashboard, name = 'mamba_dashboard'),
	url(r'^wish_items/create$', views.create, name = 'mamba_create'),
	url(r'^wish_items/add/(?P<id>\d+)$', views.add, name = 'mamba_add'),
	url(r'^wish_items/addwish/(?P<id>\d+)$', views.addWish, name = 'mamba_addwish'),
	url(r'^wish_items/remove/(?P<id>\d+)$', views.remove, name = 'mamba_remove'),
	url(r'^wish_items/delete/(?P<id>\d+)$', views.delete, name = 'mamba_delete'),
	url(r'^wish_items/(?P<id>\d+)$', views.item, name = 'mamba_item')
]