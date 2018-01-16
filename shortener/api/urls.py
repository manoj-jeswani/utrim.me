from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^mylinks$', User_Link.as_view(), name='my-links'),
	url(r'^shorten$', All_Link_Create.as_view(), name='shorten-link'),
	url(r'^mylinks/edit/(?P<code>[-\w]+)$', User_Link_RUD.as_view(), name='my-links-edit'),
	url(r'^mylinks/analytics/(?P<code>[-\w]+)$', User_Link_Analytics.as_view(), name='my-links-analytics'),

	
]

