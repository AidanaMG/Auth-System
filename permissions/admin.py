from django.contrib import admin
from .models import Role, BusinessElement, AccessRule

admin.site.register(Role)
admin.site.register(BusinessElement)
admin.site.register(AccessRule)