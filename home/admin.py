from django.contrib import admin
import django.contrib.auth.decorators
from .models import *
# Register your models here.

#admin.site.register(Project)


class ProjectInstanceInline(admin.TabularInline):
    model = TripInstance
@admin.register(Trip)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('purpose','officer','date_created')
    inlines = [ProjectInstanceInline]



