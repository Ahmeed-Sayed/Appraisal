from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

phoneRegex = RegexValidator(
    regex=r"^01[0-5]\d{8}$",
    message="Phone number must be 11 digits and start with 010, 011, 012, or 015.",
)


class UserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        role = extra_fields.pop("role", User.Roles.employee)
        return self.create(role=role, **extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        password = extra_fields.pop("password", None)
        user = self.create_user(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    objects = UserManager()

    class Roles(models.TextChoices):
        employee = "employee", "Employee"
        directHead = "directHead", "DirectHead"
        departmentManager = "departmentManager", "DepartmentManager"
        hrEmployee = "hrEmployee", "HrEmployee"

    department = models.ForeignKey(
        Department, related_name="user", on_delete=models.SET_NULL, null=True
    )
    role = models.CharField(
        verbose_name="Role",
        max_length=255,
        default=Roles.employee,
    )
    address = models.CharField(max_length=150, blank=True, null=True)

    phoneNumber = models.CharField(
        validators=[phoneRegex],
        max_length=11,
        unique=True,
        verbose_name="Phone Number",
        blank=True,
        null=True,
    )


class EmployeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.employee)


class DirectHeadManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.directHead)


class DepartmentManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(role=User.Roles.departmentManager)
        )


class DepartmentManagerMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    managedDepartment=models.OneToOneField(Department,on_delete=models.SET_NULL,null=True,related_name='manager')

class DepartmentManager(User):
    objects = DepartmentManagerManager()
    role = User.Roles.departmentManager

    @property
    def more(self):
        return self.departmentmanagermore

    class Meta:
        proxy = True


class DirectHead(User):
    objects = DirectHeadManager()
    role = User.Roles.directHead

    class Meta:
        proxy = True


class HrEmployeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.hrEmployee)

class HrEmployeeMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    empDirectHead = models.ForeignKey(
        DirectHead, related_name="hrDirectHead", on_delete=models.SET_NULL, null=True
    )


class HrEmployee(User):
    objects = HrEmployeeManager()
    role = User.Roles.hrEmployee

    @property
    def more(self):
        return self.hremployeemore

    class Meta:
        proxy = True


class EmployeeMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    empDirectHead = models.ForeignKey(
        DirectHead,
        related_name="employeedirectHead",
        on_delete=models.SET_NULL,
        null=True,
    )


class Employee(User):
    objects = EmployeeManager()
    role = User.Roles.employee

    @property
    def more(self):
        return self.employeemore

    class Meta:
        proxy = True
