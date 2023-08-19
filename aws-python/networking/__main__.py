## networking/__main__.py

import pulumi
from components.vpc import VPCComponent
from components.nat_gateway import NatGatewayComponent
#from components.internet_gateway import InternetGatewayComponent
from components.security_group import SecurityGroupComponent
from pulumi_aws import ec2


pulumi_config = pulumi.Config()


def load_config():
    pulumi_config = pulumi.Config()
    return pulumi_config.require_object("vpc")

vpc_config = load_config()

# Create VPCComponent first (without the NAT gateway)
vpc = VPCComponent(
    name=vpc_config["vpcName"],
    cidr_block=vpc_config["vpcCidrBlock"],
    public_subnet_cidr=vpc_config["publicSubnetCidr"],
    private_subnet_cidr=vpc_config["privateSubnetCidr"]
)

# Create NatGatewayComponent
nat_gateway_component = NatGatewayComponent(
    private_subnet=vpc.private_subnet
)

# Update the VPC component with the NAT gateway component
vpc.set_nat_gateway(nat_gateway_component)

# Define outputs for VPC and subnets
pulumi.export("vpc_id", vpc.vpc.id)
pulumi.export("public_subnet_id", vpc.public_subnet.id)
pulumi.export("private_subnet_id", vpc.private_subnet.id)

# Define outputs for NAT Gateway
pulumi.export("nat_gateway_id", nat_gateway_component.nat_gateway.id)
pulumi.export("nat_gateway_ip", nat_gateway_component.nat_gateway.public_ip)

# Define outputs for the Internet Gateway
pulumi.export("internet_gateway_id", vpc.internet_gateway.id)

# Create Security Groups
security_groups_config = pulumi_config.require_object("security_groups")
vpc_id = vpc.vpc.id

for sg_config in security_groups_config:
    security_group_component = SecurityGroupComponent(
        vpc_id=vpc_id,
        name=sg_config['name'],
        inbound_port=sg_config['inbound_port'],
        outbound_port=sg_config['outbound_port'],
        inbound_cidr=sg_config['inbound_cidr'],
        outbound_cidr=sg_config['outbound_cidr'],
        protocol=sg_config['protocol']
    )

    pulumi.export(f"{sg_config['name']}_security_group_id", security_group_component.security_group.id)
    pulumi.export(f"{sg_config['name']}_security_group_name", sg_config['name'])
