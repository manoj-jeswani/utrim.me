from django.db import models

# Create your models here.
from shortener.models import urlss

class ClickEventManager(models.Manager):
	def create_event(self,instance):
		if isinstance(instance,urlss):
			obj,created=self.get_or_create(urlss_url=instance)
			obj.count +=1
			obj.save()
			return obj.count
		return None




class ClickEvent(models.Model):
	urlss_url=models.OneToOneField(urlss)
	count=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	objects=ClickEventManager()

	def __str__(self):
		return "{i}".format(i=self.urlss_url.url)
	