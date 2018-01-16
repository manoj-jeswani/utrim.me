


from rest_framework import serializers
from shortener.models import urlss,Profiles


class User_Link_Serializer(serializers.ModelSerializer):
	shorturl = serializers.CharField(source='get_short_url', read_only=True)
	created = serializers.CharField(source='timestamp', read_only=True)
	
	class Meta:
		model=urlss
		fields=('url','shorturl','tag','created')

	def create(self, validated_data):
			
		obj=urlss()
		obj.url=validated_data['url']
		obj.tag=validated_data['tag']
		obj.owner='A'
		obj.save()

		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		uobj=Profiles.objects.get(user=user)
		uobj.reg_urls.add(obj)
		uobj.save()


		return obj	




class User_Link_RUD_Serializer(serializers.ModelSerializer):
	created = serializers.CharField(source='timestamp', read_only=True)
	original_url= serializers.CharField(source='url', read_only=True)
	shorturl=serializers.CharField(source='get_short_url', read_only=True)
	
	class Meta:
		model=urlss
		fields=('original_url','shorturl','tag','created')


	#gives functionality to update tag associated to url in user's url bank
	def update(self, instance, validated_data):

		instance.tag = validated_data.get('tag', instance.tag)
		instance.save()
		return instance


class All_Link_Serializer(serializers.ModelSerializer):
	shorturl = serializers.CharField(source='get_short_url', read_only=True)
	created = serializers.CharField(source='timestamp', read_only=True)
	
	class Meta:
		model=urlss
		fields=('url','shorturl','created')

	def create(self, validated_data):
			
		obj=urlss()
		obj.url=validated_data['url']
		obj.save()
		return obj	




class User_Link_Analytics_Serializer(serializers.Serializer):
	total_hit_count = serializers.IntegerField(read_only=True)
	unique_ip_set = serializers.ListField(
	child=serializers.IPAddressField(protocol='both')
	)
	regionwise_unique_hits_percent =serializers.DictField(child=serializers.DecimalField(max_digits=6,decimal_places=2))

#unique_hits: means hits by different ip addresses
#unique_ip_set:unique visitors