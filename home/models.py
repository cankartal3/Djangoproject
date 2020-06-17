from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Settings(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(blank=True,max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    company = models.CharField(blank=True,max_length=150)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=150)
    fax = models.CharField(blank=True,max_length=150)
    email = models.CharField(blank=True,max_length=150)
    smtpserver = models.CharField(blank=True,max_length=30)
    smtpemail = models.CharField(blank=True,max_length=30)
    smtppassword = models.CharField(blank=True,max_length=20)
    smrpport = models.CharField(blank=True,max_length=6)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True,max_length=150)
    instagram = models.CharField(blank=True,max_length=150)
    youtube = models.CharField(blank=True,max_length=150)
    twitter = models.CharField(blank=True,max_length=150)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New','New'),
        ('Read','Read'),
        ('Closed','Closed'),
    )
    name = models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True,max_length=50)
    subject = models.CharField(blank=True,max_length=50)
    message = models.CharField(blank=True,max_length=255)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    note = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactFormuu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name': TextInput(attrs={'class': 'vof','placeholder':'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'vof', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'vof', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'voftextarea', 'placeholder': 'Your message','rows':'5'}),
        }


class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        phone = models.CharField(blank=True, max_length=20)
        address = models.CharField(blank=True, max_length=20)
        city = models.CharField(blank=True, max_length=20)
        country = models.CharField(blank=True, max_length=20)
        image = models.ImageField(blank=True, upload_to='images/users/')

        def __str__(self):
            return self.user.username

        def user_name(self):
            return '['+self.user.username + '] ' + self.user.first_name+ ' ' + self.user.last_name

        def image_tag(self):
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country','image']


class FAQ(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField()
    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.question


class Sifreunuttum(models.Model):
    STATUS = (
        ('Yeni', 'Yeni'),
        ('Gonderildi', 'Gonderildi'),
        ('Gonderilmedi', 'Gonderilmedi'),
    )
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=200)
    ip = models.CharField(blank=True,max_length=20)
    status = models.CharField(blank=True, max_length=20,default='Yeni', choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class SifreunuttumForm(ModelForm):
    class Meta:
        model = Sifreunuttum
        fields = ['email','username']


class AdminMessage(models.Model):
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        messagess = RichTextUploadingField()
        kimden = models.CharField(max_length=30, default='Admin')
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.messagess