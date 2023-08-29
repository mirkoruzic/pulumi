import pulumi
from pulumi import Config
from components.ssh_key import SshKey
from components.eks_iam import EKSIAMComponent

# Read the configuration
config = Config()

# Retrieve the ssh_keys
ssh_keys = config.get_object("ssh_keys")

# Create the SSH keys using the SshKey component
if ssh_keys:
    for key_name, public_key in ssh_keys.items():
        SshKey(key_name, public_key)

eks_iam_component = EKSIAMComponent("EKSIAMComponent")

# Export the IAM roles
pulumi.export('eks_role_arn', eks_iam_component.eks_role.arn)
pulumi.export('ec2_role_arn', eks_iam_component.ec2_role.arn)