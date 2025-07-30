from django.contrib import admin
from blogApp.models import postModel,commentModel

# Register your models here.
admin.site.register(postModel)
admin.site.register(commentModel)
