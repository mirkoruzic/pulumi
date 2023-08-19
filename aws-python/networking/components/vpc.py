import pulumi
from pulumi_aws import ec2
from pulumi import Config
from .nat_gateway import NatGatewayComponent

class VPCComponent:
    def __init__(self, name, cidr_block, public_subnet_cidr, private_subnet_cidr, nat_gateway_component=None):
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

        if nat_gateway_component:
            self.set_nat_gateway(nat_gateway_component)

    def set_nat_gateway(self, nat_gateway_component: NatGatewayComponent):
        config = Config()
        vpc_config = config.require_object("vpc")
        private_route_cidr_block = vpc_config["privateRouteCidr"] # Retrieve the privateRouteCidr here

        self.private_route_table = ec2.RouteTable(
            f"{pulumi.get_stack()}-private-route-table",
            vpc_id=self.vpc.id,
            routes=[
                ec2.RouteTableRouteArgs(
                    cidr_block=private_route_cidr_block,
                    nat_gateway_id=nat_gateway_component.nat_gateway.id
                )
            ],
            tags={"Name": f"{pulumi.get_stack()}-private-route-table"},
        )

        ec2.RouteTableAssociation(
            f"{pulumi.get_stack()}-private-route-association",
            subnet_id=self.private_subnet.id,
            route_table_id=self.private_route_table.id
        )
