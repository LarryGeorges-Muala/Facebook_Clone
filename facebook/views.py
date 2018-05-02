from django.shortcuts import render, get_object_or_404
from facebook.models import User, Contact, Conversation
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.urls import reverse


def create_welcome_message(new_user):
	master, master_status = User.objects.get_or_create(user_name="Larry Georges", user_email="host@test.com", user_password="12345")
	init_contact, contact_status = Contact.objects.get_or_create(user_reference=new_user, contact_id=master.id, contact_name=master.user_name, contact_email=master.user_email)
	init_chat, chat_status = Conversation.objects.get_or_create(contact_reference=init_contact, contact_id=init_contact.id, contact_email=init_contact.contact_email, contact_name=init_contact.contact_name, msg_content='Welcome to the FaceBook Clone <br />♦ Have a pleasant experience ☻ ♦')

def check_for_unread_messages(verified_user):
	if verified_user.contact_set.all():
		for contact in verified_user.contact_set.all():
			if contact.conversation_set.all():
				unread_status = contact.conversation_set.filter(has_been_read=False)
				if unread_status:
					return True, contact.id
	return False, ''

def check_logins_and_signups_status(request):
	statuses = {'signup_status': '', 'login_status': ''}
	if request.session.has_key('new_user'):
		#skip to profile
		#return HttpResponseRedirect(reverse('facebook:profile'))
		pass
	if request.session.has_key('sign_up_error'):
		statuses['signup_status'] = ' Account Already Existent. <br>Please Log in or Use a Different Email Address '
		del request.session['sign_up_error']
	if request.session.has_key('sign_up_existent'):
		statuses['signup_status'] = ' Account Already Existent. <br>Please Log in or Use a Different Email Address '
		del request.session['sign_up_existent']
	if request.session.has_key('login_invalid'):
		statuses['login_status'] = ' Invalid Details. Please Try Again '
		del request.session['login_invalid']
	if request.session.has_key('login_non_existent'):
		statuses['login_status'] = ' Details Non Existent. Please Create An Account '
		del request.session['login_non_existent']
	return statuses


def index(request):
	return render(request, 'facebook/index.html', context={'statuses': check_logins_and_signups_status(request)})

def logout(request):
	if request.session.has_key('new_user'):
		del request.session['new_user']
	return HttpResponseRedirect(reverse('facebook:index'))


def check_if_user_is_authed(request):
	##Logging in with cookies
	new_user = ''
	if request.session.has_key('new_user'):
		try:
			new_user = User.objects.get(id=request.session['new_user'])
		except KeyError:
			return HttpResponseRedirect(reverse('facebook:index'))
	return new_user

def log_profile_visited(request):
	##Logging in with cookies
	visit = ''
	if request.session.has_key('profile_visited'):
		try:
			visit = User.objects.get(id=request.session['profile_visited'])
		except KeyError:
			return HttpResponseRedirect(reverse('facebook:profile'))
	return visit

def check_if_user_is_logged_in(request):
	logged_in = check_if_user_is_authed(request)
	if logged_in:
		return HttpResponseRedirect(reverse('facebook:profile'))
	return HttpResponseRedirect(reverse('facebook:index'))


def signUp(request):
	
	new_user = check_if_user_is_authed(request)

	if request.method == 'POST':
		captured_user_name = request.POST.get('userName', None)
		captured_user_email = request.POST.get('userEmail', None)
		captured_user_password = request.POST.get('userPassword', None)
		
		try:
			fetching_user = User.objects.get(user_email=captured_user_email)
			request.session['sign_up_error'] = True
			return HttpResponseRedirect(reverse('facebook:index'))
			
		except User.MultipleObjectsReturned:
			request.session['sign_up_existent'] = True
			return HttpResponseRedirect(reverse('facebook:index'))
			
		except User.DoesNotExist:
			#saving to database
			new_user = User(user_name=captured_user_name, user_email=captured_user_email, user_password=captured_user_password)
			new_user.save()
			request.session['new_user'] = new_user.id
			return HttpResponseRedirect(reverse('facebook:signUp'))

	context={
		'new_user': new_user,
	}
	return render(request, 'facebook/signUp.html', context)
	
	
def profile(request):
	
	verified_user = check_if_user_is_authed(request)

	if request.method == 'POST':
		captured_user_email = request.POST.get('checkUserEmail', None)
		captured_user_password = request.POST.get('checkUserPassword', None)
		
		try:
			fetched_user = User.objects.get(user_email=captured_user_email)
			
			if fetched_user.user_email == captured_user_email and fetched_user.user_password == captured_user_password:
				create_welcome_message(fetched_user)
				return HttpResponseRedirect(reverse('facebook:profile'))		
				
			else:
				request.session['login_invalid'] = True
				return HttpResponseRedirect(reverse('facebook:index'))
				
		except User.DoesNotExist:
			request.session['login_non_existent'] = True
			return HttpResponseRedirect(reverse('facebook:index'))

	has_unread_messages, unread_contact_id = check_for_unread_messages(verified_user)

	context={
		'verified_user': verified_user,
		'all_users': User.objects.exclude(id=verified_user.id),
		'has_unread_messages': has_unread_messages,
		'unread_contact_id': unread_contact_id
	}
	return render(request, 'facebook/profile.html', context)
	
	
