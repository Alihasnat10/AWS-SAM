import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MyDynamoDBTable')
    print(event)
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        
        text_length = len(content)
        print(content)
        print()
        print(str(text_length))
        try:
            item = {
                'filename': object_key,
                'content_length': text_length
            }
            table.put_item(Item=item)
            print("Stored to dynamodb")
        except Exception as e:
            print("Error while uploading to dynamodb")
            print(e)
        
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": str(text_length) + " length, stored to dynamodb."
        }),
    }