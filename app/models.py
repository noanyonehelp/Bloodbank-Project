from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _
# Create your models here.

class BloodBank(models.Model):

    city = [
        ("جوجر","جوجر"),
        ("ميت الكرماء","ميت الكرماء"),
    ]

    types = [
        ("A+","A+"),
        ("A-","A-"),
        ("B+","B+"),
        ("B-","B-"),
        ("AB+","AB+"),
        ("AB-","AB-"),
        ("O+","O+"),
        ("O-","O-"),
    ]
    joined = models.DateTimeField(null=True, blank=True, max_length=20, auto_now_add=True)

    bloodbank_name = models.CharField(max_length=100, null=True, help_text="اﻻسم")

    bloodbank_addr = models.CharField(max_length=255, null=True, help_text="العنوان")

    type =  models.CharField(max_length=50, null=True, choices=types, help_text="نوع فصيلة الدم")

    mobile = models.CharField(max_length=11, null=True, help_text='رقم الهاتف المحمول', default=None, blank=True)

    city =  models.CharField(max_length=50, null=True, choices=city, help_text="القرية")

    count_views = models.IntegerField(null=True, blank=True, default=0)

    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    likeBloodbank = models.ManyToManyField(User, related_name='likeBloodbank', blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=1, blank=1)

    def __str__(self):
        return self.bloodbank_name

    def total_likes(self):
        return self.likeBloodbank.count()
        
    def get_absolute_url(self):
        return reverse("profilebloodbank", kwargs={"id": self.id})
    

class Comment(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    comment = models.TextField(max_length=5000, null=True, verbose_name='التعليق')
    bloodbank = models.ForeignKey(BloodBank, related_name='comments', on_delete=models.CASCADE)
    userProfile = models.ForeignKey(User, related_name='userProfile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ['-created_at']


class Visitor_Infos(models.Model):
    ip_address = models.GenericIPAddressField()
    page_visited = models.TextField()
    event_date = models.DateTimeField(default=datetime.now)