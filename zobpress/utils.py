from zobpress.models import Board, Job, JobFormModel, JobData, JobContactDetail
from django.template.loader import render_to_string

type_template_mapping = {
                'CharField':"zobpress/editable_charfield_frag.html",
                'TextField': "zobpress/editable_textfield_frag.html", 
                'BooleanField':"zobpress/editable_checkbox_frag.html",
                'FileField':"zobpress/editable_filefield_frag.html",
                'RTEField':"zobpress/editable_textfield_frag.html",
                }

def create_inital_form(board):
    """When a board is first registered, create the default board for them."""
    JobFormModel.objects.create_default_form(board)
    
    

                        
                        


    
        
    
def get_editable_form(board):
    "Given  a board, show the form which is editable"
    #Get the lastet job form
    try:
        job_form = board.jobformmodel_set.order_by("-created")[0]
    except IndexError:
        return None
    form_fields = job_form.jobfieldmodel_set.all().order_by("order")
    final_template = ""
    for field in form_fields:
        template = type_template_mapping[field.type]
        final_template+=render_to_string(template, {"field_name": field.name, "field": field})
    return final_template
        
    
