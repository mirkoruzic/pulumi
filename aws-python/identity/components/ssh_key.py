from pulumi import Input
import pulumi_aws as aws

class SshKey(aws.ec2.KeyPair):
    def __init__(self, key_name: Input[str], public_key: Input[str]):
        full_name = key_name  # Using the exact name from the YAML
        super().__init__(full_name, public_key=public_key)
