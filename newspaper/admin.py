from django.contrib import admin
from newspaper.models import Newsletter, Post,Category,Tag,Comment, UserProfile, Contact
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Newsletter)



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display =["title", "category", "author"]
    date_hierarchy = "published_at"

admin.site.register(Post, PostAdmin)