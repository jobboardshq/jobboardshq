from django.contrib import admin
from django import forms

from zobpress.models import Board, Category, EmployeeFormModel, EmployeeFieldModel


board_admin = admin.AdminSite()


class FilterOnBoard(admin.ModelAdmin):
    def queryset(self, request):
        "This will filter based on request.board"
        return self.model._default_manager.filter(board = request.board)
    
    def get_form(self, request, obj=None, **kwargs):
        form_class = super(FilterOnBoard, self).get_form(self, request, **kwargs)
        class MyModelForm(form_class):
            def get_queryset(self):
                import pdb
                pdb.set_trace()
                return super(MyModelForm, self).get_queryset().filter(board = request.board)
        return MyModelForm

class EmployeeFieldModelAdmin(admin.ModelAdmin):
    def queryset(self, request):
        "This will filter based on request.board"
        return self.model._default_manager.filter(employee_form__board = request.board)

board_admin.register(Category, FilterOnBoard)
board_admin.register(EmployeeFormModel, FilterOnBoard)
board_admin.register(EmployeeFieldModel, EmployeeFieldModelAdmin)


