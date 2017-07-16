#Site Name: Facebook Clone
#Python Version 3.5
#Django Version: 1.10.5
#Developper: Larry Georges Muala

from django.shortcuts import render, get_object_or_404
from facebook.models import User
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse



def index(request):

	message = "facebook Clone"
	
	all_users =''
	
	try:
		all_users = User.objects.all()		
		#User.objects.filter(user_email="guest@email.com").delete()

	except:
		all_users = 'No Active User'
	
	
	context={
		'message': message,
		'all_users': all_users,
	}

	return render(request, 'facebook/index.html', context)


	
def signUp(request):
			
	message = "Congratulations - Account Successfully Created"
	
	##Logging in with cookies
	if request.session.has_key('new_user'):
		try:
			new_user = User.objects.get(id=request.session['new_user'])
		except KeyError:
			pass

	if request.method == 'POST':
		captured_user_name = request.POST.get('userName', None)
		captured_user_email = request.POST.get('userEmail', None)
		captured_user_password = request.POST.get('userPassword', None)
		
		try:
			fetching_user = User.objects.get(user_email=captured_user_email)
			signup_status = 'Account Already Existent. Please Log in or Use a Different Email Address'
			return render(request, 'facebook/signUp_invalid.html', context={'signup_status': signup_status})
			
		except User.MultipleObjectsReturned:	
			signup_status = 'Account Already Existent. Please Log in or Use a Different Email Address'
			return render(request, 'facebook/signUp_invalid.html', context={'signup_status': signup_status})
			
		except User.DoesNotExist:
			#saving to database
			new_user = User(user_name=captured_user_name, user_email=captured_user_email, user_password=captured_user_password)
			new_user.save()
			new_user.user_view_set.create(user_view_count=0, user_view_msg = "text-danger")
			request.session['new_user'] = new_user.id

			return HttpResponseRedirect(reverse('facebook:signUp'))

	
	context={
		'message': message,
		'new_user': new_user,
	}

	return render(request, 'facebook/signUp.html', context)
	
	

	
def profile(request):
			
	message = "Facebook Profile"
	
	##Logging in with cookies
	if request.session.has_key('new_user'):
		try:
			verified_user = User.objects.get(id=request.session['new_user'])
		except KeyError:
			pass

	#checking entry in database
	all_users = []
	all_users = User.objects.all()
	

	if request.method == 'POST':
		captured_user_email = request.POST.get('checkUserEmail', None)
		captured_user_password = request.POST.get('checkUserPassword', None)
		
		#using Get to check entries
		fetching_user = ''
		
		try:
			fetching_user = User.objects.get(user_email=captured_user_email)
			
			if fetching_user.user_email == captured_user_email and fetching_user.user_password == captured_user_password:
				verified_user = fetching_user
				
				##Resetting msg checker
				#verified_user.user_view_set.all().delete()
				#verified_user.user_view_set.create(user_view_count=0, user_view_msg = "text-danger")
				
				for data in verified_user.user_view_set.all():
					
					data.user_view_count += 1
					data.save()

				return HttpResponseRedirect(reverse('facebook:profile'))		
				
			else:
				login_status = 'Invalid Details. Please Try Again'
				return render(request, 'facebook/logIn_invalid.html', context={'login_status': login_status})
				
		except User.DoesNotExist:
			login_status = 'Invalid Details. Please Try Again'
			return render(request, 'facebook/logIn_invalid.html', context={'login_status': login_status})

	
	context={
		'message': message,
		'verified_user': verified_user,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)
	
	

