from django.contrib import admin
from registers.models import Profile

@admin.register(Profile)
class EmployeeAdmin(admin.ModelAdmin):
    pass
