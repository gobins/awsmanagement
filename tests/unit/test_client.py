import unittest
import boto3

from mock import patch, Mock
from awsmanagement.client import Client


class Test_Client(unittest.TestCase):

    @patch('botocore.session')
    def test_constructor_with_verify(self, Mock):
        my_client = Client(
                        aws_access_key_id='test',
                        aws_secret_access_key='test',
                        aws_region='test',
                        verify=True,
                        )

        self.assertIsInstance(my_client, Client)

    @patch('botocore.session')
    def test_get_ec2_session(self, Mock):
        my_client = Client(
                        aws_access_key_id='test',
                        aws_secret_access_key='test',
                        aws_region='test',
                        )

        app_session = my_client.get_app_session()
        ec2_session = my_client.get_ec2_session(app_session)
        self.assertIsInstance(app_session, boto3.session.Session)
