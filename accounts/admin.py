from django.contrib import admin
from accounts.models import *

admin.site.register(Department)
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Supervisor)
admin.site.register(DepartmentManager)
admin.site.register(HrEmployee)
