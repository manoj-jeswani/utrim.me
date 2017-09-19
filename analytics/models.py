from django.db import models

# Create your models here.
from shortener.models import urlss

class iplocation(models.Model):
	cip=models.CharField(max_length=50,unique=True,null=False)
	ccity=models.CharField(max_length=250,blank=True)
	ccountry=models.CharField(max_length=250)
	clat=models.DecimalField(decimal_places=20,max_digits=40)
	clon=models.DecimalField(decimal_places=20,max_digits=40)
	cstate=models.CharField(max_length=250)

	def __str__(self):
		return "{i}".format(i=self.cip)


class ClickEventManager(models.Manager):
	def create_event(self,instance):
		if isinstance(instance,urlss):
			obj,created=self.get_or_create(urlss_url=instance)
			obj.count +=1
			obj.save()
			return obj.count
		return None
	
	def save_ipdetail(self,instance,ipinstance):
		if isinstance(instance,urlss) and isinstance(ipinstance,iplocation):
			obj,created=self.get_or_create(urlss_url=instance)
			obj.req_ips.add(ipinstance)
			obj.save()
		return None




class ClickEvent(models.Model):
	urlss_url=models.OneToOneField(urlss)
	req_ips=models.ManyToManyField(iplocation)
	count=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	objects=ClickEventManager()

	def __str__(self):
		return "{i}".format(i=self.urlss_url.url)
	

