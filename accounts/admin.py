from django.contrib import admin
from accounts.models import *


class EmployeeMoreAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Roles.employee)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DirectHeadMoreAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Roles.directHead)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DepartmentManagerMoreAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Roles.departmentManager)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HrEmployeeMoreAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Roles.hrEmployee)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(EmployeeMore, EmployeeMoreAdmin)
admin.site.register(DepartmentManagerMore, DepartmentManagerMoreAdmin)
admin.site.register(HrEmployeeMore, HrEmployeeMoreAdmin)

admin.site.register(Department)
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(HrEmployee)
