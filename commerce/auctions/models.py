
from django.contrib.auth.models import AbstractUser
from django.db import models

class auction_listings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default=None, null=False)
    title = models.CharField(max_length=64, default=None, null = True)
    url = models.CharField(max_length=200, default=None, null = False)
    description = models.CharField(max_length=500, default=None, null = False)
    price = models.CharField(max_length=64, default=None, null = False)
    date = models.CharField(max_length=64, default=None, null = False)
    category = models.CharField(max_length=64, default=None, null = False)
    def __str__(self):
        return f" {self.id} {self.name} {self.title} {self.url} {self.description} {self.price} {self.date} {self.category}"

class connect_two(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, default=None, null=False)
    user_linking = models.ManyToManyField(auction_listings, blank = True, related_name="list_info")
    def __str__(self):
        return f"{self.id} {self.username} {self.user_linking}"

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return f" {self.id} {self.username}"

class bids(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, default=None, null = True)
    username = models.CharField(max_length=64, default=None, null=True)
    bids_made = models.CharField(max_length=64, default=None)
    def __str__(self):
        return f"{self.id} {self.title} {self.username} {self.bids_made}"

class comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=500, default=None, null = False)
    username = models.CharField(max_length=64, default = None, null = False)
    title = models.CharField(max_length=64, default=None, null=False)
    def __str__(self):
        return f"{self.id} {self.username} {self.comment} {self.title}"
    
class closed_listings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default=None, null=False)
    title = models.CharField(max_length=64, default=None, null = True)
    url = models.CharField(max_length=200, default=None, null = False)
    description = models.CharField(max_length=500, default=None, null = False)
    price = models.CharField(max_length=64, default=None, null = False)
    date = models.CharField(max_length=64, default=None, null = False)
    category = models.CharField(max_length=64, default=None, null = False)
    username = models.CharField(max_length=64, default=None, null=False)
    def __str__(self):
        return f" {self.id} {self.name} {self.title} {self.url} {self.description} {self.price} {self.date} {self.category} {self.username}"