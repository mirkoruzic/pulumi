import pulumi
import json

def generate_public_read_policy(bucket_arn):
    """Generate S3 public read policy for a specific bucket ARN."""
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"{bucket_arn}/*"]
        }]
    })

def generate_s3_logging_policy(bucket_name):
    """Generate S3 logging access policy for a specific bucket name."""
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "s3.amazonaws.com"
            },
            "Action": ["s3:PutObject"],
            "Resource": [f"{bucket_name}/*"],
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }]
    })
