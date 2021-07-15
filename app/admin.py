from django.contrib import admin
from .models import Category,Course,Profile
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug' : ('name',)}
    list_display=('name','slug')


@admin.register(Course)
class CourseyAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug' : ('title',)}
    list_display=('title','slug','is_premium','updated_date')

admin.site.register(Profile)