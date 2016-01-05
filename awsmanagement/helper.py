"""
This module will define all the helper functions specific to AWS Infrastructure.
"""
import logging

def get_subnet_id_by_name(ec2_client, env_name):
    log = logging.getLogger(__name__)
    log.debug('Retrieving subnet_id for environment %s', env_name)
    response = ec2_client.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [env_name]
            },
        ]
    )
    subnets = response['Subnets']
    if not subnets:
        raise ValueError('Subnet with name %s not found', env_name)
    else:
        subnet = subnets[0]
        subnet_id = subnet['SubnetId']
        log.debug('Subnet id is %s', subnet_id)
        return subnet_id

