from django.shortcuts import reverse, Http404,render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View #to use class based views
from .forms import submitUrlForm
from .models import *
import urllib.parse
from .forms import *
from django.contrib import messages
import urllib.request, json 

from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.auth import views as auth_views
from .helpers import generate_activation_key
from django.core.mail import send_mail
from django.conf import settings
from analytics.models import *
from django.db.models import Count

# for understanding purpose

# def redirectingview(request,*args,**kwargs): #fxn based view
# 	# print(request.user)
# 	# print(request.user.is_authenticated())
	
# 	print(args)
# 	print(kwargs)
	
# 	return HttpResponse("Hello")


# #class based view
# class cbredirectingview(View):
# 	def get(self,request,*args,**kwargs):
# 		print(args)
# 		print(kwargs)

# 		return HttpResponse("hello again")



# def redirectingview(request,shortcode=None,*args,**kwargs): #fxn based view
# 	# print(request.user)
# 	# print(request.user.is_authenticated())
	
# 	print(args)
# 	print(kwargs)
# 	print(shortcode)
	
# 	return HttpResponse("Hello {sc}".format(sc=shortcode))


# #class based view
# class cbredirectingview(View):
# 	def get(self,request,shortcode=None,*args,**kwargs):
# 		print(args)
# 		print(kwargs)
# 		print(shortcode)

# 		return HttpResponse("Hello again {sc}".format(sc=shortcode))



def get_client_ip(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class index_view(View):
	error_msg=""
	
	msg=0
	def get(self,request,*args,**kwargs):
		
		form=submitUrlForm()
		context={
		"form":form,
		
		"error_msg":self.error_msg

		}
		return render(request,"shortener/index.html",context)
	def post(self,request,*args,**kwargs):
		
		obj=""
		share_string=""
		form=submitUrlForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
		got_url=form.cleaned_data.get('url')
		print(got_url)
		if got_url==None:
			self.error_msg=form.errors.get('url')
			form.errors['url']=""
		
		else:
			obj,created=urlss.objects.get_or_create(url=got_url)
			
			if created:
				self.msg=1
			else:
				self.msg=0
			return redirect('/short/%s/%s'%(obj.shortcode,self.msg))
			
			
		if self.error_msg!='':
			self.error_msg='Invalid Url..Verify and try again..'

		form=submitUrlForm()
		
		new_context={
			"form":form,
			"error_msg":self.error_msg

		}


		
		return render(request,"shortener/index.html",new_context)
	



#class based view
class cbredirectingview(View):
	def get(self,request,shortcode=None,*args,**kwargs):
		cip=""
		string=""
		print(shortcode)
		obj=get_object_or_404(urlss,shortcode=shortcode)
		if obj.owner=="A":
			print(ClickEvent.objects.create_event(obj))
			
			cip=get_client_ip(request)
			
			if cip!="":
				ipobj,created=iplocation.objects.get_or_create(cip=cip)
				if created==True:

					string="http://ip-api.com/json/{cip}".format(cip=cip)
					with urllib.request.urlopen(string) as url:
						data=json.loads(url.read().decode())
					if data!={} and "status" in data.keys():
						if data["status"]=="success":
							
							ipobj.cip=cip
							ipobj.ccity=data["city"]
							ipobj.ccountry=data["country"]
							ipobj.clat=data["lat"]
							ipobj.clon=data["lon"]
							ipobj.cstate=data["regionName"]
							ipobj.save()
							ClickEvent.objects.save_ipdetail(obj,ipobj)

				elif created==False:
					ClickEvent.objects.save_ipdetail(obj,ipobj)








		# print(obj.shortcode)
		return HttpResponseRedirect(obj.url)





def register_view(request):
    all_errors=""
    activation_key=""
    if request.user.is_authenticated():
        return redirect('/profile_page/')

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():

            # send email verification now

#             activation_key = generate_activation_key(username=request.POST['username'])

#             subject = "curt.tk Account Verification"

#             message = '''\n
# Please visit the following link to verify your account {}://{}/activate-account/?key={}
#                         '''.format(request.scheme, request.get_host(), activation_key)            

#             error = False

#             if not send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']]):
#                 messages.add_message(request, messages.INFO, 'Unable to send email verification. please Try again')
#                 error = True
#             else:
#                 messages.add_message(request, messages.INFO, 'Account created! Click on the link sent to your email to activate '
#                                                              'the account')
            error=False   #remove error=False line when mail problem removed  
            if not error:
                u = User.objects.create_user(
                       username= request.POST['username'],
                       password= request.POST['password1'],
                      first_name=  request.POST['fname'],
                       last_name= request.POST['lname'],
                        email=request.POST['email'],
                        is_active = 1 #set is_active  to zero when mail problem removed
                )

                pobj = Profiles()
                pobj.activation_key = activation_key
                pobj.user = u
                pobj.save()
                                                       
         
            return redirect('login')
        else:
        	for i in f.errors.keys():
        		messages.error(request, f.errors.get(i))
        		f.errors[i]=""
        


    else:
        f = CustomUserCreationForm()

        

    return render(request, 'shortener/register.html', {'form': f})    




def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Profiles, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'shortener/activated.html')


