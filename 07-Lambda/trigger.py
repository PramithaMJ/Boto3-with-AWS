import json

def lambda_trigger(event, context):
    s3_object_key = event['Records'][0]['s3']['object']['key']
    print(f"File uploaded: {s3_object_key}")
    return s3_object_key