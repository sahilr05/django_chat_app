from django.contrib import admin  # NOQA

from .models import User,  Interest

admin.site.register([User, Interest])