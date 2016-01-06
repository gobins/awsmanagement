import logging
import boto3

from cliff.command import Command
from awsmanagement import helper


class Update_wrk(Command):
    """ This class is for updating the wrk for all machines in the subnet.
        It will also update the wrk of all the volumes
        that are attached to the machines."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Update_wrk, self).get_parser(prog_name)

        parser.add_argument(
            '--wrk',
            required=True,
            help='The WRK value , e.g. WRK123456'
        )
        parser.add_argument(
            '--environment',
            required=True,
            help='The name of the environment , e.g. Env170'
        )
        return parser

    def take_action(self, parsed_args):
        environment = parsed_args.environment
        wrk = parsed_args.wrk
        self.log.info('Environment is %s', environment)

        ec2_client = self.app.client.ec2_client()
        try:
            subnet_id = helper.get_subnet_id_by_name(ec2_client, environment)
            subnet = self.app.client.ec2_subnet_resource(subnet_id)
            helper.update_tag(subnet, 'WRK', wrk)
            self.log.debug('Getting a list of all instances in the subnet')
            instances = subnet.instances.all()
            for instance in instances:
                helper.update_tag(instance, 'WRK', wrk)
                volumes = instance.volumes.all()
                for volume in volumes:
                    helper.update_tag(volume, 'WRK', wrk)

        except ValueError as err:
            self.log.error(err.args)
