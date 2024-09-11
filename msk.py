import boto3

def get_cluster_arn_by_name(msk_client, cluster_name):
    try:
        # List all clusters
        response = msk_client.list_clusters()
        clusters = response['ClusterInfoList']
        
        # Find the cluster ARN by name
        for cluster in clusters:
            if cluster['ClusterName'] == cluster_name:
                return cluster['ClusterArn']
        
        raise ValueError(f"No cluster found with the name: {cluster_name}")
    
    except Exception as e:
        print(f"Error retrieving cluster ARN: {e}")
        return None

def get_msk_broker_details(msk_client, cluster_arn):
    try:
        # Describe the MSK cluster
        response = msk_client.describe_cluster(ClusterArn=cluster_arn)
        cluster_info = response['Cluster']
        
        # Extract broker information
        brokers = cluster_info['ZookeeperConnectString']
        return brokers

    except Exception as e:
        print(f"Error retrieving MSK broker details: {e}")
        return None

if __name__ == "__main__":
    # Replace with your MSK cluster name and AWS region
    cluster_name = 'your-cluster-name'
    region = 'us-west-2'
    
    # Create Boto3 MSK client
    msk_client = boto3.client('kafka', region_name=region)
    
    # Get the ARN for the specified cluster name
    cluster_arn = get_cluster_arn_by_name(msk_client, cluster_name)
    
    if cluster_arn:
        # Get the broker details for the specified cluster ARN
        broker_details = get_msk_broker_details(msk_client, cluster_arn)
        
        if broker_details:
            print(f"The broker details for cluster {cluster_name} (ARN: {cluster_arn}) are: {broker_details}")
        else:
            print(f"Failed to retrieve broker details for cluster {cluster_name}")
    else:
        print(f"Failed to retrieve ARN for cluster {cluster_name}")
