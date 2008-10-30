from django.contrib import admin

from emailsubs.models import EmailSubscription, EmailSent

class EmailSentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'updated_on')

admin.site.register(EmailSent, EmailSentAdmin)
admin.site.register(EmailSubscription)