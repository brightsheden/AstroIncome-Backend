import site
from django.contrib import admin

from .models import Deposit, Investment, Profile, withdrawal

# Register your models here.
admin.site.register(Profile)
admin.site.register(Investment)
admin.site.register(Deposit)
admin.site.register(withdrawal)