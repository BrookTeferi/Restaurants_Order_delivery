from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
 
	fname = models.CharField(max_length=100,null=True)
	lname = models.CharField(max_length=100,null=True)
	address = models.CharField(max_length=100, null=True)
	contact = models.CharField(max_length=100,null =True)
	email=models.EmailField(max_length=100,null=True)
	profile_img = models.ImageField(upload_to='Profile_images',default='default.png')
 
	def __str__(self):
		return self.user.username    #i use this function because i dont use null =True in user -everytime i need this
	
	
	class Meta:
		verbose_name_plural ='Profile'
		db_table = 'tbl_profile'

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
  
  

		
		
	
	
	@receiver(post_save, sender = User)
	def update_profile(sender,instance,created,*args,**kwargs):
		if created:
			Profile.objects.create(user=instance)
			instance.profile.save()
			
			
			
			

