from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from .utils import code_generator,create_shortcode
from django.conf import settings
from .validators import *

#from settings file get value of SHORTCODE_MAX and if is not present then return 15
SHORTCODE_MAX=getattr(settings,"SHORTCODE_MAX",15)


# Create your models here.
class urlssManager(models.Manager):
	def all(self,*args,**kwargs):
		qs_main=super(urlssManager,self).all(*args,**kwargs)
		qs=qs_main.filter(active=True)
		return qs
	def refresh_shortcodes(self):
		qs=urlss.objects.filter(id__gte=1)
		new_codes=0
		for q in qs:
			q.shortcode=create_shortcode(q)
			print(q.shortcode)
			q.save()
			new_codes+=1
		return "New codes made : {i}".format(i=new_codes)







class urlss(models.Model):
	url=models.CharField(max_length=220,validators=[validate_url])#posing validation here prevents admin to add invalid url
	shortcode=models.CharField(max_length=SHORTCODE_MAX,unique=True,blank=True)
	tag=models.CharField(max_length=15,default='N.A.')
	#blank true means value not complusory in admin, but still necessary in db
	timestamp=models.DateTimeField(auto_now_add=True) #when object was created
	updated=models.DateTimeField(auto_now=True) #everytime the object is edited and saved
	active= models.BooleanField(default=True)	
	owner=models.CharField(max_length=255, default="NA")
	
	objects=urlssManager()

	#below save def overrides inherited class's save method which used to be called by 
	#default-now click save from admin: firstly this below save executes and modifies shortcode
	# and then it calls inherited save and saves into db
	def save(self,*args,**kwargs):
		if self.shortcode is None or self.shortcode=="":
			self.shortcode=create_shortcode(self)
		super(urlss,self).save(*args,**kwargs)

	

	#what we see in admin site as object's name comes from here ... we can also give self.pk
	def __str__(self):
		return str(self.url)

	def get_short_url(self):
		return "http://165.227.181.182/{shortcode}".format(shortcode=self.shortcode)

	def get_absolute_url(self):
		return reverse("analytics_pg",kwargs={"shortcode":self.shortcode})



class Profiles(models.Model):
        
    ## required to associate Profiles model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True)
    reg_urls=models.ManyToManyField(urlss)
    ## additional fields
    phone = models.IntegerField(blank=True, default=1)    
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
    	return self.user.username

    # def get_absolute_url(self):
    #     return reverse('post_by_author', args=[self.user.username])
