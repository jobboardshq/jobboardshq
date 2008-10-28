from zobpress.models import Board, EmployeeFormModel, EmployeeFieldModel
from zobpress.models import JobFormModel, JobFieldModel, Category, Job, JobData, Employee, EmployeeData

from django.contrib import admin

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain')
    
class EmployeeFormModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    
class EmployeeFieldModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'type')
    
class JobFormModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    
class JobFieldModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'type')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'board', 'name')

admin.site.register(Board, BoardAdmin)
admin.site.register(EmployeeFormModel, EmployeeFormModelAdmin)
admin.site.register(EmployeeFieldModel, EmployeeFieldModelAdmin)
admin.site.register(JobFormModel, JobFormModelAdmin)
admin.site.register(JobFieldModel, JobFieldModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Job)
admin.site.register(JobData)
admin.site.register(Employee)
admin.site.register(EmployeeData)