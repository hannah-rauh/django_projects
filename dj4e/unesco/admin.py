from django.contrib import admin

# Register your models here.

from unesco.models import Site, Category, iso, Region, States

admin.site.register(Site)
admin.site.register(Category)
admin.site.register(iso)
admin.site.register(Region)
admin.site.register(States)
