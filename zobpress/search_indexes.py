
from haystack import indexes, site

from zobpress.models import Job

class JobIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    as_clob = indexes.CharField()
    name = indexes.CharField()
    description = indexes.CharField()
    
site.register(Job, JobIndex)