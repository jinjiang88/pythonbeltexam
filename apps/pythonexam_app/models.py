# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django import forms
import re, bcrypt, string, datetime

class UserManager(models.Manager):

    def register(self, data):
        numCheck = False
        charCheck = False
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        errors = [] #store errors that occur during verification
        if len(data['name']) == 0:
            errors.append("Name may not be blank.")
        elif len(data['name']) < 3:
            errors.append("Name must at least have 2 characters.")
        if not data['name'].isalpha():
            errors.append("Name may only be letters.")
        if len(data['alias']) == 0:
            errors.append("Alias may not be blank.")
        elif len(data['alias']) < 3:
            errors.append("Alias must at least have 2 characters.")
        if not data['alias'].isalpha():
            errors.append("Alias may only be letters.")
        if len(data['email']) < 8:
            errors.append("Email must at least have 8 characters.")
        if not re.match(EMAIL_REGEX, data["email"]):
            errors.append("Email not in valid format.")
        for char in data['password']:
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if numCheck and charCheck:
                break
        if not numCheck or not charCheck:
            errors.append("Your password must include at least one letter and at least one number.")
        if len(data['birth_date']) == 0:
            errors.append("Birth date may not be blank.")
        elif datetime.datetime.strptime(data['birth_date'], '%Y-%m-%d') >= datetime.datetime.now():
            errors.append("You have to be born in the past!")
        if len(data['password']) < 8:
            errors.append("Password must at least have 8 characters.")
        if data['password'] != data['confirm_password']:
            errors.append("Password is not matching confirm password!")

        try:
            User.objects.get(email=data['email'])
            errors.append("You already have an account!")
        except:
            pass
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        if len(errors) == 0:#log in if there are no errors and create profile
            user = User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=data['password'], birth_date= data['birth_date'])
            return{"user" : user, "errors" : None}
        else:
            return{"user" : None, "errors" : errors}
    def logger(self, data):
        errors = []
        try:
            found_user = User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
				errors.append("Incorrect password.")
        except:
			errors.append("Email address not registered.")
        if len(errors) == 0:
            user = User.objects.get(email=data['email'])
            return{"user" : user, "errors" : None}
        else:
            return{"user" : None, "errors" : errors}

class QuoteManager(models.Manager):
    def regquote(self, data):
        errors = []
        if len(data['who']) < 4:
            errors.append("Quoted by must be more than 3 chracters.")
        if len(data['saying']) < 11:
            errors.append("Message must be more than 10 chracters.")
        if len(errors) == 0:
            quote = Quote.objects.create(who=data['who'], saying=data['saying'], user=data['user_id'])
            return{"quote" : quote, "errors" : None}
        else:
            return{"quote" : None, "errors" : errors}

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birth_date = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    who = models.CharField(max_length=255)
    saying = models.CharField(max_length=255)
    favorite = models.ManyToManyField(User, related_name="quote_fav")
    user = models.ForeignKey(User, related_name='quote')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = QuoteManager()
