## networking/components/security_group.py


from pulumi_aws import ec2
import pulumi

class SecurityGroupComponent:
    def __init__(self, vpc_id, name, inbound_port, outbound_port, inbound_cidr, outbound_cidr, protocol):
        self.security_group = ec2.SecurityGroup(
            name,
            vpc_id=vpc_id,
            description=f"{name} security group",
            name=name,
             tags = {"Name" : name} # this is the name of the security group in AWS

        )

        # Handle "ALL" for ports
        inbound_from_port = inbound_port if inbound_port != "ALL" else 0
        inbound_to_port = inbound_port if inbound_port != "ALL" else 65535
        outbound_from_port = outbound_port if outbound_port != "ALL" else 0
        outbound_to_port = outbound_port if outbound_port != "ALL" else 65535

        # Inbound rule
        ec2.SecurityGroupRule(
            name + "-inbound-rule",
            security_group_id=self.security_group.id,
            type="ingress",
            protocol=protocol,
            from_port=inbound_from_port,
            to_port=inbound_to_port,
            cidr_blocks=[inbound_cidr],
            opts=pulumi.ResourceOptions(parent=self.security_group) # Set the security group as the parent

        )

        # Outbound rule
        if outbound_port and outbound_cidr:
            ec2.SecurityGroupRule(
                name + "-outbound-rule",
                security_group_id=self.security_group.id,
                type="egress",
                protocol=protocol,
                from_port=outbound_from_port,
                to_port=outbound_to_port,
                cidr_blocks=[outbound_cidr],
                opts=pulumi.ResourceOptions(parent=self.security_group) # Set the security group as the parent

            )
