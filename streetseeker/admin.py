from django.contrib import admin
from .models import Place, Comment, Contact

# Register your models here.
admin.site.register(Place)
admin.site.register(Comment)
admin.site.register(Contact)