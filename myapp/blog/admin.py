from django.contrib import admin
from .models import post,Category,AboutUs


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content') # only displaying content
    search_fields = ('title','content') # its searching the content and text
    list_filter = ('Category', 'created_at') # add filter column 


# Register your models here.
admin.site.register(post,PostAdmin)
admin.site.register(Category)
admin.site.register(AboutUs)
