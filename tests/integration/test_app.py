import unittest
from awsmanagement.main import AwsManagementApp


class Test_App(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.my_app = AwsManagementApp()
        #self.parser = my_app.build_option_parser()

    def test_without_args(self):
        self.my_app.run()
