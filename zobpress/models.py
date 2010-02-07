from django.db import models
from django.db.models import permalink
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify

from libs.fields import AutoSlugField

from datetime import date, datetime, timedelta
from django.core.urlresolvers import reverse

type_mapping = {
                'CharField':(forms.CharField, dict(max_length = 100)), 'TextField': (forms.CharField, dict(widget = forms.Textarea)), 
                'BooleanField':(forms.BooleanField, dict(required = False)), 'RTEField':(forms.CharField, dict(widget = forms.Textarea(attrs={"class":"rich_text"}))),
                'URLField': (forms.URLField, dict()), 'EmailField': (forms.EmailField, dict()),
                'CategoryField': (forms.ModelChoiceField, dict()), 'FileField':(forms.FileField, dict()), 
                }
rev_type_mapping_list  = [(v[0], k) for k,v in type_mapping.iteritems()]
type_mapping_list  = [(k, k) for k,v in type_mapping.iteritems()]
rev_type_mapping = {}
for el in rev_type_mapping_list:
    rev_type_mapping[el[0]] = el[1]
    
class BoardManager(models.Manager):
    "Manager for a board."
    def register_new_board(self, subdomain, name, description, user):
        "Create a new board, creating other objects as needed."
        board = Board(subdomain = subdomain, name = name, description = description, owner = user)
        board.save()
        from emailsubs.models import EmailSent
        email_sent = EmailSent(board =  board)
        email_sent.save()
        from profiles.models import UserProfile
        user_profile = UserProfile(user = user)
        user_profile.save()
        board_extended_settings = BoardExtendedSettings(board = board)
        board_extended_settings.save()
        JobFormModel.objects.create_default_form(board = board)
        return board

class Board(models.Model):
    subdomain = models.CharField(max_length = 100, unique = True)
    domain = models.CharField(null = True, blank = True, max_length = 100, unique = True)
    name = models.CharField(max_length = 100)        
    description = models.TextField()
    
    #Settings for Board
    "For listings value  of 0 means it never expires. For cost 0 means listing is free."
    job_listing_expires = models.PositiveIntegerField(default = 0)#Number of days a job should show up before being removed.
    cost_per_job_listing = models.PositiveIntegerField(default = 0)#Amount in USD which a user needs to pay to activate their listing.
    
    owner = models.ForeignKey(User)
    
    objects = BoardManager()
    
    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return 'http://%s.%s' % (self.subdomain, current_site.domain)
    
    def get_management_url(self):
        return "%s/%s/" % (self.get_absolute_url(), 'manage')
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # create settings
        super(Board, self).save(*args, **kwargs)
        BoardSettings.objects.get_or_create(board=self)
        


class BoardSpecificEntitiesManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        from zobpress.middleware import get_current_board
        board = get_current_board()
        qs = super(BoardSpecificEntitiesManager, self).get_query_set( *args, **kwargs)
        if board:
            qs =  qs.filter(board = board)
        field_names = [field.name for field in self.model._meta.fields]
        if "is_deleted" in field_names:
            qs = qs.filter(is_deleted = False)
        return qs
    
    
    
