import pulumi
from pulumi_aws import ec2
from pulumi import Config
from .nat_gateway import NatGatewayComponent

class VPCComponent:
    def __init__(self, name, cidr_block, public_subnet_cidr, private_subnet_cidr, private_subnet_cidr2, nat_gateway_component=None):
        config = Config()
        vpc_config = config.require_object("vpc")
        public_route_cidr_block = vpc_config["publicRouteCidr"]

        self.vpc = ec2.Vpc(name + "-vpc", cidr_block=cidr_block)
        
        self.public_subnet = ec2.Subnet(
            name + "-public-subnet",
            cidr_block=public_subnet_cidr,
            vpc_id=self.vpc.id,
            tags={"Name": name + "-public-subnet"},
            opts=pulumi.ResourceOptions(parent=self.vpc)
        )
        
        self.private_subnet = ec2.Subnet(
            name + "-private-subnet",
            cidr_block=private_subnet_cidr,
            vpc_id=self.vpc.id,
            tags={"Name": name + "-private-subnet"},
            availability_zone="eu-west-1a",

            opts=pulumi.ResourceOptions(parent=self.vpc)
        )

        self.private_subnet2 = ec2.Subnet(
            name + "-private-subnet2",
            cidr_block=private_subnet_cidr2,
            availability_zone="eu-west-1b",
            vpc_id=self.vpc.id,
            tags={"Name": name + "-private-subnet2"},
            opts=pulumi.ResourceOptions(parent=self.vpc)
        )

        stack_name = pulumi.get_stack()
        self.internet_gateway = ec2.InternetGateway(
            f"{stack_name}-internet-gateway",
            vpc_id=self.vpc.id,
            opts=pulumi.ResourceOptions(parent=self.vpc)
        )

        self.public_route_table = ec2.RouteTable(
            f"{name}-public-route-table",
            vpc_id=self.vpc.id,
            routes=[
                ec2.RouteTableRouteArgs(
                    cidr_block=public_route_cidr_block,
                    gateway_id=self.internet_gateway.id
                )
            ],
            tags={"Name": f"{stack_name}-public-route-table"}
        )

        # Associate the public route table with the public subnet
        ec2.RouteTableAssociation(
            f"{stack_name}-public-route-association",
            subnet_id=self.public_subnet.id,
            route_table_id=self.public_route_table.id,
            opts=pulumi.ResourceOptions(parent=self.public_route_table)
        )




    