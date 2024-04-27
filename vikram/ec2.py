import boto3
import json
from datetime import datetime

client = boto3.client('ec2')
response = client.describe_instances()

# Convert response to JSON string, ignoring datetime objects
response_json = json.dumps(response, indent=4, default=lambda o: str(o) if isinstance(o, datetime) else None)

# Print JSON string
print(response_json)