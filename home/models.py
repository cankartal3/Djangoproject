from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
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
    twitter = models.CharField(blank=True,max_length=150)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.title
