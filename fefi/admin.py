from .models import Profile,Fef,Reply
from django.contrib import admin
from django.contrib.auth.models import Group
@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','date_added','photo']
    raw_id_fields=['user']
    #the readonly_fields=['id] is important in displaying image uploads too.
    readonly_fields=['id']
@admin.register(Fef)
class FefAdmin(admin.ModelAdmin):
    list_display=['profile','date_created','im','text','video']
    raw_id_fields=['profile']
    readonly_fields=['id']
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display=['fef','date_created','repimg','repvideo','body','users']
    list_filter=['date_created']
    raw_id_fields=['users']
    search_fields=['body']
    readonly_fields=['id']   
admin.site.unregister(Group)

# Register your models here.
