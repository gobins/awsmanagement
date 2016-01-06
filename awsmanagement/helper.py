"""
This module will define all the helper \
functions specific to AWS Infrastructure.
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

def update_tag(client, key, value):
    log = logging.getLogger(__name__)
    log.debug('Updating WRK tag for the subnet')
    client.create_tags(
        Tags=[
            {
                'Key': key,
                'Value': value
            },
        ]
    )

def parse_subnets_data(subnets):
    log = logging.getLogger(__name__)
    subnets_data = []
    for subnet in subnets:
        parsed_data = {}
        parsed_data['subnet_id'] = subnet['SubnetId']
        parsed_data['cidr_block'] = subnet['CidrBlock']
        tags = subnet['Tags']
        name_flag = False
        wrk_flag = False
        log.debug('Parsing data for subnet %s', subnet['SubnetId'])
        for tag in tags:
            if tag['Key'] == "Name":
                parsed_data['subnet_name'] = tag['Value']
                name_flag = True
            if tag['Key'] == 'WRK':
                parsed_data['subnet_wrk'] = tag['Value']
                wrk_flag = True
        if name_flag is False:
            parsed_data['subnet_name'] = "None"
        if wrk_flag is False:
            parsed_data['subnet_wrk'] = "None"
        subnets_data.append(parsed_data)
    return subnets_data
