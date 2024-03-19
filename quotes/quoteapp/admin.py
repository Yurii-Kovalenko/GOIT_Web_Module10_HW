from django.contrib import admin

from .models import Tag, Author, Quote, TopTenTags


admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(TopTenTags)
