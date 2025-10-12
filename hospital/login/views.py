from django.shortcuts import render, HttpResponse

# Create your views here.
'''
# MVC = Model View Controller
# MVT = Model Template View

Aqui a la vista se le llama template y el controllador se llama View
'''

# hola mundo
def hola_mundo(request):
    return HttpResponse("Hola mundo con Django!!")

# index
def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def create_user(request):
    return render(request, 'create_user.html')

def home(request):
    return render(request, 'home.html')

def control_users(request):
    return render(request, 'control_users.html')