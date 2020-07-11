from django.db import models
 
# Create your models here.
class Blogpost(models.Model):
	post_id  = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50)	
	head0 =  models.CharField(max_length=500)
	chead0 =  models.CharField(max_length=5000, default="")
	head1 =  models.CharField(max_length=500)
	chead1 =  models.CharField(max_length=5000, default="")
	head2 =  models.CharField(max_length=500)
	chead2 =  models.CharField(max_length=5000, default="")
	pub_date = models.DateField()
	

	thumbnail = models.ImageField(upload_to='blog/images', default="")

	def __str__(self):
		return self.title

class Owner(models.Model):
	# ...
	name = models.CharField(max_length=255, default='')
	def __str__(self):
		return self.title
	


class Car(object):
	name= models.CharField(max_length=255)
	owner = models.OneToOneField(Owner,
		on_delete = models.CASCADE,
		related_name = 'car'
		)
	def __str__(self):
		return self.title
		
			
						