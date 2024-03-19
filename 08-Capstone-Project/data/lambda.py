from pathlib import Path
import boto3

dynamodb = boto3.client('dynamodb')

### Extract metadata from the file ###
def extract_metadata(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']
    file_type = Path(key).suffix[1:]
    if not file_type:
        file_type = "None"
    return bucket, key, file_type, size

### Add metadata to database. Use file identifier as id ###
def add_to_database(bucket, key, file_type, size):
    id = f"{bucket}/{key}"
    response = dynamodb.put_item(
        TableName='MediaMetadata',  # Change to your table
        Item={
            'id': {'S': id},
            'filetype': {'S': file_type},
            'size': {'N': str(size)}
        }
    )
    print(f"Data added to DynamoDB: {response}")

### Lambda handler routine ###
def lambda_handler(event, context):
    # Extract bucket and file key from S3 Event
    bucket, key, file_type, size = extract_metadata(event)
    print(file_type, size / 1024)
    add_to_database(bucket, key, file_type, size / 1024)
