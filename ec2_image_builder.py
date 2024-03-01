import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2')


def create_ec2_instance(ami_id):
  subnet_id = 'subnet-xxxxxxxxxxxxxxxx' #need to change

  response = ec2_client.run_instances(
      ImageId=ami_id,
      InstanceType='t3.large',
      MinCount=1,
      MaxCount=1,
      NetworkInterfaces=[
          {
              'SubnetId': subnet_id,
              'DeviceIndex': 0,
              'AssociatePublicIpAddress': True
          }
      ],
      TagSpecifications=[
          {
              'ResourceType': 'instance',
              'Tags': [
                  {
                      'Key': 'Name',
                      'Value': 'Instance for Scan Amazon Linux 2 AZL2'
                  }
              ]
          }
      ]
  )

  instance_id = response["Instances"][0]["InstanceId"]
  logger.info(f'New EC2 instance created with ID: {
              response["Instances"][0]["InstanceId"]}')

  return instance_id


def lambda_handler(event, context):
  logger.info('Lambda function execution starts')

  sns_message = event['Records'][0]['Sns']['Message']

  try:
    sns_message = json.loads(sns_message)
  except json.JSONDecodeError as e:
    logger.error(f'Error decoding SNS message as JSON: {e}')
    return

  print(sns_message)

  ami_status = sns_message.get('state', {}).get('status')

  logger.info(f'AMI status: {ami_status}')

  if ami_status == 'AVAILABLE':
    logger.info('The AMI was generated successfully')

    for ami_info in sns_message.get('outputResources', {}).get('amis', []):
      ami_id = ami_info.get('image')
      vpc_id = 'subnet-xxxxxxxxxxxxxxx' #need to change
      create_ec2_instance(ami_id)
      break
  else:
    logger.warning(f'The image creation state is: {
                   ami_status}. No instances will be created.')

  logger.info('End of Lambda function execution')
