import pulumi
import boto3
from pulumi_aws import ec2
from pulumi import Config

class VPCComponent:
    def __init__(self, name):
        config = Config()
        vpc_config = config.require_object("vpc")

        availability_zones = get_availability_zones(vpc_config['region'])
        total_azs = len(availability_zones)
        subnet_cidrs = generate_subnets(vpc_config['vpcCidrBlock'], total_azs)
        
        self.vpc = ec2.Vpc(name + "-vpc", cidr_block=vpc_config['vpcCidrBlock'])
        
        self.public_subnet = []
        self.private_subnet = []
        
        for i in range(total_azs):
            self.public_subnet.append(ec2.Subnet(
                name + f"-public-subnet-{i+1}",
                cidr_block=subnet_cidrs['public'][i],
                vpc_id=self.vpc.id,
                tags={"Name": name + f"-public-subnet-{i+1}"},
                availability_zone=availability_zones[i],
                opts=pulumi.ResourceOptions(parent=self.vpc)
            ))
            
            self.private_subnet.append(ec2.Subnet(
                name + f"-private-subnet-{i+1}",
                cidr_block=subnet_cidrs['private'][i],
                vpc_id=self.vpc.id,
                tags={"Name": name + f"-private-subnet-{i+1}"},
                availability_zone=availability_zones[i],
                opts=pulumi.ResourceOptions(parent=self.vpc)
            ))
        
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
                    cidr_block=vpc_config['publicRouteCidr'],
                    gateway_id=self.internet_gateway.id
                )
            ],
            tags={"Name": f"{stack_name}-public-route-table"}
        )

        # Associate the public route table with the public subnets
        for i, subnet in enumerate(self.public_subnet):
            ec2.RouteTableAssociation(
                f"{stack_name}-public-route-association-{i+1}",
                subnet_id=subnet.id,
                route_table_id=self.public_route_table.id,
                opts=pulumi.ResourceOptions(parent=self.public_route_table)
            )

def get_availability_zones(region_m):
    client = boto3.client('ec2', region_name=region_m)
    response = client.describe_availability_zones(Filters=[{'Name': 'region-name', 'Values': [region_m]}])
    availability_zones = [zone['ZoneName'] for zone in response['AvailabilityZones']]
    return availability_zones

def generate_subnets(vpc_cidr, total_azs):
    base_ip = vpc_cidr.split('.')[0]
    base_cidr = int(vpc_cidr.split('.')[2])
    subnet_cidrs = {
        'public': [],
        'private': []
    }
    
    for i in range(total_azs):
        subnet_cidrs['public'].append(f'{base_ip}.0.{base_cidr + i * 2}.0/24')
        subnet_cidrs['private'].append(f'{base_ip}.0.{base_cidr + i * 2 + 1}.0/24')
        
    return subnet_cidrs

