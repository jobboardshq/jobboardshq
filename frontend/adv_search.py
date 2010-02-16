
from haystack.forms import SearchForm

from zobpress.models import Job

def get_haystack_results(request):
    hs_form = SearchForm(request.POST)
    if hs_form.is_valid():
        return hs_form.search()
    return []
    
def search(data, request):
    board = request.board
    q = data['q']
    category = data['category']
    job_type = data['job_type']
    
    hay_stack_objects = False
    
    if q:
        # get results from haystack
        results = get_haystack_results(request)
        if not results:
            return None
        results = Job.objects.filter(board=board)
        hay_stack_objects = False
    else:
        results = Job.objects.filter(board=board)

    if category:
        results = results.filter(category=category)
    
    if job_type:
        results = results.filter(job_type=job_type)
        
    if hay_stack_objects:
        results = [res.object for res in results ]
        
    return results