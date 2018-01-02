from django.contrib import admin

from post.models import Post, PostCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'created', 'cate']
    list_editable = ['active']
    list_filter = ['cate']
    

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    pass
