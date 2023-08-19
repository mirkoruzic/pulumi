from pulumi_aws import ec2

class EC2Component:
    def __init__(self, ec2_name, ami, instance_type, subnet_id, security_group_id, associate_public_ip=False):
        self.ec2_instance = ec2.Instance(
            ec2_name,
            instance_type=instance_type,
            ami=ami,
            subnet_id=subnet_id,
            vpc_security_group_ids=security_group_id,
            associate_public_ip_address=associate_public_ip,
            tags={"Name": ec2_name}  # Add this line to set the Name tag
        )
