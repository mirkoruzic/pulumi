import pulumi
from pulumi_aws import eks

current_stack = pulumi.get_stack()

class EKSComponent(pulumi.ComponentResource):

    def __init__(self, name, version, node_groups, vpc_config, role_arn, node_role_arn, opts=None):
        super().__init__('custom:EKSComponent', name, None, opts)
        
        self.cluster = eks.Cluster(
            'cluster',
            name=name,
            role_arn=role_arn,
            version=version,
            tags={
                'Name':  f"{current_stack}" + name,
            },
            vpc_config=vpc_config,
        )
        
        for ng in node_groups:
            node_group = eks.NodeGroup(
            ng['name'],
            cluster_name=self.cluster.name,
            node_role_arn=node_role_arn,
            subnet_ids=vpc_config.subnet_ids,
            scaling_config=eks.NodeGroupScalingConfigArgs(
                desired_size=ng['desiredCapacity'],
                max_size=ng['maxSize'],
                min_size=ng['minSize'],
            ),
            tags={
                'Name': f'{name}-{ng["name"]}',
            },
        )
        
        self.register_outputs({})
