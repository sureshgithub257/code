import boto3
import csv

def get_auto_scaling_groups(region_name):
    # Create a boto3 client for Auto Scaling
    client = boto3.client('autoscaling', region_name=region_name)
    
    # Initialize a list to hold the Auto Scaling Groups
    auto_scaling_groups = []

    # Retrieve the Auto Scaling Groups
    response = client.describe_auto_scaling_groups()

    for group in response['AutoScalingGroups']:
        auto_scaling_groups.append({
            'AutoScalingGroupName': group['AutoScalingGroupName'],
            'LaunchConfigurationName': group.get('LaunchConfigurationName', 'N/A'),
            'MinSize': group['MinSize'],
            'MaxSize': group['MaxSize'],
            'DesiredCapacity': group['DesiredCapacity'],
            'VPCZoneIdentifier': group.get('VPCZoneIdentifier', 'N/A'),
            'Tags': ', '.join([tag['Key'] + '=' + tag['Value'] for tag in group.get('Tags', [])])
        })

    return auto_scaling_groups

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
    output_file = 'auto_scaling_groups.csv'
    
    # Get the Auto Scaling Groups
    auto_scaling_groups = get_auto_scaling_groups(region)
    
    # Write the data to CSV
    write_to_csv(auto_scaling_groups, output_file)
    
    print(f"Data written to {output_file}")
