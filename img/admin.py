from django.contrib import admin
from .models import img,ig_img
# Register your models here.
class ImgAdmin(admin.ModelAdmin):
    list_display=('id', 'photo', 'CreateDate')

class IgImgAdmin(admin.ModelAdmin):
    list_display=('id','username','url', 'CreateDate')

admin.site.register(img,ImgAdmin)
admin.site.register(ig_img,IgImgAdmin)
