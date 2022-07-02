from django.contrib import admin
from movie_app.models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "duration",
        "director",
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = ("title".split(),)
    # inlines = [CommentInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "movie", "stars")
    list_display_links = ("id", "text")
    search_fields = ("text",)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Review, ReviewAdmin)
