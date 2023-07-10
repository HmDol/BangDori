from django.contrib import admin

from .models import CustomerUser
from .models import Authentication
from .models import UpvoteHistory


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'birthday', 'phone', 'nickname')


class SMSAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'auth_number')


class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'board', 'article_id')


admin.site.register(Authentication, SMSAdmin)
admin.site.register(CustomerUser, UserAdmin)
admin.site.register(UpvoteHistory, UpvoteAdmin)
