import json

import pulumi


def generate_kube_config(eks_cluster):

    kubeconfig = pulumi.Output.json_dumps({
        "apiVersion": "v1",
        "clusters": [{
            "cluster": {
                "server": eks_cluster.endpoint,
                "certificate-authority-data": eks_cluster.certificate_authority.apply(lambda v: v.data)
            },
            "name": "kubernetes",
        }],
        "contexts": [{
            "context": {
                "cluster": "kubernetes",
                "user": "aws",
            },
            "name": "aws",
        }],
        "current-context": "aws",
        "kind": "Config",
        "users": [{
            "name": "aws",
            "user": {
                "exec": {
                    "apiVersion": "client.authentication.k8s.io/v1beta1",
                    "command": "aws-iam-authenticator",
                    "args": [
                        "token",
                        "-i",
                        eks_cluster.endpoint,
                    ],
                },
            },
        }],
    })
    return kubeconfig


def get_security_group_ids(security_group_names, networking_stack):
    security_group_ids = []
    for sg_name in security_group_names:
        sg_id = networking_stack.get_output(f"{sg_name}_security_group_id")
        security_group_ids.append(sg_id)
    return security_group_ids
