from django.db import models
import re
import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,8}$')
now = datetime.datetime.now()

class UsersManager(models.Manager):
    def basic_validator(self, post):
        errors = {}
        if len(post['f_name']) < 2:
            errors['f_name'] = "First Name requires at least 2 characters"
        if len(post['l_name']) < 2:
            errors['l_name'] = "Last Name requires at least 2 characters"
        # if len(post['email']) < 2:
        #     errors['email'] = "Email requires at least 2 characters"
        # if len(post['password']) < 2:
        #     errors['password'] = "Password requires at least 2 characters"
        if post['confirm'] != post['password']:
            errors['confirm'] = "Passwords do not match"
        if not EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid Email"
        if not PASSWORD_REGEX.match(post['password']):
            errors['password'] = "Must be 4-8 chars, with one uppercase, one lowercase and a number"       
        if Users.objects.filter(email=post['email']):
            errors['email'] = "Email alread Exists"
        return errors 

class TripsManager(models.Manager):
    def basic_validator(self, post):
        errors = {}
        if len(post['destination']) < 3:
            errors['destination'] = "Destination requires at least 3 characters"
        if len(post['start']) < 1:
            errors['start'] = "Start Date Required"
        else:    
            datetime_object = datetime.datetime.strptime(post['start'],'%Y-%m-%d')
            if datetime_object < now:
                errors['start'] = "Start must be in future"
        if len(post['end']) < 1:
            errors['end'] = "End Date Required"
        else:
            datetime_object_end = datetime.datetime.strptime(post['end'],'%Y-%m-%d')
            if datetime_object_end < datetime_object:
                errors['end'] = "End Date must be after Start Date"
        if len(post['plan']) < 1:
            errors['plan'] = "Plan is required"
        return errors 


class Users(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length=2555)
    plan = models.TextField()
    start = models.DateField()
    end  = models.DateField()
    creator = models.ForeignKey(Users, related_name="trips_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(Users, related_name="trip_joined")
    objects = TripsManager()