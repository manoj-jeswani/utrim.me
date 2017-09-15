from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

	url(r'^register/$', register_view, name='register'),
	
	url(r'^login/$', login_view, {'template_name': 'shortener/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'shortener/logout.html'}, name='logout'),
    url(r'^profile_page/$', profile_page, name='profile_page'),
    url(r'^ubank/$',ubview, name='ubank_page'),


	url(r'^(?P<shortcode>[-\w]+)$',cbredirectingview.as_view()),
	url(r'^$',index_view.as_view()),
	url(r'^activate-account/$', activate_account, name='activate'),
	url(r'^short/(?P<shortcode>[-\w]+)/(?P<msg>\d+)$',short_page,name='short_pg'),
	url(r'^analytics/(?P<shortcode>[-\w]+)$',analytics_page,name='analytics_pg'),
	
	# # url(r'a/(?P<shortcode>[\w-]+)/$',redirectingview),


]

