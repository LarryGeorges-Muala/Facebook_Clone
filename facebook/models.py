from django.db import models
import datetime

class User(models.Model):

	user_name = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)
	user_email = models.CharField(max_length=200)

	def generate_chat_thread(self):
		counter = 0
		if self.contact_set.all():
			for contact in self.contact_set.all():
				if contact.conversation_set.all():
					print()
					print(contact.conversation_set.all().count())
					counter += contact.conversation_set.all().count()
		return counter

	def generate_contact_thread(self):
		return self.contact_set.all()

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


class Contact(models.Model):

	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	contact_id = models.IntegerField(default=0)
	contact_name = models.CharField(max_length=10000)
	contact_email = models.CharField(max_length=10000)
		
	def __str__(self):
		return self.contact_id

	def __str__(self):
		return self.contact_name
		
	def __str__(self):
		return self.contact_email


class Conversation(models.Model):
		
	contact_reference = models.ForeignKey(Contact, on_delete=models.CASCADE)
	contact_id = models.IntegerField(default=0)
	contact_name = models.CharField(max_length=10000)
	contact_email = models.CharField(max_length=10000)
	msg_content = models.CharField(default='', max_length=10000)
	sent_on = models.DateTimeField('Date Published', default=datetime.datetime.now)
	has_been_read = models.BooleanField(default=False, blank=True)
	
	def __str__(self):
		return self.contact_name
		
	def __str__(self):
		return self.msg_content
