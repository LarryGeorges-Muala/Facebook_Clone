from django.conf.urls import url 
from . import views

app_name = 'facebook'

urlpatterns=[

	url(r'^$', views.index, name='index'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^register$', views.signUp, name='signUp'),
	url(r'^profile$', views.profile, name='profile'),
	url(r'^profile/uploaded$', views.validate_upload, name='validate_upload'),
	url(r'^profile/edited$', views.edit_info, name='edit_info'),
	url(r'^profile/posted$', views.make_post, name='make_post'),
	url(r'^profile/liked$', views.like_post, name='like_post'),
	url(r'^profile/deleted$', views.delete_post, name='delete_post'),
	url(r'^view profile$', views.search_user, name='search_user'),
	url(r'^view profile/liked$', views.like_post_other_profile, name='like_post_other_profile'),
	url(r'^view profile/MsgSent$', views.send_msg_other_profile, name='send_msg_other_profile'),
	url(r'^ajax/messages/$', views.messager, name='messager'),
		
]