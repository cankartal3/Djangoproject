from django.contrib import admin

# Register your models here.
from home.models import Settings, ContactFormMessage, UserProfile, FAQ, AdminMessage, Sifreunuttum


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','note', 'status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','address','city','country','image_tag']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question' , 'ordernumber' , 'answer', 'status']
    list_filter = ['status']

class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'kimden']

class SifreunuttumAdmin(admin.ModelAdmin):
    list_display = ['username','email','status','ip','create_at','update_at']
    list_filter = ['status']

admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Settings)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(AdminMessage,AdminMessageAdmin)
admin.site.register(Sifreunuttum,SifreunuttumAdmin)