import django.contrib.auth.mixins
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
    
class Trip(models.Model):
    officer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    driver = models.CharField(max_length=100)
    purpose = models.TextField()
    time_in = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("Trip-detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.destination

    class Meta:
        ordering = ['-date_created']

class Officer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True,blank=True)

    
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

class TripInstance(models.Model):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    trip = models.ForeignKey(Trip,max_length=20,on_delete=models.RESTRICT, null=False)
    

