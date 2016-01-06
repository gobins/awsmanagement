import logging
from boto3.session import Session


class Client(object):
    log = logging.getLogger(__name__)

    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region,
                 verify=False):
        self.app_session = self.get_app_session(aws_access_key_id,
                                                aws_secret_access_key,
                                                aws_region)
        self.ec2_resource = self.get_ec2_resource()
        self.s3_resource = self.get_s3_resource()

    def get_app_session(self,
                        aws_access_key_id,
                        aws_secret_access_key,
                        aws_region):
        self.log.info('Getting AWS app session')
        app_session = Session(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)
        return app_session

    def get_ec2_resource(self):
        self.log.info('Getting AWS EC2 session')
        ec2_resource = self.app_session.resource('ec2', verify=False)
        return ec2_resource

    def ec2_client(self):
        self.log.debug("Creating an ec2 client object")
        ec2_client = self.app_session.client('ec2', verify=False)
        return ec2_client

    def ec2_subnet_resource(self, subnet_id):
        self.log.debug("Creating a ec2 Subnet resource object")
        subnet_resource = self.ec2_resource.Subnet(subnet_id)
        return subnet_resource

    def ec2_tag(self, resource_id, key, value):
        self.log.debug("Creating a ec2 Tag resource object")
        subnet_resource = self.ec2_resource.Tag(resource_id, key, value)
        return subnet_resource

    def ec2_volume(self, volume_id):
        self.log.debug("Creating a ec2 Volume resource object")
        volume_resource = self.ec2_resource.Volume(volume_id)
        return volume_resource

    def ec2_vpc(self, vpc_id):
        self.log.debug("Creating a ec2 Vpc resource object")
        vpc_resource = self.ec2_resource.Vpc(vpc_id)
        return vpc_resource

    def ec2_keypair(self, keypair_name):
        self.log.debug("Creating a ec2 Keypair resource object")
        keypair_resource = self.ec2_resource.Keypair(keypair_name)
        return keypair_resource

    def ec2_image(self, image_id):
        self.log.debug("Creating a ec2 Image resource object")
        image_resource = self.ec2_resource.Image(image_id)
        return image_resource

    def ec2_instance(self, instance_id):
        self.log.debug("Creating a ec2 Instance resource object")
        instance_resource = self.ec2_resource.Instance(instance_id)
        return instance_resource

    def get_s3_resource(self):
        self.log.info('Getting AWS S3 session')
        s3_resource = self.app_session.resource('s3', verify=False)
        return s3_resource

    def get_instances_by_subnet(subnet_id):
        self.log.info('Retrieving all instances for subnet %s', subnet_id)
        subnet_resource = self.ec2_subnet_resource(subnet_id)
        return subnet_resource.instances.all()
