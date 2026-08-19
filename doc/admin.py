from django.contrib import admin
from .models import Cars, MatchingGroup, Course


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(MatchingGroup)
class MatchingGroupAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "academy",
        "direction",
        "location",
        "time",
        "match_percent",
    )
    list_filter = ("direction", "location", "time")
    search_fields = ("title", "academy", "direction", "location")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "teacher",
        "price",
        "rating",
        "students",
    )
    list_filter = ("category",)
    search_fields = ("title", "teacher")
    ordering = ("-rating", "title")
