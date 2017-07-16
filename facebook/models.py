from django.db import models
import datetime

# Create your models here.
class User(models.Model):

	user_name = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)
	user_email = models.CharField(max_length=200)

	
	def __str__(self):
		return self.user_name
		
	def __str__(self):
		return self.user_password
		
	def __str__(self):
		return self.user_email
	
	

class User_Options(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	about_bio = models.CharField(max_length=2000)
	about_location = models.CharField(max_length=100)

	
	def __str__(self):
		return self.about_bio
		
	def __str__(self):
		return self.about_location
		
	def __str__(self):
		return self.about_post

		
		
class User_Posts(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	post_made = models.CharField(max_length=10000)
	pub_date = models.DateTimeField('Date Published')
	likes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.post_made
		
		
class User_Photo(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	profile_picture_link = models.CharField(max_length=10000)
	
	def __str__(self):
		return self.profile_picture_link
		

class User_Msg(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	sent_by = models.CharField(max_length=10000)
	msg_content = models.CharField(max_length=10000)
	sent_on = models.DateTimeField('Date Published')
	respond_to = models.IntegerField(default=0)
	
	def __str__(self):
		return self.sent_by
		
	def __str__(self):
		return self.msg_content
		
		
class User_View(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	user_view_count = models.IntegerField(default=0)
	user_view_msg = models.CharField(max_length=10000)
	
	def __str__(self):
		return self.user_view_msg
