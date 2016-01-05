"""
This module will define all the helper functions specific to AWS Infrastructure.
"""


def get_subnet_id_by_name(ec2_client, name):
    response = ec2_client.describe_subnets(Filters=[{'Name'=name}])
    subnets = response['Subnets']
    subnet = subnets[0]
    subnet_id = subnet['SubnetId']

