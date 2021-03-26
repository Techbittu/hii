from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image
from django.shortcuts import reverse,render,redirect
import random

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    profile_image = models.ImageField(default='unnamed.png',upload_to='prof',null=True,blank=True)

    def __str__(self):
        return '%s %s' %(self.user.first_name,self.user.last_name)



    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
    


class contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from ' +  self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name   

class post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    img = models.ImageField(upload_to='pics')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(default=now)
    slug = models.CharField(default=f"Post-Url-BlogPost-{random.randint(100,100000)}",max_length=80)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

class postComments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    postcomment = models.ForeignKey(post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):

        return '%s ...  %s' % (self.comment[0:13],self.user.username)
    
