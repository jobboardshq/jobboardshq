
from haystack import indexes, site

from zobpress.models import Job

class JobIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    as_clob = indexes.CharField(model_attr = "as_clob")
    
site.register(Job, JobIndex)