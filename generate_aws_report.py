import boto3
import pandas as pd
from datetime import datetime

REGION = "eu-west-1"
SESSION = boto3.Session(region_name=REGION)

def get_ec2_instances():
    ec2 = SESSION.client("ec2")
    instances = []
    for res in ec2.describe_instances()["Reservations"]:
        for inst in res["Instances"]:
            tag_dict = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
            instances.append({
                "InstanceId": inst["InstanceId"],
                "InstanceName": tag_dict.get("Name", ""),
                "InstanceType": inst["InstanceType"],
                "State": inst["State"]["Name"],
                "PrivateIP": inst.get("PrivateIpAddress", ""),
                "Tags": tag_dict
            })
    return pd.DataFrame(instances)

def get_rds_instances():
    rds = SESSION.client("rds")
    dbs = rds.describe_db_instances()["DBInstances"]
    data = []

    for db in dbs:
        arn = db["DBInstanceArn"]
        # Pega as tags associadas ao RDS
        tags = rds.list_tags_for_resource(ResourceName=arn)["TagList"]
        tag_dict = {t["Key"]: t["Value"] for t in tags}
        instance_name = tag_dict.get("Name", "")

        data.append({
            "DBInstanceIdentifier": db["DBInstanceIdentifier"],
            "NameTag": instance_name,
            "Engine": db["Engine"],
            "Status": db["DBInstanceStatus"],
            "Endpoint": db["Endpoint"]["Address"],
            "Tags": tag_dict
        })

    return pd.DataFrame(data)

def get_ecs_clusters():
    ecs = SESSION.client("ecs")
    cluster_arns = ecs.list_clusters()["clusterArns"]
    return pd.DataFrame([{"ClusterArn": arn} for arn in cluster_arns])

def get_eks_clusters():
    eks = SESSION.client("eks")
    clusters = eks.list_clusters()["clusters"]
    return pd.DataFrame([{"ClusterName": name} for name in clusters])

def get_lambda_functions():
    lamb = SESSION.client("lambda")
    funcs = lamb.list_functions()["Functions"]
    data = [{
        "FunctionName": f["FunctionName"],
        "Runtime": f["Runtime"],
        "LastModified": f["LastModified"]
    } for f in funcs]
    return pd.DataFrame(data)

def get_security_groups():
    ec2 = SESSION.client("ec2")
    sgs = ec2.describe_security_groups()["SecurityGroups"]
    data = [{
        "GroupId": sg["GroupId"],
        "GroupName": sg["GroupName"],
        "Description": sg["Description"],
        "VpcId": sg.get("VpcId", ""),
        "InboundRules": len(sg["IpPermissions"]),
        "OutboundRules": len(sg["IpPermissionsEgress"])
    } for sg in sgs]
    return pd.DataFrame(data)

# Main export
def export_to_excel():
    filename = f"aws_resource_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        get_ec2_instances().to_excel(writer, index=False, sheet_name="EC2 Instances")
        get_rds_instances().to_excel(writer, index=False, sheet_name="RDS Databases")
        get_ecs_clusters().to_excel(writer, index=False, sheet_name="ECS Clusters")
        get_eks_clusters().to_excel(writer, index=False, sheet_name="EKS Clusters")
        get_lambda_functions().to_excel(writer, index=False, sheet_name="Lambda Functions")
        get_security_groups().to_excel(writer, index=False, sheet_name="Security Groups")

    print(f"✅ Report saved to: {filename}")

if __name__ == "__main__":
    export_to_excel()
