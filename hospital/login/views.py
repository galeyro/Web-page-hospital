from django.shortcuts import render, HttpResponse

# Create your views here.
'''
# MVC = Model View Controller
# MVT = Model Template View

Aqui a la vista se le llama template y el controllador se llama View
'''

#
def hola_mundo(request):
    return HttpResponse("Hola mundo con Django!!")