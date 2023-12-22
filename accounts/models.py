from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phoneRegex = RegexValidator(
    regex=r"^01[0-5]\d{8}$",
    message="Phone number must be 11 digits and start with 010, 011, 012, or 015.",
)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserManager(models.Manager):
    def create_user(self, **extra_fields):
        role = extra_fields.pop("role", User.Roles.employee)
        return self.create(role=role, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractUser):
    objects = UserManager()

    class Roles(models.TextChoices):
        employee = "employee", "Employee"
        supervisor = "supervisor", "Supervisor"
        departmentManager = "departmentManager", "DepartmentManager"
        hrEmployee = "hrEmployee", "HrEmployee"

    department = models.ForeignKey(
        Department, related_name="department", on_delete=models.SET_NULL, null=True
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


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.employee)


class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.supervisor)


class DepartmentManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(role=User.Roles.departmentManager)
        )


class HrEmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.hrEmployee)


class DepartmentManager(User):
    objects = DepartmentManagerManager()
    role = User.Roles.departmentManager

    class Meta:
        proxy = True


class Supervisor(User):
    objects = SupervisorManager()
    role = User.Roles.supervisor

    class Meta:
        proxy = True


class HrEmployee(User):
    objects = HrEmployeeManager()
    role = User.Roles.hrEmployee

    class Meta:
        proxy = True


class Employee(User):
    objects = EmployeeManager()
    role = User.Roles.employee

    @property
    def more(self):
        return self.EmployeeMore

    class Meta:
        proxy = True


class EmployeeMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="more")
    empSupervisor = models.ForeignKey(
        Employee, related_name="supervisor", on_delete=models.SET_NULL, null=True
    )
    departmentManager = models.ForeignKey(
        DepartmentManager,
        related_name="departmentManager",
        on_delete=models.SET_NULL,
        null=True,
    )
