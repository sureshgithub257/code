import argparse

# Function to process arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to get AWS account ID, Kubernetes cluster name, and AWS region')

    # Define the arguments
    parser.add_argument('--account-id', type=str, required=True, help='AWS account ID')
    parser.add_argument('--cluster-name', type=str, required=True, help='Kubernetes cluster name')
    parser.add_argument('--region', type=str, required=True, help='AWS region')

    # Parse the arguments
    args = parser.parse_args()

    return args

# Main function
def main():
    # Parse the arguments
    args = parse_arguments()

    # Access the arguments
    account_id = args.account_id
    cluster_name = args.cluster_name
    region = args.region

    # Print the values (or use them in your logic)
    print(f"AWS Account ID: {account_id}")
    print(f"Cluster Name: {cluster_name}")
    print(f"AWS Region: {region}")

if __name__ == '__main__':
    main()
