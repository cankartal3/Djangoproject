from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from content.models import CImage, Menu, Content, Commentcontent


#from turistikmekan.admin import ImagesAdmin


class ContentImageInline(admin.TabularInline):
    model = CImage
    extra = 3

class MenuContentInline(admin.TabularInline):
    model = Content
    extra = 1

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'status', 'create_at']
    list_filter = ['status', 'type']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug': ('title',)}

#class ImagesAdmin(admin.ModelAdmin):
 #   list_display = ['title', 'title', 'image_tag']

class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'status')
    list_filter = ['status']
    inlines = [MenuContentInline]

class CommentcontentAdmin(admin.ModelAdmin):
    list_display = ['id','subject','comment','user','status']
    list_filter = ['status']

admin.site.register(Commentcontent,CommentcontentAdmin)
admin.site.register(Menu,MenuAdmin)
admin.site.register(Content,ContentAdmin)
#admin.site.register(CImage,ImagesAdmin)