import boto3
import csv

def get_eks_node_groups(region_name, cluster_name):
    eks_client = boto3.client('eks', region_name=region_name)
    
    # Get the EKS node groups for the specified cluster
    response = eks_client.list_nodegroups(clusterName=cluster_name)
    nodegroup_names = response['nodegroups']
    
    node_groups_info = []
    
    for nodegroup_name in nodegroup_names:
        nodegroup = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
        node_group_info = nodegroup['nodegroup']
        node_groups_info.append({
            'NodeGroupName': node_group_info['nodegroupName'],
            'InstanceTypes': ', '.join(node_group_info['scalingConfig']['instanceTypes']),
            'MinSize': node_group_info['scalingConfig']['minSize'],
            'MaxSize': node_group_info['scalingConfig']['maxSize'],
            'DesiredCapacity': node_group_info['scalingConfig']['desiredCapacity']
        })
    
    return node_groups_info

def write_to_csv(data, filename):
    # Specify the header based on the keys of the first dictionary item
    headers = data[0].keys() if data else []
    
    # Write the data to a CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    region = 'us-west-2'  # Replace with your desired region
    cluster_name = 'your-cluster-name'  # Replace with your EKS cluster name
    output_file = 'eks_nodegroups.csv'
    
    # Get the EKS node groups
    node_groups = get_eks_node_groups(region, cluster_name)
    
    # Write the data to CSV
    write_to_csv(node_groups, output_file)
    
    print(f"Data written to {output_file}")
