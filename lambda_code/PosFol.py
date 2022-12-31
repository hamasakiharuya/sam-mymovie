import json
import boto3
import os

movie = os.environ['MovieTable']
user = os.environ['UserTable']
follow = os.environ['FollowTable']

dynamodb = boto3.client('dynamodb')
dynamoDB = boto3.resource("dynamodb")
table = dynamoDB.Table(user)

def lambda_handler(event, context):
    
    user_id = event["user_id"]
    follow = event["follow"]
    print(user_id)
    
    
    dynamodb.put_item(
     TableName = follow,
     Item={
         'user_id': {"S": user_id},
         'follow': {"S": follow}
     }
    )
    
    table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set follow_version = follow_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )
         
    return {
        'statusCode': 200
    }