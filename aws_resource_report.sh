#!/bin/bash

#PROFILE="argus"
REGION="eu-west-1"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="aws_resource_report_${DATE}.md"

echo "# AWS Argus Cloud Resource Report (${DATE})" > $REPORT_FILE
echo "" >> $REPORT_FILE

function add_section() {
    local title="$1"
    local command="$2"

    echo "## $title" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE
    eval "$command" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE
    echo "" >> $REPORT_FILE
}

add_section "EC2 Instances" "aws ec2 describe-instances --region $REGION --query \"Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PrivateIpAddress,Tags]\" --output table"

add_section "RDS Databases" "aws rds describe-db-instances --region $REGION --query \"DBInstances[*].[DBInstanceIdentifier,Engine,DBInstanceStatus,Endpoint.Address]\" --output table"

add_section "ECS Clusters" "aws ecs list-clusters --region $REGION --output table"

add_section "EKS Clusters" "aws eks list-clusters --region $REGION --output table"

add_section "Lambda Functions" "aws lambda list-functions --region $REGION --query \"Functions[*].[FunctionName,Runtime,LastModified]\" --output table"

add_section "Security Groups" \
"aws ec2 describe-security-groups --region $REGION \
--query \"SecurityGroups[*].[GroupId,GroupName,Description,VpcId]\" --output table"

echo "✅ Report generated: $REPORT_FILE"
