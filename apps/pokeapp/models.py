from __future__ import unicode_literals
from django.db import models
import re
from  datetime import *
import bcrypt
# password_regex = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class RegManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        count = User.objects.filter(email=postData["email"]).count()
        if count > 0:
            errors["email"] = "Email already registered"
        if len(postData["name"]) < 3:
            errors["name"] = "Name should be more than 3 characters"
        if len(postData["alias"]) < 3:
            errors["alias"] = "Alias should be more than 3 characters"
        if len(postData["email"]) < 1:
            errors["email"] = "Email field can not be empty"
        elif not email_regex.match(postData["email"]):  
            errors["email"] = "Invalid email address"
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be more thatn 8 characters"
        # elif not password_regex.match(postData["password"]):
        #     errors["password"] = "Invalid password"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Password confirmation does not match"
        if len(postData["dob"]) < 1:
            errors["dob"] = "Date of Birth field cannot be empty"
        if postData["dob"] > datetime.now().strftime("%Y-%m-%d"):
            errors["dob"] = "Date of Birth can not be in the future"   
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData["email"]) < 3:
            errors["email"] = "Email should be more than 3 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be longer than 8 characters"
        check = User.objects.filter(email=postData["email"])
        if len(check) == 0:
            errors["email"] = "Must enter an email address"
            return errors
        if not bcrypt.checkpw(postData["password"].encode(), check[0].password.encode()):
            errors["password"] = "Password doesn't match"
        return errors





class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    pokes = models.IntegerField(default=0)
    pokers = models.ManyToManyField("self", related_name="who_poked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()
