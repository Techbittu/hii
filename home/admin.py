from django.contrib import admin
from .models import contact ,postComments,post,Profile ,Category

# Register your models here.

admin.site.register(contact)
admin.site.register(postComments)
admin.site.register(Profile)
admin.site.register(Category)

@admin.register(post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyscript.js',)