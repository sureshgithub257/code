import boto3

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
    # Replace with your MSK cluster ARN and AWS region
    cluster_arn = 'arn:aws:kafka:us-west-2:123456789012:cluster/MyCluster/abcd1234-5678-90ab-cdef-EXAMPLE1234'
    region = 'us-west-2'
    
    # Create Boto3 MSK client
    msk_client = boto3.client('kafka', region_name=region)
    
    # Get the broker details for the specified cluster
    broker_details = get_msk_broker_details(msk_client, cluster_arn)
    
    if broker_details:
        print(f"The broker details for cluster {cluster_arn} are: {broker_details}")
    else:
        print(f"Failed to retrieve broker details for cluster {cluster_arn}")
