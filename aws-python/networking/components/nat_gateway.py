## networking/components/nat.py


import pulumi
from pulumi_aws import ec2

class NatGatewayComponent:
    def __init__(self, private_subnet):
        # Create an Elastic IP for the NAT Gateway
        stack_name = pulumi.get_stack()
        elastic_ip = ec2.Eip(f"{stack_name}-nat-gateway-eip")

        # Create a NAT Gateway in the private subnet with the Elastic IP
        self.nat_gateway = ec2.NatGateway(
            "f{stack_name}-nat-gateway-eip",
            subnet_id=private_subnet.id,
            allocation_id=elastic_ip.id,
            opts=pulumi.ResourceOptions(
                parent=private_subnet,  # Set private subnet as the parent
            )
        )