class BoardSpecificEntities(models.Model):
    board = models.ForeignKey(Board)
    
    objects = BoardSpecificEntitiesManager()
    
    def save(self, *args, **kwargs):
        if not self.board:
            from zobpress.middleware import get_current_board
            self.board = get_current_board()
        super(BoardSpecificEntities, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True
        
class DeletedEntities(models.Model):
    board = models.ForeignKey(Board)
    deleted_on = models.DateTimeField(default = datetime.now)
    
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    
    content_object = generic.GenericForeignKey()
    
    def get_content_object(self):
        klass = self.content_type.model_class()
        try:
            return klass.all_objects.get(pk = self.object_id)
        except klass.DoesNotExist:
            pass
        
    
class BoardSettings(models.Model):
    board = models.OneToOneField(Board, related_name='settings')
    
    analytics_code = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    tag_line = models.CharField(max_length = 250, null=True, blank=True)
    template = models.CharField(max_length = 100, default='default')
    
class BoardPayPal(models.Model):
    board = models.OneToOneField(Board, primary_key = True)
    paypal_token_sec = models.CharField(null = True, blank = True, max_length = 100)
    paypal_token_gec = models.CharField(null = True, blank = True, max_length = 100)
    paypal_payer_id = models.CharField(null = True, blank = True, max_length = 100)
    
class BoardExtendedSettings(models.Model):
    "Extended settings for the board"
    board = models.OneToOneField(Board, primary_key = True)
    is_default_job_form = models.BooleanField(True)#Is the Job form a Default form.
    
class BoardPaymentsManager(models.Manager):
    def add_job_payment(self, board, amount, amount_for = None):
        if amount_for == None:
            amount_for = date.today()
        board_payment, created = BoardPayments.objects.get_or_create(board = board,  amount_for = amount_for)
        board_payment.job_payments = board_payment.job_payments + amount
        board_payment.save()
        
class BoardPayments(models.Model):
    board = models.ForeignKey(Board)
    amount_for = models.DateField()
    job_payments = models.PositiveIntegerField(default = 0, )
    payment_type = models.CharField(default = 'PayPal', max_length = 10)# As we get multiple gateways, we will have multiple types.
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now_add = 1)
    
    objects = BoardPaymentsManager()
    
class Category(BoardSpecificEntities):
    "Categories for a specific board"
    
    #board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    is_deleted = models.BooleanField(default = False)
    
    all_objects = models.Manager()
    objects = BoardSpecificEntitiesManager()
    
    
    @models.permalink
    def get_absolute_url(self):
        return('zobpress.views.category_jobs', [self.slug])
    
    @models.permalink
    def get_jobs_url(self):
        return('zobpress.views.category_jobs', [self.slug])
    
    @models.permalink
    def edit_url(self):
        return('zobpress.views.edit_category', [self.pk])
    
    def get_public_jobs(self):
        "Gets public jobs of a category, that which has not been deleted, or made inactive."
        return self.job_set.filter(is_active = True, is_deleted = False)
    
    def delete(self):
        "Never delete"
        model_delete(self)
    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        unique_together = ("board", "name", "is_deleted")
    
class JobType(BoardSpecificEntities):
    #board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    slug = AutoSlugField(max_length = 100, populate_from = "name")
    is_deleted = models.BooleanField(default = False)
    
    def delete(self):
        "Never delete"
        model_delete(self)
    
    def __unicode__(self):
        return self.name
    
default_fields = [
                      ("Location", "CharField", True, "Where is this job located?"),
                      ("Approximate Budget", "CharField", False, "What is the approximate budget? Leave blank if you are not sure."),
                      ("Company", "CharField", False, "What is name of the company offering this job. Leave blank if you would rather not disclose this."),
                      ("Company Url", "CharField", False, "Url of the company. (Optional.)"),
                ]  
  
class JobFormModelManager(models.Manager):
    def create_default_form(self, board):
        
        job_form_model, created = JobFormModel.objects.get_or_create(board = board)
        for field_name, field_type, required, help_text in default_fields:
            JobFieldModel.objects.get_or_create(job_form = job_form_model, name=field_name, type = field_type,\
                                                 required = required, help_text = help_text)
#        
#        job_form = JobFormModel(board = board)
#        job_form.save()
#        job_description = JobFieldModel(job_form = job_form, name = 'Job Description', type = 'TextField', order = 0)
#        job_description.save()

class JobFormModel(models.Model):
    "Model for Job form for a specific Job board."
    board = models.ForeignKey(Board, unique = True)
    
    created = models.DateTimeField(default = datetime.now)
    
    objects = JobFormModelManager()
    
    def __unicode__(self):
        return self.board.name
    
