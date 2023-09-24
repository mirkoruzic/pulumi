import pulumi
import os
import boto3
import utils
from components.ec2_instance import EC2Component
from components.eks import EKSComponent
from pulumi import Config, StackReference, Output
from collections import defaultdict
from pulumi_aws import eks
from utils import get_security_group_ids


# Read configuration
config = Config()
ec2_instances = config.require_object("ec2_instances")
eks_cluster = config.require_object("eks_cluster")
ssh_key_name = eks_cluster["node_groups"][0]["ssh_key_name"]
ec2_client = boto3.client('ec2')
response = ec2_client.describe_availability_zones()
num_azs = len(response['AvailabilityZones'])


# Get the current stack's name
current_stack = pulumi.get_stack()

# Reference the networking stack using the same stack name
org_name = os.environ.get("PULUMI_ORG_NAME", "default_org_name")
networking_stack = StackReference(f"{org_name}/networking/{current_stack}")
identity_stack = StackReference(f"{org_name}/identity/{current_stack}")



total_monthly_costs = defaultdict(float)

for ec2_instance_config in ec2_instances:
    name = ec2_instance_config["name"]
    number = ec2_instance_config["number"]
    ami = ec2_instance_config["ami"]
    instance_type = ec2_instance_config["instanceType"]
    subnet_type = ec2_instance_config["subnetType"]
    security_group_names = ec2_instance_config["securityGroupName"]
    ssh_key_name = ec2_instance_config["use_ssh"]  # Get the SSH key name from the configuration

    associate_public_ip = ec2_instance_config.get("associatePublicIp", False) if subnet_type == "public" else False

    # Get security group IDs based on names
    security_group_ids_list = get_security_group_ids(security_group_names, networking_stack)

    subnet_ids = {
        "public1": "public_subnet_id_1",
        "public2": "public_subnet_id_2",
        "public3": "public_subnet_id_3",
        "private1": "private_subnet_id_1",
        "private2": "private_subnet_id_2",
        "private3": "private_subnet_id_3"
    }

    try:
        subnet_id = networking_stack.get_output(subnet_ids[subnet_type])
    except KeyError:
        raise Exception("Invalid subnet type. It must be 'public' or 'private' with numeric order.")
    
    static_private_ips = ec2_instance_config.get("staticPrivateIp", [])

    if static_private_ips == "none":
        static_private_ips = ["none"] * number  # Create a list of 'none' values to represent auto-assign
    elif not isinstance(static_private_ips, list):
        raise ValueError(f"'staticPrivateIp' for {name} should be either 'none' or a array of IPs.")

    if len(static_private_ips) != number:
        raise Exception(f"Number of static IPs provided ({len(static_private_ips)}) does not match the number of instances ({number}) for {name}.")

    
    def create_ec2_instances(security_group_ids_list, name, number, ami, instance_type, subnet_id, subnet_type, ssh_key_name, associate_public_ip, static_private_ips):

        # Create the number of EC2 instances specified
        global total_monthly_cost
            # Set hostname using user_data


        for i in range(number):
            ec2_name = f"{name}-{i+1:02}"  # Create unique name for each instance

            ec2_component = EC2Component(
                ec2_name=ec2_name,
                ami=ami,
                instance_type=instance_type,
                subnet_id=subnet_id,
                security_group_id=security_group_ids_list,
                ssh_key_name=ssh_key_name,  # Pass the SSH key name
                associate_public_ip=associate_public_ip,
                private_ip=static_private_ips[i] if static_private_ips[i] != "none" else None


            )

            total_monthly_costs[name] += ec2_component.monthly_cost


            # Export the EC2 instance details
            #pulumi.export(f"{ec2_name}_id", ec2_component.ec2_instance.id)
            #pulumi.export(f"{ec2_name}_private_ip", ec2_component.ec2_instance.private_ip)
            #pulumi.export(f"{ec2_name}_public_ip", ec2_component.ec2_instance.public_ip if subnet_type == "public" else "N/A")
            #pulumi.export(f"{ec2_name}_private_dns", ec2_component.ec2_instance.private_dns)
            #pulumi.export(f"{ec2_name}_public_dns", ec2_component.ec2_instance.public_dns if subnet_type == "public" else "N/A")
            pulumi.export(f"{ec2_name}_hourly_cost", ec2_component.hourly_cost) # Exporting the hourly cost
            pulumi.export(f"{ec2_name}_daily_cost", ec2_component.daily_cost)   # Exporting the daily cost
            pulumi.export(f"{ec2_name}_monthly_cost", ec2_component.monthly_cost) # Exporting the monthly cost

            


    create_ec2_instances(security_group_ids_list, name, number, ami, instance_type, subnet_id, subnet_type, ssh_key_name, associate_public_ip, static_private_ips)

for group_name, group_total_monthly_cost in total_monthly_costs.items():
    pulumi.export(f"{group_name}_total_monthly_cost", group_total_monthly_cost)


#### EKS ########

# eks_node_groups = eks_cluster["node_groups"]
# eks_subnet_id_1 = networking_stack.get_output("private_subnet_id_1")
# eks_subnet_id_2 = networking_stack.get_output("private_subnet_id_2")
# eks_subnet_id_3 = networking_stack.get_output("private_subnet_id_3")



# eks_vpc_config = eks.ClusterVpcConfigArgs(
#     public_access_cidrs=['0.0.0.0/0'],
#     security_group_ids=get_security_group_ids(eks_cluster['node_groups'][0]['securityGroupName'], networking_stack),
#     subnet_ids=[eks_subnet_id_1,eks_subnet_id_2,eks_subnet_id_3],
# )

# eks_cluster_config = config.require_object('eks_cluster')
# # Get IAM role ARNs from the identity stack
# eks_role_arn = identity_stack.get_output("eks_role_arn")
# ec2_role_arn = identity_stack.get_output("ec2_role_arn")

# # Create EKS Cluster and Node Groups
# eks_component = EKSComponent(
#     name=f"{current_stack}-eks-cluster",
#     version=eks_cluster_config['version'],
#     node_groups=eks_cluster_config['node_groups'],
#     vpc_config=eks_vpc_config,
#     role_arn=eks_role_arn,
#     node_role_arn=ec2_role_arn,
# )

# # Export kubeconfig
# pulumi.export('cluster-name', eks_component.cluster.name)
# pulumi.export('kubeconfig', utils.generate_kube_config(eks_component.cluster))
####### EKS ########
