import pulumi
from pulumi_aws import ec2

class EC2Component:
    def __init__(self, ec2_name, ami, instance_type, subnet_id, security_group_id):
        self.ec2_instance = ec2.Instance(
            ec2_name,
            ami=ami,
            instance_type=instance_type,
            subnet_id=subnet_id,
            vpc_security_group_ids=security_group_id  # List of security group IDs
        )
