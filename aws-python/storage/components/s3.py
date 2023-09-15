import pulumi
from pulumi_aws import s3
from .s3_policy import generate_public_read_policy, generate_s3_logging_policy

def create_s3_bucket(bucket_name, s3_iam_policies, public_available):
    # Create the S3 bucket
    bucket = s3.Bucket(bucket_name)
    
    # Determine Block Public Access settings based on public_available flag and apply them
    block_public_access = s3.BucketPublicAccessBlock(
        f"{bucket_name}-block-public-access",
        bucket=bucket.id,
        block_public_acls=not public_available,
        block_public_policy=not public_available,
        ignore_public_acls=not public_available,
        restrict_public_buckets=not public_available
    )

    # Generate and attach the bucket policy if public_available is set to true
    if public_available:
        policy = bucket.arn.apply(lambda arn: generate_public_read_policy(arn))
        s3.BucketPolicy(f'{bucket_name}-policy', bucket=bucket.id, policy=policy)

    if "s3_logging_policy" in s3_iam_policies:
        policy = bucket.arn.apply(lambda arn: generate_s3_logging_policy(arn))
        s3.BucketPolicy(f'{bucket_name}-log-read-policy', bucket=bucket.id, policy=policy)

    return bucket
