from __future__ import unicode_literals
import re, bcrypt
from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class WishListManager(models.Manager):
    def register(self, postData):
        errors = []
        if not len(postData['first_name']) >= 2:
            errors.append('First name must be at least 2 characters!')
        if not len(postData['last_name']) >= 2:#soory, my last name just Du, so...
            errors.append('Last name must be at least 2 characters!')
        if not len(postData['email']):
            errors.append('Email must be there!')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Must have a valid email')
        if not len(postData['password']) > 8:
            errors.append('Password must be at least 8 characters long!')
        if not postData['password'] == postData['confirm_password']:
            errors.append('Passwords must match!')

        user = self.filter(email = postData['email'])

        if user:
            errors.append('Email already exists!')

        modelResponse = {}
        #if failed validations, seend response to views.py
        if errors:
            modelResponse['status'] = False
            modelResponse['errors'] = errors
        #passed validations, save user
        else:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = postData['password'])

            modelResponse['status'] = True
            modelResponse['user'] = user

        return modelResponse

    def login(self, postData):
        errors = []
        user = self.filter(email = postData['email'])
        # check to see is in db
        modelResponse = {}
        if user[0]:
            # check for passwords
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors.append('Invalid email/password combination!')
            # success login
            else:
                modelResponse['status'] = True
                modelResponse['user_id'] = user[0].id
        else:
            errors.append('Invalid email')

        if errors:
            modelResponse['status'] = False
            modelResponse['errors'] = errors

        return modelResponse

    def addWish(self, postData):
        errors = []
        if not len(postData['wish']) >= 2:
            errors.append('Wish must be at least 2 characters!')
        else:
            self.create(user_id = postData['user_id'], wish = postData['wish'])

    def delWish(self, postData):
        self.delete(id = postData['id'])

    def mvWish(self, postData):
        self.update(id = postData['id'] ,wish=postData['wish'])

    def showWish(self, postData):
        self.select(id = postData['id'])

class User(models.Model):
      first_name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      password = models.CharField(max_length=100)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      objects = WishListManager()

class Wish(models.Model):
      # Notice the association made with ForeignKey for a one-to-many relationship
      user_id = models.ForeignKey(User)
      title = models.CharField(max_length=255)
      wish = models.TextField(max_length=1000)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      objects = WishListManager()
