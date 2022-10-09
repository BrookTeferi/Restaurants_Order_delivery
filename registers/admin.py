from django.contrib import admin

@admin.register(Profile)
class EmployeeAdmin(admin.ModelAdmin):
    pass
