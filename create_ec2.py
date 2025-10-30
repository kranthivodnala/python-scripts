# Create EC2 Instance and Security Group

import boto3
import datetime
import requests

session = boto3.Session(profile_name='personal')
ec2_client = session.resource('ec2')

def create_ec2_instance():
    ec2 = ec2_client

# Detect Public IP for SSH Access
    try:
        my_ip = requests.get('https://api.ipify.org').text.strip()
        cidr_ip = f"{my_ip}/32"
        print(f"Detected public IP for SSH: {cidr_ip}")
    except Exception as e:
        raise RuntimeError(f"Failed to detect public IP: {e}")

    # Create Security Group
    security_group = ec2.create_security_group(
        GroupName='LabSecurityGroup',
        Description='Security group for lab EC2 instance'
    )
    security_group.authorize_ingress(
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': cidr_ip}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    print(f'Security Group Created {security_group.id} in vpc {security_group.vpc_id}')

      # --- User Data Script ---
    user_data_script = """#!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y git wget curl unzip python3 python3-pip docker.io
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ubuntu || usermod -aG docker ec2-user
    echo "DevOps environment setup completed" > /home/ubuntu/devops_setup.log || echo "Done" > /home/ec2-user/devops_setup.log
    """

    tag_value = f"Created using Python on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    # Create EC2 Instance
    instances = ec2.create_instances(
        ImageId='ami-0bdd88bd06d16ba03',  # Example AMI ID, replace with a valid one
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.medium',
        KeyName='',  # Replace with your key pair name
        SecurityGroupIds=[security_group.id],
        UserData=user_data_script,
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 8,
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp2'
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'LabInstance'
                    },
                    {
                        'Key': 'CreatedBy',
                        'Value': tag_value
                    }
                ]
            }
        ]
    )
    
    print(f"Created instance {instances[0].id}")
    return instances[0].id

if __name__ == '__main__':
    try:
        instance_id = create_ec2_instance()
        print(f"Successfully created EC2 instance with ID: {instance_id}")
    except Exception as e:
        print(f"Error creating EC2 instance: {str(e)}")