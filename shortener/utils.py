import string
import random
from django.conf import settings


SHORTCODE_MIN=getattr(settings,"SHORTCODE_MIN",6)



#default argument chars is assigned all lowercase alphabets and digits 
def code_generator(size=SHORTCODE_MIN,chars=string.ascii_lowercase + string.digits):
	new_code=''
	for _ in range(size): #this line runs for loop size number of times
		new_code+=random.choice(chars) #chooses and adds a char to new_code in each iteration
	return new_code #of len size


def create_shortcode(instance,size=SHORTCODE_MIN):
	new_code=code_generator(size=size)
	print(instance)
	print(instance.__class__)
	print(instance.__class__.__name__)
	cur_class=instance.__class__
	qs_bool=cur_class.objects.filter(shortcode=new_code).exists()
	#qs_bool is true if returned queryset length is >0  else false
	if qs_bool:
		return create_shortcode(size=size)
	return new_code

	