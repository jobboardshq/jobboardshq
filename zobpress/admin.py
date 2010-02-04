from zobpress.models import Board, BoardPayments, DeletedEntities
from zobpress.models import JobFormModel, JobFieldModel, Category, Job, JobData, JobType

from django.contrib import admin

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain')
    
class JobFormModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    
class JobFieldModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'type')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'board', 'name')

admin.site.register(Board, BoardAdmin)
admin.site.register(JobFormModel, JobFormModelAdmin)
admin.site.register(JobFieldModel, JobFieldModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Job)
admin.site.register(JobData)
admin.site.register(BoardPayments)
admin.site.register(JobType)
admin.site.register(DeletedEntities)