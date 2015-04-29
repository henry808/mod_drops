from django.contrib import admin
from image.models import Image


class ImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ['user', 'title', 'description', 'source', 'year', 'category']}),
        ('Upload image', {'fields': ['picture']}),
        ('Date information', {'fields': ['date_uploaded', 'date_modified', 'date_published']}),
        ('Published', {'fields': ['published']}),

    ]
    readonly_fields = ('date_uploaded', 'date_modified', 'date_published')
    list_display = ('user', 'title', 'picture', 'source', 'year', 'category', 'published', 'date_uploaded', 'date_modified', 'date_published', 'size')

    def size(self, obj):
        return obj.picture.size
    size.short_description = 'File size'
    size.admin_order = 'size'

admin.site.register(Image, ImageAdmin)