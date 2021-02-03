from django.urls import path

from . import views

app_name = 'eventos'
urlpatterns = [
    path('', views.myLogin, name='myLogin'),
    path('myLogin', views.myLogin, name='myLogin'),
    path('myLogout', views.myLogout, name='myLogout'),
    path('register', views.register, name='register'),
    path('eventList', views.eventList, name='eventList'),
    path('createEvent', views.createEvent, name='createEvent'),
    path('updateEvent/<int:eventId>', views.updateEvent, name='updateEvent'),
    path('deleteEvent/<int:eventId>', views.deleteEvent, name='deleteEvent'),
]