class JobFieldModel(models.Model):
    "Model for Job form fields for a specific Job board."
    job_form = models.ForeignKey(JobFormModel)
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100, choices= type_mapping_list)
    required = models.BooleanField(default = True)
    help_text = models.TextField(max_length = 100, null = True, blank = True)
    order = models.IntegerField(default = 10)
    
    def __unicode__(self):
        return self.job_form.board.name
    
    
    class Meta:
        unique_together = (('job_form', 'name'), )
        ordering = ('-order', )

    
class JobPublicManager(BoardSpecificEntitiesManager):
    def get_query_set(self):
        return super(JobPublicManager, self).get_query_set().filter(is_active = True)
        
    def get_public_jobs(self, board):
        "If people_listing_expires is a non zero value, filter on number of days this will be active. Else all paid for are active."
        active_for = board.job_listing_expires
        if active_for:
            return self.filter(created_on__gt = date.today() - timedelta(days = active_for))
        else:
            return self.all()    
    
class Job(BoardSpecificEntities):
    #board = models.ForeignKey(Board)
    name = models.CharField(max_length = 300, null=True, blank=True)
    
    category = models.ForeignKey(Category)
    job_type = models.ForeignKey(JobType, null=True, blank=True)
    
    description = models.TextField()
    
    job_slug = models.SlugField(max_length=100)
    
    times_viewed = models.PositiveIntegerField(default = 0)
    
    is_active = models.BooleanField(default = False)#listings start as inactive. After Payment become active.
    is_expired = models.BooleanField(default = False)#Has this listing expired yet?
    is_editable = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    
    paypal_token_sec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from set_express_checkout
    paypal_token_gec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from get_express_checkout
    
    
    
    all_objects = models.Manager()
    objects = BoardSpecificEntitiesManager()
    public_objects = JobPublicManager()
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    def __unicode__(self):
        return self.name or ''
    
    def delete(self):
        model_delete(self)
    
    
    def as_snippet(self):
        "Get the current job as a snippet."
        snippet = ""
        data = self.jobdata_set.all()[:2]
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
   
    @property
    def as_clob(self):
        "As a large text."
        snippet = ""
        snippet += '\n'.join([self.name or '', self.category.name or '', self.job_type.name or ''])
        data = self.jobdata_set.all()
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
    
    @permalink
    def get_absolute_url(self):
        return ('frontend.views.job', [str(self.job_slug)])
    
    @permalink
    def edit_link(self):
        return ('zobpress.views.edit_job', [self.pk])
    
    @property
    def primary_contact(self):
        if self.jobcontactdetail_set.all().count():
            return self.jobcontactdetail_set.all()[0]
    
    class Meta:
        ordering = ('-created_on', )
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.job_slug = slugify(self.name)
            slug_count = Job.objects.filter(job_slug__icontains = self.job_slug).count()
            if slug_count:
                self.job_slug += str(slug_count + 1)
        super(Job, self).save(*args, **kwargs)
        
class JobContactDetail(models.Model):
    job = models.ForeignKey(Job)
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    website = models.URLField(null = True, blank = True)
        
class JobData(models.Model):
    job = models.ForeignKey(Job)
    data_type = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    value = models.TextField()
    
    def value_as_str(self):
        "Value as pretty string"
        if self.data_type == 'BooleanField':
            if self.value:
                return 'Yes'
            else:
                return 'No'
        return self.value

    def get_absolute_url(self):
        if self.data_type == 'FileField':
            return self.jobfile_set.all()[0].get_absolute_url()
        return self.value
    
class JobFile(models.Model):
    "Files attached to a specific Job"
    job = models.ForeignKey(Job)
    job_data = models.ForeignKey(JobData)
    uploaded_file = models.CharField(max_length = 100)
    public_path = models.CharField(max_length = 100)
    content_type = models.CharField(max_length = 100)
    
    def get_absolute_url(self):
        return settings.MEDIA_URL + self.public_path
    
class Applicant(BoardSpecificEntities):
    job = models.ForeignKey(Job)
    name = models.CharField(max_length = 100, help_text = "Your name")
    response = models.TextField(help_text = "What would you like to say")
    email = models.EmailField(help_text = "Your email id")
    resume = models.FileField(upload_to = "resumes")
    
    
