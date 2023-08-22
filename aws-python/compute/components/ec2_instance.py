import boto3
import json
from pulumi_aws import ec2
from pulumi import Config

REGION_MAPPING = {
    "eu-west-1": "EU (Ireland)"
    # Add other regions as needed
}

class EC2Component:
    def __init__(self, ec2_name, ami, instance_type, subnet_id, security_group_id, associate_public_ip=False):
        config = Config("compute")
        ec2_instances_config = config.require_object("ec2_instances")

        number_of_instances = next((instance["number"] for instance in ec2_instances_config if instance["name"] == ec2_name), 1)

        price_per_hour = self.get_on_demand_instance_price(instance_type, "eu-west-1")
        daily_cost = price_per_hour * 24 * number_of_instances
        monthly_cost = daily_cost * 30

        self.ec2_instance = ec2.Instance(
            ec2_name,
            instance_type=instance_type,
            ami=ami,
            subnet_id=subnet_id,
            vpc_security_group_ids=security_group_id,
            associate_public_ip_address=associate_public_ip,
            tags={"Name": ec2_name}
        )

        self.hourly_cost = price_per_hour
        self.daily_cost = daily_cost
        self.monthly_cost = monthly_cost

    @staticmethod
    def get_on_demand_instance_price(instance_type, region):
        client = boto3.client('pricing', region_name='us-east-1')

        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': REGION_MAPPING.get(region, region)},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
            # Additional filters as required for On-Demand pricing
        ]

        price = client.get_products(
            ServiceCode='AmazonEC2',
            Filters=filters,
            MaxResults=1
        )

        try:
            price_data = json.loads(price['PriceList'][0])
            on_demand_pricing = price_data['terms']['OnDemand']
            item_key = next(iter(on_demand_pricing))
            price_dimensions = on_demand_pricing[item_key]['priceDimensions']
            price_dimension_key = next(iter(price_dimensions))
            price_per_hour = float(price_dimensions[price_dimension_key]['pricePerUnit']['USD'])
        except (IndexError, KeyError):
            print("Could not find the On-Demand price for the specified instance type and region.")
            price_per_hour = 0

        return price_per_hour
