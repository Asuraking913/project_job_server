from email.policy import default
from random import choice, choices
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
from django.contrib import admin

def generate_id():
    return uuid4().hex

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("The email field is not provided")
        if not password:
            raise ValueError("The password field should be provided@")
        email = self.normalize_email(email)
        user = self.model(email = email, **kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('is_staff attribute must be set to true')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('is_superuser must be set to True')
        
        return self.create_user(email, password, **kwargs)

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    username = None
    role_choices = (
            ('hire', 'hire'),
            ('freelance', 'freelance'),
        )

    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    address_default = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length = 255, blank=True)
    last_name = models.CharField(max_length = 255, blank=True)
    phone_number = models.CharField(max_length = 255, blank=True)
    location = models.TextField(blank=True)
    role  = models.CharField(choices = role_choices, max_length = 255, null=False)

    REQUIRED_FIELDS = []
    objects = UserManager()

class Profile(models.Model):
    id = models.CharField(max_length = 255, unique = True, null = False, default = generate_id, primary_key = True)
    job_title = models.CharField(max_length = 255, blank = True)
    experience = models.IntegerField(default = 1, blank = True)
    hourly_rate = models.FloatField(blank = True, null = True)
    languages = models.CharField(max_length = 255, blank = True)
    bio = models.TextField(blank = True)
    skills = models.TextField(blank = True)
    education = models.TextField(blank = True)
    website_link = models.CharField(max_length = 255, blank = True, null = True)
    linkdeln_link = models.CharField(max_length = 255, blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)

class Job(models.Model):

    type_choices = (
            ('one', 'subscription'),
            ('con', 'contract'),
        )
    size_choices = (
                ("1", 'Writing'),
                ("2", 'Design'),
                ("3", 'Development'),
                ("4", 'Marketing'),
                ("5", 'Management'),
                ("6", 'Data Entry'),
                ("7", 'Customer Service'),
                ("8", 'Translation'), 
                ("9", 'others')
            )

    company_size_choices = (
            ("1", '1-10'),
            ("2", '11-50'),
            ("3", '51-200'),
            ("4", '201-500'),
            ("5", '500+'),
            
        )

    payment_type_choices = (
            ("1", "Fixed Price"),
            ("2", "Monthly"),
        )

    id = models.CharField(max_length = 255, unique = True, null = False, default = generate_id, primary_key = True)
    job_title = models.CharField(max_length = 255)
    job_type = models.CharField(max_length = 255, choices=type_choices)
    location = models.CharField(max_length = 255)
    description = models.TextField()
    category = models.CharField(max_length = 255, choices = size_choices)
    payment_type = models.CharField(max_length = 255, choices = payment_type_choices)
    min_budget = models.IntegerField()
    max_budget = models.IntegerField()
    company_size = models.CharField(max_length = 255, choices = company_size_choices)
    required_skills = models.CharField(max_length = 400)
    special_skills = models.CharField(max_length = 255, default = '')
    duration = models.CharField(max_length = 255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = "")
    posted_date = models.DateTimeField(null=False, auto_now=True)

    # deadline date


class Apply(models.Model):

    status_choices = (
            ("1", "pending"), 
            ("2", "rejected"), 
            ("3", "accepted")
        )

    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user_doc = models.FileField(blank = True)
    salary = models.IntegerField(default=10000)
    status = models.CharField(max_length = 15,choices = status_choices, default = 'pending')
    applied_date = models.DateTimeField(null=False, auto_now=True)

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null = False)
    name  = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    available_stock = models.PositiveIntegerField(null=False)
    category = models.CharField(max_length=50, null = False)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Order(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True, default=generate_id, null=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
