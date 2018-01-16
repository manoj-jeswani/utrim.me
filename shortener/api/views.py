from rest_framework import generics
from rest_framework import permissions
from shortener.models import Profiles
from .serializers import User_Link_Serializer,All_Link_Serializer,User_Link_RUD_Serializer,User_Link_Analytics_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404,Http404
from shortener.models import urlss


class User_Link(generics.ListCreateAPIView):
   
    serializer_class = User_Link_Serializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
       
        user = self.request.user
        uobj=Profiles.objects.get(user=user)
        return uobj.reg_urls.all()




class All_Link_Create(generics.CreateAPIView):
   
    serializer_class = All_Link_Serializer



class User_Link_RUD(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = User_Link_RUD_Serializer
	permission_classes = (permissions.IsAuthenticated,)
	lookup_field='shortcode'
	lookup_url_kwarg="code"
	
	def get_queryset(self):

		user = self.request.user
		uobj=Profiles.objects.get(user=user)
		return uobj.reg_urls.all()
	
	#removes that url from user's url bank....but url remains stored in db bcoz it may have also been shortened and being used by other users
	#only associated tag is changed to N.A.	
	def perform_destroy(self, instance):
		user = self.request.user
		uobj=Profiles.objects.get(user=user)
		uobj.reg_urls.remove(instance)
		uobj.save()
		instance.tag='N.A.'
		instance.save()
		return instance


class User_Link_Analytics(APIView):
	permission_classes = (permissions.IsAuthenticated,)	

	def get(self, request,code,format=None):

		user = request.user
		obj=get_object_or_404(urlss,shortcode=code)
		uobj=Profiles.objects.get(user=user)
		if obj in uobj.reg_urls.all():

			hit_count=0
			if obj.clickevent.count is not None:
				hit_count=int(obj.clickevent.count)

			ipqset=obj.clickevent.req_ips.all()
			ip_set=[]
			for ob in ipqset:
				ip_set.append(ob.cip)
			cnt=len(ip_set)
		
			d={}
			for pp in ipqset:
				if pp.ccountry in d:
					d[pp.ccountry]=d[pp.ccountry]+1
				else:
					d[pp.ccountry]=1
			
			for i in d.keys():
				d[i]=(d[i]/cnt)*100

			serializer=User_Link_Analytics_Serializer({"total_hit_count":hit_count,"unique_ip_set":ip_set,"regionwise_unique_hits_percent":d})	
			
			return Response(serializer.data)	
		else:
			return Response({'error-msg':'Permission Denied'})	



