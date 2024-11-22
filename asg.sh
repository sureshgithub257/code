#!/bin/bash

# Path to the file containing ASG names (one per line)
ASG_FILE="asg_list.txt"

# AWS Region (modify as needed)
AWS_REGION="us-east-1"

# Check if the file exists
if [[ ! -f "$ASG_FILE" ]]; then
  echo "File $ASG_FILE not found!"
  exit 1
fi

# Loop through each ASG in the file and update
while IFS= read -r asg_name; do
  if [[ -n "$asg_name" ]]; then
    echo "Updating Auto Scaling Group: $asg_name"
    aws autoscaling update-auto-scaling-group \
      --auto-scaling-group-name "$asg_name" \
      --region "$AWS_REGION" \
      --desired-capacity 0 \
      --min-size 0 \
      --max-size 0

    if [[ $? -eq 0 ]]; then
      echo "Successfully updated $asg_name."
    else
      echo "Failed to update $asg_name."
    fi
  fi
done < "$ASG_FILE"


# aws autoscaling describe-auto-scaling-groups \
#   --region us-east-1 \
#   --query "AutoScalingGroups[?AutoScalingGroupName=='my-asg-1'].[AutoScalingGroupName,DesiredCapacity,MinSize,MaxSize]" \
#   --output table
