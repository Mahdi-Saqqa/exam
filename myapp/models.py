from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        if not postData.get('fname'):
            errors['first_name'] = 'First name is required.'
        if not postData.get('lname'):
            errors['last_name'] = 'Last name is required.'
        if not postData.get('email'):
            errors['email'] = 'Email is required.'
        if not postData.get('password'):
            errors['password'] = 'Password is required.'
        if len(postData['fname']) < 2:
            errors['first_name1'] = 'First name should be at least 2 char.'
        if len(postData['lname']) < 2:
            errors['last_name1'] = 'First name should be at least 2 char.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = "Invalid Email address!"
        if len(postData['password']) < 8:
            errors['pass1'] = "passwords doesn't match"
        if postData['password'] != postData['confirmpw']:
            errors['pass2'] = "passwords doesn't match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class PaintManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not postData.get('title'):
            errors['title'] = 'title is required.'
        if not postData.get('desc'):
            errors['desc'] = 'description is required.'
        if not postData.get('price'):
            errors['price'] = 'price is required.'
        if not postData.get('qts'):
            errors['qts'] = 'Quantity is required.'
        if len(postData['title']) < 2:
            errors['title11'] = 'title should be at least 2 char.'
        if len(postData['desc']) < 10:
            errors['desc1'] = 'description should be at least 10 char.'
        if float(postData['price']) <=0:
            errors['price1'] = "passwords should be more than 0 "
        if int(postData['qts']) <=0:
            errors['qts1'] = "Quantity should be more than 0 "

        return errors



class Paint(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    price=models.FloatField()
    qts=models.IntegerField()
    add_by=models.ForeignKey(User,related_name='added_paints', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purchased_by=models.ManyToManyField(User, related_name='purchased_paints')
    objects=PaintManager()