def messager(request):
	
	change_status = request.GET.get('change_status', None)
	change_item = request.GET.get('change_item', None)
	message_item = request.GET.get('message_item', None)

	if change_status == 'read':
		try:
			contact_from_msg = Contact.objects.get(id=str(change_item))
			filtered_tread = contact_from_msg.conversation_set.filter(has_been_read=False)
			if filtered_tread:
				for msg in filtered_tread:
					msg.has_been_read = True
					msg.save()
		except Exception as error:
			print(error)
		''' Real time update help on models needed here '''
		circle_user = check_if_user_is_authed(request)
		circle_user = circle_user.generate_chat_thread()
		''' End Real time update help needed '''
		data = {
			'is_taken': True,
			'marked_read': True,
			'change_item': change_item
		}
		return JsonResponse(data)

	if change_status == 'response':
		try:
			contact_from_msg = Contact.objects.get(id=str(change_item))
			Conversation.objects.create(contact_reference=contact_from_msg, contact_id=contact_from_msg.id, contact_email=contact_from_msg.contact_email, contact_name=contact_from_msg.contact_name, msg_content=message_item, has_been_read=True)
		except Exception as error:
			print(error)

		data = {
			'is_taken': True,
			'new_response': True,
			'change_item': change_item,
			'message_item': message_item
		}
		return JsonResponse(data)

	data = {
		'is_taken': False
	}
	return JsonResponse(data)


def edit_info(request):

	if request.method == 'POST':		
		verified_user = check_if_user_is_authed(request)
		captured_user_about = request.POST.get('textAreaAbout', None)
		captured_user_location = request.POST.get('inputLocation', None)
		
		#cleaning database
		verified_user.user_options_set.all().delete()
		#saving to database
		verified_user.user_options_set.create(about_bio=captured_user_about, about_location=captured_user_location)
			
	return HttpResponseRedirect(reverse('facebook:profile'))



def make_post(request):

	if request.method == 'POST':	
		verified_user = check_if_user_is_authed(request)
		captured_user_post = request.POST.get('textAreaPost', None)

		#saving to database
		verified_user.user_posts_set.create(post_made=captured_user_post, pub_date=datetime.datetime.now(), likes=0)
		
	return HttpResponseRedirect(reverse('facebook:profile'))	

	
def like_post(request):

	if request.method == 'POST':		
		verified_user = check_if_user_is_authed(request)
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		#finding post in database
		selected_post = verified_user.user_posts_set.get(id=captured_user_post_id)
		selected_post.likes += 1
		selected_post.save()
		
	return HttpResponseRedirect(reverse('facebook:profile'))
	

def delete_post(request):

	if request.method == 'POST':	
		verified_user = check_if_user_is_authed(request)
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		#finding post in database
		selected_post = verified_user.user_posts_set.get(id=captured_user_post_id)
		selected_post.delete()
		
	return HttpResponseRedirect(reverse('facebook:profile'))

	
def search_user(request):

	verified_user = check_if_user_is_authed(request)
	
	captured_user_profile = request.GET.get('profileSelected', None)
	
	#finding user in database
	selected_user_profile = ''
	if captured_user_profile:
		try:
			selected_user_profile = User.objects.filter(user_name=captured_user_profile).first()
			request.session['profile_visited'] = selected_user_profile.id 
		except Exception as error:
			print(error)
			return HttpResponseRedirect(reverse('facebook:profile'))
	else:
		selected_user_profile = log_profile_visited(request)
	
	#fetching in database
	all_users = User.objects.exclude(id=verified_user.id)

	context={
		'verified_user': verified_user,
		'selected_user_profile': selected_user_profile,
		'all_users': all_users,
	}
	return render(request, 'facebook/view_other_profile.html', context)
	
	
	
	
def like_post_other_profile(request):

	if request.method == 'POST':	
		verified_user = check_if_user_is_authed(request)
		captured_user_post_id = request.POST.get('checkPostID', None)
		
		#finding post in database
		selected_user_profile = log_profile_visited(request)
		
		#finding post in database
		selected_post = selected_user_profile.user_posts_set.get(id=captured_user_post_id)
		selected_post.likes += 1
		selected_post.save()
		
	return HttpResponseRedirect(reverse('facebook:search_user'))


def send_msg_other_profile(request):

	if request.method == 'POST':	
		verified_user = check_if_user_is_authed(request)
		captured_msg = request.POST.get('textAreaSendMsg', None)
		
		#finding receiver in database
		selected_user_profile = log_profile_visited(request)
		
		#saving to database
		init_contact, contact_status = Contact.objects.get_or_create(user_reference=selected_user_profile, contact_id=verified_user.id, contact_name=verified_user.user_name, contact_email=verified_user.user_email)
		Conversation.objects.create(contact_reference=init_contact, contact_id=init_contact.id, contact_email=init_contact.contact_email, contact_name=init_contact.contact_name, msg_content=captured_msg, has_been_read=False)

	return HttpResponseRedirect(reverse('facebook:search_user'))
	

def validate_upload(request):
	
	if request.method == 'POST' and request.FILES['myfile']:		
		verified_user = check_if_user_is_authed(request)
		
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		#fs = FileSystemStorage(location='/media/photos')
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		
		#cleaning database
		verified_user.user_photo_set.all().delete()
		
		#saving to database
		verified_user.user_photo_set.create(profile_picture_link=uploaded_file_url)
			
	return check_if_user_is_logged_in(request)
