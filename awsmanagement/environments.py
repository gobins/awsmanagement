import logging

from cliff.lister import Lister


class Environments(Lister):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Environments, self).get_parser(prog_name)

        parser.add_argument(
            '--environment',
            required=True,
            help='The name of the environment , e.g. Env170'
        )

        return parser

    def take_action(self, parsed_args):
        environment = parsed_args.environment
        self.log.info('Environment is %s', environment)
        ec2_client = self.app.client.ec2_client()
        subnets = ec2_client.describe_subnets()

        for subnet in subnets:
            data = 
        if subnets:
            data = ((n['sr'], n['comment_karma'], n['link_karma']) for n in mykarma.data)
            columns = (
                'Name',
                'WRK',
                'CIDR'
            )
            return columns, data
        else:
            return None

            subnet_id = helper.get_subnet_id_by_name(ec2_client, environment)
            subnet = self.app.client.ec2_subnet_resource(subnet_id)
            self.log.debug('Updating WRK tag for the subnet')
            subnet.create_tags(
                DryRun=True,
                Tags=[
                    {
                        'Key' : 'WRK',
                        'Value' : wrk
                    },
                ]
            )

            self.log.debug('Getting a list of all instances in the subnet')
            instances = subnet.instances.all()
            for instance in instances:
                instance.create_tags(
                    DryRun=True,
                    Tags=[
                        {
                            'Key': 'WRK',
                            'Value': wrk
                        },
                    ]
                )

