import boto3

def get_eks_security_groups(eks_client, cluster_name):
    # Get the EKS cluster details
    response = eks_client.describe_cluster(name=cluster_name)
    cluster = response['cluster']
    
    # Extract the security groups associated with the EKS cluster
    security_groups = cluster['resourcesVpcConfig']['securityGroupIds']
    return security_groups

def get_security_group_rules(ec2_client, security_group_ids):
    # Get details for each security group
    response = ec2_client.describe_security_groups(GroupIds=security_group_ids)
    security_groups = response['SecurityGroups']
    
    rules = {}
    
    for sg in security_groups:
        sg_id = sg['GroupId']
        rules[sg_id] = {
            'InboundRules': sg.get('IpPermissions', []),
            'OutboundRules': sg.get('IpPermissionsEgress', [])
        }
    
    return rules

def print_rules(rules):
    for sg_id, rule_set in rules.items():
        print(f"Security Group ID: {sg_id}")
        
        print("Inbound Rules:")
        for rule in rule_set['InboundRules']:
            print(f"  Protocol: {rule.get('IpProtocol', 'ALL')}")
            for ip_range in rule.get('IpRanges', []):
                print(f"    CIDR: {ip_range['CidrIp']}")
            for group in rule.get('UserIdGroupPairs', []):
                print(f"    Security Group: {group['GroupId']}")
        
        print("Outbound Rules:")
        for rule in rule_set['OutboundRules']:
            print(f"  Protocol: {rule.get('IpProtocol', 'ALL')}")
            for ip_range in rule.get('IpRanges', []):
                print(f"    CIDR: {ip_range['CidrIp']}")
            for group in rule.get('UserIdGroupPairs', []):
                print(f"    Security Group: {group['GroupId']}")
        
        print("\n")

if __name__ == "__main__":
    # Replace these with your actual EKS cluster name and AWS region
    cluster_name = 'your-cluster-name'
    region = 'us-west-2'
    
    # Create Boto3 clients
    eks_client = boto3.client('eks', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)
    
    # Get security groups associated with the EKS cluster
    security_groups = get_eks_security_groups(eks_client, cluster_name)
    
    # Get rules for these security groups
    rules = get_security_group_rules(ec2_client, security_groups)
    
    # Print the rules
    print_rules(rules)
