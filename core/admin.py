from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(ObjectPerspectiveBlueprint)
admin.site.register(GroupObject)
admin.site.register(GroupObjectInstance)
admin.site.register(InstanceNotes)
admin.site.register(BlueprintObjectInstance)
