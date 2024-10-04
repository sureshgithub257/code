import boto3
import csv

# Initialize boto3 client for EC2
ec2 = boto3.client('ec2')

# Function to retrieve and export security group rules
def export_security_group_rules(security_group_id, csv_filename):
    try:
        # Get the details of the security group
        response = ec2.describe_security_groups(GroupIds=[security_group_id])

        # Open CSV file for writing
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write the CSV header
            csvwriter.writerow([
                'Type', 'Protocol', 'PortRange', 'Source/Destination', 'Description'
            ])

            # Get the security group details
            security_group = response['SecurityGroups'][0]

            # Process Inbound Rules (Ingress)
            for rule in security_group['IpPermissions']:
                process_rule(csvwriter, rule, 'Inbound')

            # Process Outbound Rules (Egress)
            for rule in security_group['IpPermissionsEgress']:
                process_rule(csvwriter, rule, 'Outbound')

        print(f"Security group rules exported to {csv_filename}")
    
    except Exception as e:
        print(f"Error retrieving security group rules: {e}")

# Helper function to process rules
def process_rule(csvwriter, rule, rule_type):
    protocol = rule.get('IpProtocol', 'all')
    
    # Handle port range
    from_port = rule.get('FromPort', 'All')
    to_port = rule.get('ToPort', 'All')
    
    if from_port == to_port:
        port_range = from_port if from_port != -1 else 'All'
    else:
        port_range = f"{from_port}-{to_port}"

    # Handle CIDR ranges for IPs
    if 'IpRanges' in rule:
        for ip_range in rule['IpRanges']:
            csvwriter.writerow([
                rule_type,
                protocol,
                port_range,
                ip_range.get('CidrIp', 'N/A'),
                ip_range.get('Description', 'N/A')
            ])
    
    # Handle IPv6 ranges
    if 'Ipv6Ranges' in rule:
        for ipv6_range in rule['Ipv6Ranges']:
            csvwriter.writerow([
                rule_type,
                protocol,
                port_range,
                ipv6_range.get('CidrIpv6', 'N/A'),
                ipv6_range.get('Description', 'N/A')
            ])
    
    # Handle security group references (Source/Destination security groups)
    if 'UserIdGroupPairs' in rule:
        for group_pair in rule['UserIdGroupPairs']:
            csvwriter.writerow([
                rule_type,
                protocol,
                port_range,
                group_pair.get('GroupId', 'N/A'),
                group_pair.get('Description', 'N/A')
            ])

# Example usage
security_group_id = 'sg-xxxxxxxx'  # Replace with your Security Group ID
csv_filename = 'security_group_rules.csv'

# Export security group rules to CSV
export_security_group_rules(security_group_id, csv_filename)
