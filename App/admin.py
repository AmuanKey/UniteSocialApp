from django.contrib import admin
from .models import PostModel,CategoryModel,CommentModel

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ("title","body","created_at")
    list_filter = ("created_at", )
    search_fields = ("title","body", )

admin.site.register(PostModel)
admin.site.register(CategoryModel)
admin.site.register(CommentModel)


