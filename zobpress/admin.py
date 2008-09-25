from zobpress.models import Board, EmployeeFormModel, EmployeeFieldModel
from zobpress.models import Board, JobFormModel, JobFieldModel

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

admin.site.register(Board, BoardAdmin)
admin.site.register(EmployeeFormModel, EmployeeFormModelAdmin)
admin.site.register(EmployeeFieldModel, EmployeeFieldModelAdmin)
admin.site.register(JobFormModel, JobFormModelAdmin)
admin.site.register(JobFieldModel, JobFieldModelAdmin)