class Page(BoardSpecificEntities):
    #job_board = models.ForeignKey(Board)
    title = models.CharField(max_length=100, help_text="Title of the created page.")
    page_slug = models.SlugField(max_length=100, unique = False, help_text="Slug to be used as url identifier.")
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("frontend_job_board_page", args =[self.page_slug])
    
    def save(self, *args, **kwargs):
        if not self.page_slug and not self.pk:
            self.page_slug = slugify(self.title)
            slug_count = Page.objects.filter(page_slug__icontains = self.page_slug, board=self.board).count()
            if slug_count:
                self.page_slug = self.page_slug +str(slug_count)
        super(Page, self).save(*args, **kwargs)
        
    class Meta:
        unique_together = ("board", "page_slug")
        
#Signals
def populate_job_board_form_initial(sender, instance, created, **kwargs):
    "Called when a board is first created to populate the JObBoardForm"
    from zobpress.utils import create_inital_form
    if created:
        create_inital_form(instance)
        
initial_categories = [
                      ("Engineering", "engineering"),
                      ("Sales", "sales"),
                      ("Testing", "testing"),
                      ("Finanace", "finanace")
                      ] 
    
initial_job_types = [
                     ("Permanent", "permananent"),
                     ("Freelance", "freelance"),
                     ("Part time", "part-time"),
                     ]

initial_pages = [
                 ("Privacy Policy", "Update your privacy policy here."),
                 ("Faqs", "Update your Faqs here."),
                 ("Contact Us", "Update your contact us page here.")
                 ]
    
def populate_categories_initial(sender, instance, created, **kwargs):
    board = instance
    if created:
        for category, slug in initial_categories:
            Category.objects.create(board = board, slug=slug, name = category)
        
def populate_job_types_initial(sender, instance, created, **kwargs):
    board = instance
    if created:
        for job_type, slug in initial_job_types:
            JobType.objects.create(board = board, slug=slug, name = job_type)
        
        
def populate_pages_initial(sender, instance, created, **kwargs):
    "Populate the pages when the board is first created"
    board = instance      
    if created:
        for title, content in initial_pages:
            Page.objects.create(board = board, title = title, content = content)
    

    
          
    
def model_delete(model_obj):
        "Never delete"
        d = DeletedEntities()
        d.content_object = model_obj
        d.board = model_obj.board
        d.save()
        model_obj.is_deleted = True
        model_obj.save()
        

    
def create_initial_jobs(board):
    job_details = {
        "name":"This is a sample Job post.",
        "description": """You can edit it, or delete it. <p>You can format yout text. <strong>This is bold, for example</b></p>
        """,
        "Location": "Anywhere",
        "Company": "Acme, Inc",
        "Approximate Budget": "Depends",
        "Company Url": "http://example.com",  
        
        
    }    
    
    job_contact_details = {
        "name": "Jane Smith",
        "email": "jane@example.com"                       
    }
    category = board.category_set.all()[0]
    job_type = board.jobtype_set.all()[0]
    job = Job.objects.create(name = job_details["name"], 
                       description = job_details["description"],
                       board = board,
                       category = category,
                       job_type = job_type,
                       )
    for name, value in job_details.items():
        if not name in ["name", "description"]:
            JobData.objects.create(name = name, value = value, data_type="TextField", job = job)
    JobContactDetail.objects.create(name = job_contact_details["name"], email=job_contact_details["email"], job=job)
    
def populate_initial_jobs(sender, instance, created, **kwargs):
    board = instance
    create_initial_jobs(board)
        

    
from django.db.models.signals import post_save

#Populate the database with initial things.

post_save.connect(populate_job_board_form_initial, sender = Board)
post_save.connect(populate_categories_initial, sender = Board)
post_save.connect(populate_job_types_initial, sender = Board)
post_save.connect(populate_pages_initial, sender = Board)
post_save.connect(populate_initial_jobs, sender = Board)

    
    