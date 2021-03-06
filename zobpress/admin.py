from zobpress.models import Board, BoardPayments, DeletedEntities, BoardSettings
from zobpress.models import JobFormModel, JobFieldModel, Category, Job, JobData, JobType, Page, Applicant
from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE
class BoardAdminForm(forms.ModelForm):
    introductory_text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    class Meta:
        model = Board

class BoardAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'subdomain')
    class Media:
      js = (
           '/site_media/js/tiny_mce/tiny_mce.js',
           '/site_media/js/admin_pages.js'
      )
            

    
class JobFormModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    
class JobFieldModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'type')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'board', 'name')

admin.site.register(Board, BoardAdmin)
admin.site.register(BoardSettings)
admin.site.register(JobFormModel, JobFormModelAdmin)
admin.site.register(JobFieldModel, JobFieldModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Job)
admin.site.register(JobData)
admin.site.register(BoardPayments)
admin.site.register(JobType)
admin.site.register(DeletedEntities)
admin.site.register(Page)
admin.site.register(Applicant)