def edit_info(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_about = request.POST.get('textAreaAbout', None)
		captured_user_location = request.POST.get('inputLocation', None)
		
		#cleaning database
		verified_user.user_options_set.all().delete()
		
		#saving to database
		verified_user.user_options_set.create(about_bio=captured_user_about, about_location=captured_user_location)
		
		#values for future edit_info
		edit_about = ''
		edit_location = ''
		
		all_users = []
		all_users = User.objects.all()
		
		for data in verified_user.user_options_set.all():
			edit_about = data.about_bio
			edit_location = data.about_location
			
		#updating checker
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
			
	return HttpResponseRedirect(reverse('facebook:profile'))
"""	
	context={
		'verified_user': verified_user,
		'edit_about': edit_about,
		'edit_location': edit_location,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)
"""



def make_post(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_post = request.POST.get('textAreaPost', None)
		
		#saving to database
		verified_user.user_posts_set.create(post_made=captured_user_post, pub_date=datetime.datetime.now(), likes=0)
		
		all_users = []
		all_users = User.objects.all()
		
		#updating checker
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
		
	return HttpResponseRedirect(reverse('facebook:profile'))
"""	
	context={
		'verified_user': verified_user,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)	
"""
		
	

	
def like_post(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		#finding post in database
		selected_post = verified_user.user_posts_set.get(id=captured_user_post_id)
		selected_post.likes += 1
		selected_post.save()
		
		all_users = []
		all_users = User.objects.all()
		
		#updating checker
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
		
	return HttpResponseRedirect(reverse('facebook:profile'))
"""	
	context={
		'verified_user': verified_user,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)
"""
	
	

def delete_post(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		#finding post in database
		selected_post = verified_user.user_posts_set.get(id=captured_user_post_id)
		selected_post.delete()
		
		all_users = []
		all_users = User.objects.all()
		
		#updating checker
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
		
	return HttpResponseRedirect(reverse('facebook:profile'))
"""		
	context={
		'verified_user': verified_user,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)
"""


	
def search_user(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_profile = request.POST.get('profileSelected', None)
		
		#finding post in database
		selected_user_profile = User.objects.get(user_name=captured_user_profile)
		
		#fetching in database
		all_users = []
		all_users = User.objects.all()
		
		
	context={
		'verified_user': verified_user,
		'selected_user_profile': selected_user_profile,
		'all_users': all_users,
	}

	return render(request, 'facebook/view_other_profile.html', context)
	
	
	
	
def like_post_other_profile(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		captured_user_profile = request.POST.get('profileSelected', None)
		
		#finding post in database
		selected_user_profile = User.objects.get(id=captured_user_profile)
		
		#finding post in database
		selected_post = selected_user_profile.user_posts_set.get(id=captured_user_post_id)
		selected_post.likes += 1
		selected_post.save()
		
		all_users = []
		all_users = User.objects.all()
		
		
	context={
		'verified_user': verified_user,
		'selected_user_profile': selected_user_profile,
		'all_users': all_users,
	}

	return render(request, 'facebook/view_other_profile.html', context)	
	


def send_msg(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_msg = request.POST.get('textAreaMsg', None)
		
		captured_user_profile = request.POST.get('checkUserIDmsgReceiver', None)
		
		#finding receiver in database
		selected_user_profile = User.objects.get(id=captured_user_profile)
		
		#saving to database
		selected_user_profile.user_msg_set.create(sent_by=verified_user.user_name, msg_content=captured_msg, sent_on=datetime.datetime.now(), respond_to=verified_user.id)
		
		#updating checker
		for data in selected_user_profile.user_view_set.all():
			data.user_view_count = 0
			data.save()
			
		#updating sender
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
		
		all_users = []
		all_users = User.objects.all()
		
	return HttpResponseRedirect(reverse('facebook:profile'))
"""
	context={
		'verified_user': verified_user,
		'all_users': all_users,
	}

	return render(request, 'facebook/profile.html', context)
"""
	

	
def send_msg_other_profile(request):

	if request.method == 'POST':
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		captured_msg = request.POST.get('textAreaSendMsg', None)
		
		captured_user_profile = request.POST.get('checkUserIDmsgReceiver', None)
		
		#finding receiver in database
		selected_user_profile = User.objects.get(id=captured_user_profile)
		
		#saving to database
		selected_user_profile.user_msg_set.create(sent_by=verified_user.user_name, msg_content=captured_msg, sent_on=datetime.datetime.now(), respond_to=verified_user.id)
		
		#updating checker
		for data in selected_user_profile.user_view_set.all():
			data.user_view_count = 0
			data.save()
		
		all_users = []
		all_users = User.objects.all()
		
		
	context={
		'verified_user': verified_user,
		'selected_user_profile': selected_user_profile,
		'all_users': all_users,
	}

	return render(request, 'facebook/view_other_profile.html', context)
	
	

	
def validate_upload(request):
	uploaded_file_url = ''
	all_users = []
	all_users = User.objects.all()
	
	if request.method == 'POST' and request.FILES['myfile']:
		captured_user_email = request.POST.get('checkUserEmail', None)
		captured_user_password = request.POST.get('checkUserPassword', None)
		captured_user_id = request.POST.get('checkUserID', None)		
		verified_user = User.objects.get(id=captured_user_id)
		
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		#fs = FileSystemStorage(location='/media/photos')
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		
		#cleaning database
		verified_user.user_photo_set.all().delete()
		
		#saving to database
		verified_user.user_photo_set.create(profile_picture_link=uploaded_file_url)
		
		#updating checker
		for data in verified_user.user_view_set.all():
			data.user_view_count = 2
			data.save()
			
		
	context={
		'verified_user': verified_user,
		'all_users': all_users,
		'uploaded_file_url': uploaded_file_url,
	}

	return render(request, 'facebook/profile.html', context)