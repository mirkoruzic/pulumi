## networking/components/vpc.py


import pulumi
from pulumi_aws import ec2

class VPCComponent:
    def __init__(self, name, cidr_block, public_subnet_cidr, private_subnet_cidr):
        self.vpc = ec2.Vpc(name + "-vpc", cidr_block=cidr_block)
        self.public_subnet = ec2.Subnet(
            name + "-public-subnet",
            cidr_block=public_subnet_cidr,
            vpc_id=self.vpc.id,
            tags={"Name": name + "-public-subnet"},
            opts=pulumi.ResourceOptions(parent=self.vpc)  # Set VPC as the parent
        )
        self.private_subnet = ec2.Subnet(
            name + "-private-subnet",
            cidr_block=private_subnet_cidr,
            vpc_id=self.vpc.id,
            tags={"Name": name + "-private-subnet"},
            opts=pulumi.ResourceOptions(parent=self.vpc)  # Set VPC as the parent
        )

        # Create Internet Gateway
        stack_name = pulumi.get_stack()
        self.internet_gateway = ec2.InternetGateway(
            f"{stack_name}-internet-gateway",
            vpc_id=self.vpc.id,  # Attach the Internet Gateway to the VPC
         opts=pulumi.ResourceOptions(parent=self.vpc)  # Set VPC as the parent
        )
