import pulumi
from pulumi_aws import ec2

class NatGatewayComponent:
    def __init__(self, public_subnet, private_subnets):
        # Create an Elastic IP for the NAT Gateway
        stack_name = pulumi.get_stack()
        elastic_ip = ec2.Eip(f"{stack_name}-nat-gateway-eip")

        # Create a NAT Gateway in the public subnet with the Elastic IP
        self.nat_gateway = ec2.NatGateway(
            f"{stack_name}-nat-gateway",
            subnet_id=public_subnet.id,
            allocation_id=elastic_ip.id,
            opts=pulumi.ResourceOptions(
                parent=public_subnet,  # Set public subnet as the parent
            ),
            tags={"Name": f"{stack_name}"}
        )

        # Define a route for the private subnets to use the NAT Gateway for internet access
        config = pulumi.Config()
        vpc_config = config.require_object("vpc")
        private_route_cidr_block = vpc_config["privateRouteCidr"]

        for i, private_subnet in enumerate(private_subnets):
            private_route_table = ec2.RouteTable(
                f"{stack_name}-nat-private-route-table-{i+1}",
                vpc_id=private_subnet.vpc_id,
                routes=[
                    ec2.RouteTableRouteArgs(
                        cidr_block=private_route_cidr_block,
                        nat_gateway_id=self.nat_gateway.id
                    )
                ],
                tags={"Name": f"{stack_name}-nat-private-route-table-{i+1}"},
            )

            # Associate the route table with the private subnet
            ec2.RouteTableAssociation(
                f"{stack_name}-nat-private-route-association-{i+1}",
                subnet_id=private_subnet.id,
                route_table_id=private_route_table.id,
            )
