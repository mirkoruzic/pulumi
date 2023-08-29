from pulumi_aws import config, iam
import json
import pulumi

class EKSIAMComponent(pulumi.ComponentResource):

    def __init__(self, name, opts=None):
        super().__init__('custom:resources:EKSIAMComponent', name, None, opts)

        # EKS Cluster Role
        self.eks_role = iam.Role(
            'eks-iam-role',
            assume_role_policy=json.dumps({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'sts:AssumeRole',
                        'Principal': {
                            'Service': 'eks.amazonaws.com'
                        },
                        'Effect': 'Allow',
                        'Sid': ''
                    }
                ],
            }),
            opts=pulumi.ResourceOptions(parent=self),
        )

        iam.RolePolicyAttachment(
            'eks-service-policy-attachment',
            role=self.eks_role.id,
            policy_arn='arn:aws:iam::aws:policy/AmazonEKSServicePolicy',
            opts=pulumi.ResourceOptions(parent=self),
        )

        iam.RolePolicyAttachment(
            'eks-cluster-policy-attachment',
            role=self.eks_role.id,
            policy_arn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy',
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Ec2 NodeGroup Role
        self.ec2_role = iam.Role(
            'ec2-nodegroup-iam-role',
            assume_role_policy=json.dumps({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'sts:AssumeRole',
                        'Principal': {
                            'Service': 'ec2.amazonaws.com'
                        },
                        'Effect': 'Allow',
                        'Sid': ''
                    }
                ],
            }),
            opts=pulumi.ResourceOptions(parent=self),
        )

        iam.RolePolicyAttachment(
            'eks-workernode-policy-attachment',
            role=self.ec2_role.id,
            policy_arn='arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
            opts=pulumi.ResourceOptions(parent=self),
        )

        iam.RolePolicyAttachment(
            'eks-cni-policy-attachment',
            role=self.ec2_role.id,
            policy_arn='arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
            opts=pulumi.ResourceOptions(parent=self),
        )

        iam.RolePolicyAttachment(
            'ec2-container-ro-policy-attachment',
            role=self.ec2_role.id,
            policy_arn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly',
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.register_outputs({})
