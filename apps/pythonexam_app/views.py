# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . models import User, Quote
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def home(request):
    return redirect("/main")
def index(request):
    return render(request, 'pythonexam_app/index.html')
def reg(request):
    user_data={
    "name" : request.POST['name'],
    "alias" : request.POST['alias'],
    "email" : request.POST['email'],
    "birth_date" : request.POST['birth_date'],
    "password" : request.POST['password'],
    "confirm_password" : request.POST['confirm_password']
    }
    result = User.objects.register(user_data)
    if result['errors'] == None:
        request.session['user_alias'] = result['user'].alias
        request.session['user_name'] = result['user'].name
        request.session['user_email'] = result['user'].email
        request.session['user_id'] = result['user'].id
        return redirect("/quotes")
    else:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
def login(request):
    user_data={
    "email" : request.POST['email'],
    "password" : request.POST['password']
    }
    result = User.objects.logger(user_data)
    if result['errors'] == None:
        request.session['user_alias'] = result['user'].alias
        request.session['user_name'] = result['user'].name
        request.session['user_email'] = result['user'].email
        request.session['user_id'] = result['user'].id
        return redirect("/quotes")
    else:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
def quotes(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect("/")
    loginuser = User.objects.get(id= request.session['user_id'])
    context={
    'all_quotes' : Quote.objects.all().exclude(favorite=loginuser),
    'fave_quotes' : Quote.objects.all().filter(favorite=loginuser),
    }
    return render(request, 'pythonexam_app/quotes.html', context)
def addquote(request):
    loginuser = User.objects.get(id= request.session['user_id'])
    quote_data={
    "who" : request.POST['who'],
    "saying" : request.POST['saying'],
    "user_id": loginuser,
    }
    quote_result = Quote.objects.regquote(quote_data)
    if quote_result['errors'] == None:
        return redirect("/quotes")
    else:
        for error in quote_result['errors']:
            messages.add_message(request, messages.ERROR, error)
            return redirect("/quotes")
def addfav(request, Quote_id):
    favuser = User.objects.get(id=request.session['user_id'])
    favequote = Quote.objects.get(id=Quote_id)
    favequote.favorite.add(favuser)
    return redirect('/quotes')
def removefav(request, Quote_id):
    leaveuser = User.objects.get(id=request.session['user_id'])
    leavequote = Quote.objects.get(id=Quote_id)
    leavequote.favorite.remove(leaveuser)
    return redirect('/quotes')
def userpage(request, User_id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect("/")
    userquotes= User.objects.get(id=User_id)
    quoteusers= Quote.objects.filter(user=userquotes)
    userquotesname=User.objects.get(id=User_id)
    context={
    "quoteusers" : quoteusers,
    "userquotesname" : userquotesname,
    }
    return render(request, 'pythonexam_app/user.html', context)
def logout(request):
	request.session.clear()
	return redirect('/main')
