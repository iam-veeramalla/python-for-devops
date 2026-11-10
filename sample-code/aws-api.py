import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
resource_tagging = boto3.client('resourcegroupstaggingapi')


def list_ec2_instances():
    try:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'Tags': instance.get('Tags', [])
                })
        return instances
    except ClientError as e:
        print(f"Error listing EC2 instances: {e}")
        return []


def manage_instance(instance_id, action):
    try:
        if action == "start":
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Started instance: {instance_id}")
        elif action == "stop":
            ec2.stop_instances(InstanceIds=[instance_id])
        else:
            print("Invalid action. Use 'start' or 'stop'.")
    except ClientError as e:
        print(f"Error managing instance: {e}")


def list_s3_buckets():
    try:
        response = s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except ClientError as e:
        print(f"Error listing S3 buckets: {e}")
        return []


def list_objects_in_bucket(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except ClientError as e:
        print(f"Error listing objects in {bucket_name}: {e}")
        return []


def tag_resource(resource_arn, tags):
    try:
        formatted_tags = [{'Key': k, 'Value': v} for k, v in tags.items()]
        resource_tagging.tag_resources(
            ResourceARNList=[resource_arn],
            Tags=formatted_tags
        )
        print(f"Tagged resource {resource_arn} with {formatted_tags}")
    except ClientError as e:
        print(f"Error tagging resource: {e}")


if __name__ == "__main__":
    print("EC2 Instances:")
    for instance in list_ec2_instances():
        print(instance)

    print("\nS3 Buckets:")
    for bucket in list_s3_buckets():
        print(f"- {bucket}")
