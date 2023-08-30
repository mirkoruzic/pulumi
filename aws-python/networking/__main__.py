## networking/__main__.py

import pulumi
from components.vpc import VPCComponent
from components.nat_gateway import NatGatewayComponent
from components.security_group import SecurityGroupComponent
from pulumi_aws import ec2

##### Create VPCComponent #####

pulumi_config = pulumi.Config()
vpc_config = pulumi_config.require_object("vpc")
vpc = VPCComponent(name=vpc_config["vpcName"])

pulumi.export("vpc_id", vpc.vpc.id)
for i, subnet in enumerate(vpc.public_subnet):
    pulumi.export(f"public_subnet_id_{i+1}", subnet.id)
for i, subnet in enumerate(vpc.private_subnet):
    pulumi.export(f"private_subnet_id_{i+1}", subnet.id)

pulumi.export("internet_gateway_id", vpc.internet_gateway.id)
################################

##### Create NatGatewayComponent #####
nat_gateway_component = NatGatewayComponent(
    public_subnet=vpc.public_subnet[0],  # First public subnet
    private_subnets=vpc.private_subnet,  # List of private subnets
)

pulumi.export("nat_gateway_id", nat_gateway_component.nat_gateway.id)
pulumi.export("nat_gateway_ip", nat_gateway_component.nat_gateway.public_ip)
#####################################

##### Create SecurityGroupComponent #####
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
################################