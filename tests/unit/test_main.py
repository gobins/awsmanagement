import unittest
from awsmanagement.main import AwsManagementApp
from cliff.app import App


class Test_Main(unittest.TestCase):

    def test_constructor(self):
        my_app = AwsManagementApp()
        self.assertIsInstance(my_app, App)
