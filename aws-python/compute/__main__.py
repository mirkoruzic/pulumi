import pulumi
from components.ec2_instance import EC2Component
from pulumi import Config, StackReference

def get_security_group_ids(security_group_names):
    security_group_ids = []
    for sg_name in security_group_names:
        sg_id = networking_stack.output[f"{sg_name}_security_group_id"]
        security_group_ids.append(sg_id)
    return security_group_ids

# Read configuration
config = Config()
ec2_instances = config.require_object("ec2_instances")

# Get the current stack's name
current_stack = pulumi.get_stack()

# Reference the networking stack using the same stack name
networking_stack = StackReference(f"mruzic/networking/{current_stack}")

# Loop through the EC2 instances defined in the configuration
for ec2_instance_config in ec2_instances:
    name = ec2_instance_config["name"]
    number = ec2_instance_config["number"]
    ami = ec2_instance_config["ami"]
    instance_type = ec2_instance_config["instanceType"]
    subnet_type = ec2_instance_config["subnetType"]
    security_group_names = ec2_instance_config["securityGroupName"]

    # Get security group IDs based on names
    security_group_ids_list = get_security_group_ids(security_group_names)

    # Based on the subnet type, decide which subnet ID to use
    if subnet_type == "public":
        subnet_id = networking_stack.output.public_subnet_id
    elif subnet_type == "private":
        subnet_id = networking_stack.output.private_subnet_id
    else:
        raise Exception("Invalid subnet type. It must be 'public' or 'private'.")

    # Create the number of EC2 instances specified
    for i in range(1, number + 1):
        ec2_name = f"{name}-{i+1:02}"  # Create unique name for each instance
        ec2_component = EC2Component(
            ec2_name=ec2_name,
            ami=ami,
            instance_type=instance_type,
            subnet_id=subnet_id,
            security_group_id=security_group_ids_list
        )

        # Export the EC2 instance details
        pulumi.export(f"{ec2_name}_id", ec2_component.ec2_instance.id)
        pulumi.export(f"{ec2_name}_private_ip", ec2_component.ec2_instance.private_ip)
        pulumi.export(f"{ec2_name}_public_ip", ec2_component.ec2_instance.public_ip if subnet_type == "public" else "N/A")
        pulumi.export(f"{ec2_name}_private_dns", ec2_component.ec2_instance.private_dns)
        pulumi.export(f"{ec2_name}_public_dns", ec2_component.ec2_instance.public_dns if subnet_type == "public" else "N/A")
