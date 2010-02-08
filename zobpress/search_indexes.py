
from haystack import indexes, site

from zobpress.models import Job

class JobIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    as_clob = indexes.CharField()
    name = indexes.CharField(model_attr = "name")
    description = indexes.CharField(model_attr = "description")
    board = indexes.CharField(model_attr = "board")
    
site.register(Job, JobIndex)