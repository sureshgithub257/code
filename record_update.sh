#!/bin/bash

# Variables
HOSTED_ZONE_ID="<Your-Hosted-Zone-ID>"      # Replace with your Route 53 Hosted Zone ID
RECORD_NAME="<record.example.com>"          # Replace with your DNS record name
NLB_NAME="<Your-NLB-Name>"                  # Replace with your NLB name
TTL=300                                     # Time-To-Live for the DNS record

# Get the DNS name of the Network Load Balancer
NLB_DNS_NAME=$(aws elbv2 describe-load-balancers \
    --names "$NLB_NAME" \
    --query "LoadBalancers[0].DNSName" \
    --output text)

if [ -z "$NLB_DNS_NAME" ]; then
    echo "Error: Unable to fetch the DNS name for NLB '$NLB_NAME'."
    exit 1
fi

echo "NLB DNS Name: $NLB_DNS_NAME"

# Create the JSON payload for the Route 53 change
CHANGE_BATCH=$(cat <<EOF
{
  "Comment": "Update Route 53 record for NLB",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "$RECORD_NAME",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z32O12XQLNTSW2",  # Hosted Zone ID for NLB, see below
          "DNSName": "$NLB_DNS_NAME",
          "EvaluateTargetHealth": false
        }
      }
    }
  ]
}
EOF
)

# Update the Route 53 record
aws route53 change-resource-record-sets \
    --hosted-zone-id "$HOSTED_ZONE_ID" \
    --change-batch "$CHANGE_BATCH"

if [ $? -eq 0 ]; then
    echo "Route 53 record '$RECORD_NAME' updated successfully to point to NLB '$NLB_NAME'."
else
    echo "Error: Failed to update Route 53 record."
    exit 1
fi
