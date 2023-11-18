from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    follows=models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True

    )
    date_added=models.DateTimeField(auto_now_add=True)
    photo=models.ImageField(upload_to='fefi/photos/%Y/%m/%d',blank=True)
    def __str__(self):
        return self.user.username
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile,sender=User)            
class Fef(models.Model):
    profile=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='fefs')
    text=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='fef_like',blank=True)
    im=models.ImageField(upload_to='fefi/pics/%Y/%m/%d',blank=True)
    video=models.FileField(upload_to='fefi/video/%Y/%m/%d',blank=True)
    audio=models.FileField(upload_to='fefi/audio/%Y-%m-%d',blank=True)
    def number_of_likes(self):
        return self.likes.count()
    def __str__(self):
        return (
            f"{self.profile}"
            f"{self.date_created:%Y-%m-%d %H:%M}"
            f"{self.text[:30]}..." )
class Reply(models.Model):
    fef=models.ForeignKey(Fef,on_delete=models.CASCADE,related_name='replies')
    body=models.CharField(max_length=300)
    date_created=models.DateTimeField(auto_now_add=True)
    users=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='replies')
    repimg=models.ImageField(upload_to='fefi/pics/%Y/%m/%d',blank=True)
    repvideo=models.FileField(upload_to='fefi/video/%M/%y/%d',blank=True)
    likes=models.ManyToManyField(User,related_name='reply_like',blank=True)
    audio2=models.FileField(upload_to='fefi/audio/%Y/%m/%d',blank=True)
    def numbers_of_likes(self):
        return self.likes.count() 
    def __str__(self):
        try:
            return f"{self.users.username} :{self.body[:30]}"
        except:
            return f"no author :{self.body[:30]}"
   
        
   



        
 
# Create your models here.
