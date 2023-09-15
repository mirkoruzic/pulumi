import pulumi
from components import s3
from pulumi import Config

config = Config()

# Load the S3 configurations
s3_configurations = config.require_object('S3')

for config in s3_configurations:
    bucket_name = config['bucket_name']
    s3_iam_policies = config.get('s3_iam_policy', [])
    public_available = config.get('public_available', False)

    s3.create_s3_bucket(bucket_name, s3_iam_policies, public_available)
