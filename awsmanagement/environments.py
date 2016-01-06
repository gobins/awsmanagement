import logging
from awsmanagement import helper
from cliff.lister import Lister


class GetEnvironments(Lister):
    log = logging.getLogger(__name__)

    # def get_parser(self, prog_name):
    #     parser = super(GetEnvironments, self).get_parser(prog_name)

    #     parser.add_argument(
    #         '--environment',
    #         required=True,
    #         help='The name of the environment , e.g. Env170'
    #     )

    #     return parser

    def take_action(self, parsed_args):
        ec2_client = self.app.client.ec2_client()
        response = ec2_client.describe_subnets()
        subnets = response['Subnets']

        subnets_data = helper.parse_subnets_data(subnets)
        if subnets_data:
            data = (
                (
                    subnet['subnet_name'],
                    subnet['cidr_block'],
                    subnet['subnet_wrk'],
                    subnet['subnet_id']
                ) for subnet in subnets_data
            )
            columns = (
                'Name',
                'CIDR Block',
                'WRK',
                'Subnet Id'
            )
            return columns, data
        else:
            return None


class GetInstances(Lister):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetInstances, self).get_parser(prog_name)

        parser.add_argument(
            '--environment',
            required=True,
            help='The name of the environment , e.g. Env170'
        )

        return parser

    def take_action(self, parsed_args):
        env_name = parsed_args.environment
        ec2_client = self.app.client.ec2_client()
        subnet_id = helper.get_subnet_id_by_name(ec2_client, env_name)
        subnet_resource = self.app.client.ec2_subnet_resource(subnet_id)
        instances = subnet_resource.instances.all()
        instances_data = helper.parse_instances_data(instances)

        if instances_data:
            data = (
                (
                    instance['Name'],
                    instance['State'],
                    instance['Wrk'],
                    instance['Launched_by']
                ) for instance in instances_data
            )
            columns = (
                'Name',
                'State',
                'WRK',
                'Launched_by'
            )
            return columns, data
        else:
            return None