def login_view(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/profile_page/')
    else:
        return auth_views.login(request, **kwargs)




def analytics_page(request,shortcode=None,country=None):
	if not request.user.is_authenticated():
		return redirect('login')
	speciqset=""
	bol=0
	obj=get_object_or_404(urlss,shortcode=shortcode)
	ipqset=obj.clickevent.req_ips.all()

	cqset=ipqset.annotate(total=Count('ccountry'))
	if country!='all':
		spcqset=obj.clickevent.req_ips.filter(ccountry=country)
		speciqset=spcqset.annotate(rtotal=Count('ccity'))
		bol=1
		context={
			"obj":obj,
			"qset":ipqset,
			"cqset":cqset,
			"speciqset":speciqset,
			"bol":bol


		}
		return render(request, 'shortener/analytics_page.html',context)		

	else:
		bol=0
		context={
			"obj":obj,
			"qset":ipqset,
			"cqset":cqset,
			"speciqset":speciqset,
			"bol":bol

		}
		return render(request, 'shortener/analytics_page.html',context)    


def ubview(request):
	if not request.user.is_authenticated():
		return redirect('/#analytics')
	else:
		return redirect('/profile_page/#urltable')




def short_page(request,shortcode=None,msg=None):
	share_string=""
	added_msg=""
	error_msg=""
	obj=get_object_or_404(urlss,shortcode=shortcode)
	share_string=urllib.parse.quote(obj.get_short_url(), safe='')
	
	if request.method == 'POST' and request.user.is_authenticated():
		form = addtobankForm(request.POST)
		if form.is_valid():
		 	print(form.cleaned_data)
		got_url=form.cleaned_data.get('url')
		got_tag=form.cleaned_data.get('tag')
		
		print(got_url)
		if got_url==None:
		 	error_msg=form.errors.get('url')
		 	form.errors['url']=""
		elif got_tag==None:
		 	error_msg=form.errors.get('tag')
		 	form.errors['tag']=""
		else:
			obj.owner="A"
			obj.tag=got_tag
			obj.save()

			qs=Profiles.objects.all()
			for ob in qs:
				if ob.user.username==request.user.username:
					break
			# pobj=get_object_or_404(Profiles,user=request.user)
			pobj=ob
			pobj.reg_urls.add(obj)
			pobj.save()	
					 	
			added_msg="Url added.."
			print('yes')

		if error_msg!='':
			error_msg='Addition Denied..Invalid Url'
	else:
		form = addtobankForm()
	context={
				"msg":int(msg),
				"share_string":share_string,
				"obj":obj,
				"form":form,
				"error_msg":error_msg,
				"added_msg":added_msg
    		} 	
	return render(request,"shortener/short.html",context)




def profile_page(request):
	if not request.user.is_authenticated():
		return redirect('login')
	# pobj=get_object_or_404(Profiles,user=)
	qs=Profiles.objects.all()
	for ob in qs:
		if ob.user.username==request.user.username:
			break
	pobj=ob

	
	qset=pobj.reg_urls.all()
	context={
		"qset":qset,
		"num":len(qset)
	}
	return render(request, 'shortener/profile_page.html',context)    



def terms_page(request):

	return render(request, 'shortener/terms.html',{})

def privacy_page(request):
	return render(request, 'shortener/privacy.html',{})
def disc_page(request):
	return render(request, 'shortener/disclaimer.html',{})
