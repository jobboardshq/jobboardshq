from django.test import TestCase
from django.contrib.auth.models import User


from zobpress.models import Board, JobFormModel, BoardSettings, Category,\
    JobType

from zobpress.models import initial_categories,initial_job_types,initial_pages



class TestBoard(TestCase):
    
    def setUp(self):
        self.user = get_test_user()
        self.board = Board.objects.register_new_board("box123", "The box", "Box industry", self.user)
        self.c = self.client
        
    def test_board_creation(self):
        """
        Test that a board can be created successfully.
        Also, a BoardSetting and default job form must be created by this time.
        """
        self.assertEqual(self.board.jobformmodel_set.count(), 1)
        self.assertEqual(BoardSettings.objects.count(), 1)
        
    def test_board_creation_initial_data(self):
        "Tests that the inital data in categories and job types is populated."
        new_board = Board.objects.register_new_board("asdfgh", "The box", "Box industry", self.user)
        self.assertEqual(new_board.category_set.count(), len(initial_categories))
        self.assertEqual(new_board.jobtype_set.count(), len(initial_job_types))
        
    def test_initial_job_is_active(self):
        self.assertEquals(self.board.job_set.filter(is_active=True).count(),1)
        
    def test_auto_slug(self):
        JobType.objects.create(name='jobtype',board=self.board)
        new_board = Board.objects.register_new_board("asdfgh", "The box", "Box industry", self.user)
        jobtype1 = JobType.objects.create(name='jobtype',board=new_board)
        self.assertEquals(jobtype1.slug,'jobtype')
        jobtype2 = JobType.objects.create(name='jobtype',board=new_board)
        self.assertEquals(jobtype2.slug,'jobtype-2')
        
        
        
class JobTypeSlugPopulate(TestCase):
    
    def setup(self):
        user = get_test_user()
        board = Board.objects.register_new_board("box123", "The box", "Box industry", user)
        c = self.client
        #c.login()
    
    def create_a_job_type(self):
        from zobpress.forms import JobTypeForm
        form = JobTypeForm(board=board,data={'name':'job complex type_this'})
        assert form.is_valid()
        assert form.save()
        
        
        
def get_test_user():
    user, created = User.objects.get_or_create(username = "test")
    return user        