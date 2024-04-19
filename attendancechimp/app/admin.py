from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(QRCodeUpload)
admin.site.register(QRCode)
admin.site.register(Course)



class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_instructor')

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    username.short_description = 'Username'
    email.short_description = 'Email'
    username.admin_order_field = 'user__username'
    email.admin_order_field = 'user__email'

admin.site.register(UniversityPerson, MemberAdmin)
