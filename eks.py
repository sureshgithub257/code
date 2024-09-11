import boto3


import boto3

def get_eks_nodegroup_instances(eks_client, ec2_client, cluster_name, nodegroup_name):
    # Get details of the specified node group
    response = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
    nodegroup = response['nodegroup']
    
    # Extract the node role ARN
    node_role_arn = nodegroup['nodeRole']
    
    # Get the instance IDs associated with the node role
    instance_ids = get_instance_ids_by_role(ec2_client, node_role_arn)
    return instance_ids

def get_instance_ids_by_role(ec2_client, role_arn):
    instance_ids = set()
    
    # Describe instances to get those associated with the specified role
    paginator = ec2_client.get_paginator('describe_instances')
    for page in paginator.paginate(Filters=[
        {'Name': 'iam-instance-profile.arn', 'Values': [role_arn]}
    ]):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.add(instance['InstanceId'])
    
    return list(instance_ids)

def print_instance_ids(instance_ids):
    if not instance_ids:
        print("No instances found for the specified node group.")
    else:
        print("Instance IDs:")
        for instance_id in instance_ids:
            print(f"  {instance_id}")

if __name__ == "__main__":
    # Replace these with your actual EKS cluster name, node group name, and AWS region
    cluster_name = 'your-cluster-name'
    nodegroup_name = 'your-nodegroup-name'
    region = 'us-west-2'
    
    # Create Boto3 clients
    eks_client = boto3.client('eks', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)
    
    # Get instance IDs for the specified node group
    instance_ids = get_eks_nodegroup_instances(eks_client, ec2_client, cluster_name, nodegroup_name)
    
    # Print the instance IDs
    print_instance_ids(instance_ids)


def list_eks_node_groups(eks_client, cluster_name):
    # List the node groups for the specified cluster
    response = eks_client.list_nodegroups(clusterName=cluster_name)
    node_groups = response['nodegroups']
    return node_groups

def describe_node_groups(eks_client, cluster_name, node_group_names):
    # Get detailed information for each node group
    node_group_details = []
    for node_group_name in node_group_names:
        response = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=node_group_name)
        node_group_details.append(response['nodegroup'])
    return node_group_details

def print_node_group_details(node_groups):
    for node_group in node_groups:
        print(f"Node Group Name: {node_group['nodegroupName']}")
        print(f"Node Group ARN: {node_group['nodegroupArn']}")
        print(f"Cluster Name: {node_group['clusterName']}")
        print(f"Node Role ARN: {node_group['nodeRole']}")
        print(f"Scaling Config: Min={node_group['scalingConfig']['minSize']}, Max={node_group['scalingConfig']['maxSize']}, Desired={node_group['scalingConfig']['desiredSize']}")
        print(f"Subnets: {node_group['subnets']}")
        print(f"Instance Types: {node_group['instanceTypes']}")
        print(f"Launch Template: {node_group.get('launchTemplate', 'N/A')}")
        print(f"Labels: {node_group['labels']}")
        print(f"Taints: {node_group['taints']}")
        print(f"Created At: {node_group['createdAt']}")
        print(f"Status: {node_group['status']}")
        print("\n")

if __name__ == "__main__":
    # Replace these with your actual EKS cluster name and AWS region
    cluster_name = 'your-cluster-name'
    region = 'us-west-2'
    
    # Create Boto3 client
    eks_client = boto3.client('eks', region_name=region)
    
    # List node groups for the EKS cluster
    node_group_names = list_eks_node_groups(eks_client, cluster_name)
    
    # Get detailed information about each node group
    node_groups = describe_node_groups(eks_client, cluster_name, node_group_names)
    
    # Print node group details
    print_node_group_details(node_groups)
