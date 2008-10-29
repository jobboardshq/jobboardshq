from django.contrib.syndication.feeds import Feed
from zobpress.models import Job, Employee

class JobFeed(Feed):
    title = "Latest Jobs"
    link = "/sitenews/"
    description = "Latest Jobs added to our site"

    def items(self):
        return Job.objects.order_by('-created_on')[:5]
    
class EmployeeFeed(Feed):
    title = "Recent People"
    link = "/sitenews/"
    description = "Latest people added to our site"

    def items(self):
        return Employee.objects.order_by('-created_on')[:5]
    