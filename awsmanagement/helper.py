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


def get_tag_value(tags, key):
    value = None
    for tag in tags:
        if tag['Key'] == key:
            value = tag['Value']
    return value


def parse_subnets_data(subnets):
    log = logging.getLogger(__name__)
    log.debug('Parsing data for subnets')
    subnets_data = []
    if subnets:
        for subnet in subnets:
            parsed_data = {}
            parsed_data['subnet_id'] = subnet['SubnetId']
            parsed_data['cidr_block'] = subnet['CidrBlock']
            tags = subnet['Tags']
            log.debug('Parsing data for subnet %s', subnet['SubnetId'])
            if tags:
                parsed_data['subnet_name'] = get_tag_value(tags, 'Name')
                parsed_data['subnet_wrk'] = get_tag_value(tags, 'WRK')
            else:
                parsed_data['subnet_name'] = "Not Set"
                parsed_data['subnet_wrk'] = "Not Set"
            subnets_data.append(parsed_data)
        return sorted(subnets_data, key=lambda k: k['subnet_name'])


def parse_instances_data(instances):
    log = logging.getLogger(__name__)
    instances_data = []
    if instances:
        log.debug('Parsing data for instances')
        log.debug(dir(instances))
        for instance in instances:
            log.debug('Parsing data for instance %s', instance.id)
            parsed_data = {}
            tags = instance.tags
            if tags:
                parsed_data['Name'] = get_tag_value(tags, 'Name')
                parsed_data['Wrk'] = get_tag_value(tags, 'WRK')
                parsed_data['State'] = instance.state['Name']
                parsed_data['Launched_by'] = get_tag_value(tags, 'Launched_by')
            else:
                parsed_data['Name'] = instance.id
                parsed_data['Wrk'] = "Not Set"
                parsed_data['State'] = "Not Set"
                parsed_data['Launched_by'] = "Not Set"
            instances_data.append(parsed_data)
    return sorted(instances_data, key=lambda k: k['Name'])
