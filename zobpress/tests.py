from django.test import TestCase
from django.contrib.auth.models import User


from zobpress.models import Board, JobFormModel, BoardSettings, Category,\
    JobType



class TestBoard(TestCase):
    
    def test_board_creation(self):
        """
        Test that a board can be created successfully.
        Also, a BoardSetting and default job form must be created by this time.
        """
        user = get_test_user()
        board = Board.objects.register_new_board("box123", "The box", "Box industry", user)
        self.assertEqual(board.jobformmodel_set.count(), 1)
        self.assertEqual(BoardSettings.objects.count(), 1)
        
    def test_board_creation_initial_data(self):
        "Tests that the inital data in categories and job types is populated."
        initial_category_count = Category.objects.count()
        initial_job_type_count = JobType.objects.count()
        user = get_test_user()
        board = Board.objects.register_new_board("box123", "The box", "Box industry", user)
        self.assertNotEqual(board.category_set.count(), initial_category_count)
        self.assertNotEqual(board.jobtype_set.count(), initial_job_type_count)
        
        
    
        
        
def get_test_user():
    user, created = User.objects.get_or_create(username = "test")
    return user        