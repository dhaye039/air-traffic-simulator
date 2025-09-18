from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, Permission
#from .permissions import group

# Register your models here.
admin.site.register(Gate)
admin.site.register(Airplane)
admin.site.register(Runway)
admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(TakeOffRequest)
admin.site.register(GateRunwayAssignment)
admin.site.register(PassengerAssignment)
admin.site.register(Permission)

# Custom GroupAdmin
class CustomGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)

# Unregister the default Group admin
admin.site.unregister(Group)

# Register the Group model with the custom admin
admin.site.register(Group, CustomGroupAdmin)