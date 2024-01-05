from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(ObjectivePerspectiveBlueprint)
admin.site.register(GroupObjective)
admin.site.register(GroupObjectiveInstance)
admin.site.register(InstanceNotes)
admin.site.register(BlueprintObjectiveInstance)
