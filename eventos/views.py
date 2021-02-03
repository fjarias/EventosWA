from datetime import date, datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Get URL del API de eventos
def getBackendEndpoint():
    # Desarrollo
    #return 'http://127.0.0.1:5000/eventos'
    # Deploy
    return 'http://172.24.98.82:5000/eventos'


# Vista de cración de eventos
def createEvent(request):
    if not request.user.is_authenticated:
        return redirect('eventos:myLogin')
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            obj = {
                "nombre": form.cleaned_data['nombre'],
                "categoria": form.cleaned_data['categoria'],
                "lugar": form.cleaned_data['lugar'],
                "direccion": form.cleaned_data['direccion'],
                "fecha_creacion": dt_string,
                "fecha_inicio": str(form.cleaned_data['fecha_inicio']),
                "fecha_fin": str(form.cleaned_data['fecha_fin']),
                "evento_virtual": form.cleaned_data['evento_virtual'],
                "usuario": request.session['app_user']
            }

            requests.post(getBackendEndpoint(), json=obj)
            return redirect('eventos:eventList')
    form = CreateForm()
    return render(request, 'eventos/createEvent.html', {'form': form})


# Vista de actualiación de eventos
def updateEvent(request, eventId):
    if not request.user.is_authenticated:
        return redirect('eventos:myLogin')
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            obj = {
                "nombre": form.cleaned_data['nombre'],
                "categoria": form.cleaned_data['categoria'],
                "lugar": form.cleaned_data['lugar'],
                "direccion": form.cleaned_data['direccion'],
                "fecha_creacion": dt_string,
                "fecha_inicio": str(form.cleaned_data['fecha_inicio']),
                "fecha_fin": str(form.cleaned_data['fecha_fin']),
                "evento_virtual": form.cleaned_data['evento_virtual']
            }
            url = getBackendEndpoint() + '/' + str(eventId)
            requests.put(url, json=obj)
            return redirect('eventos:eventList')
    event = requests.get(getBackendEndpoint() + '/' + str(eventId))
    if event.json()['usuario'] != request.session['app_user']:
        return HttpResponse("Acceso a recurso no permitido")
    form = CreateForm(event.json())
    return render(request, 'eventos/updateEvent.html', {'eventId': eventId, 'form': form})


# Vista de eliminar evento
def deleteEvent(request, eventId):
    if not request.user.is_authenticated:
        return redirect('eventos:myLogin')
    url = getBackendEndpoint() + '/' + str(eventId)
    event = requests.get(url)
    if event.json()['usuario'] != request.session['app_user']:
        return HttpResponse("Acceso a recurso no permitido")
    x = requests.delete(url)
    return redirect('eventos:eventList')


# Vista principal de gestión de eventos
def eventList(request):
    if not request.user.is_authenticated:
        return redirect('eventos:myLogin')
    appUser = request.session['app_user']
    events = requests.get(getBackendEndpoint() + '/' + appUser)
    return render(request, 'eventos/eventList.html', {'app_user': appUser, 'events': events.json()})


# Vista para log in
def myLogin(request):
    msg = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['app_user'] = email
                return redirect('eventos:eventList')
            else:
                msg = "Usuario o contraseña inválida"
    form = RegisterForm()
    return render(request, 'eventos/myLogin.html', {'msg': msg, 'form': form})


# Vista para log out
def myLogout(request):
    if not request.user.is_authenticated:
        return redirect('eventos:myLogin')
    logout(request)
    return HttpResponse("Logout exitoso")


# Vista de registro
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(email, email, password)
            user.save()
        return redirect('eventos:myLogin')
    form = RegisterForm()
    return render(request, 'eventos/register.html', {'form': form})


# Form para registrarse y autenticarse
class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


# Form para crear eventos
class CreateForm(forms.Form):
    CATEGORIAS = (
        ("Conferencia", "Conferencia"),
        ("Seminario", "Seminario"),
        ("Congreso", "Congreso"),
        ("Curso", "Curso"),
    )
    nombre = forms.CharField(max_length=100)
    categoria = forms.ChoiceField(choices=CATEGORIAS)
    lugar = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    fecha_inicio = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    fecha_fin = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    evento_virtual = forms.BooleanField(required=False)
