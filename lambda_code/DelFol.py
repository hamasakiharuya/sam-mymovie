import json
import boto3
from boto3.dynamodb.conditions import Key
import os

movie = os.environ['MovieTable']
user = os.environ['UserTable']
follow = os.environ['FollowTable']

def lambda_handler(event, context):
    dynamoDB = boto3.resource("dynamodb")
    follow_table = dynamoDB.Table(follow)
    user_table = dynamoDB.Table(user)
    
    user_id = event['user_id']
    follow = event['follow']
    
    # 映画削除
    follow_table.delete_item(
        Key = {
            'user_id': user_id,
            'follow': follow
        }
    )
    
    # version更新
    user_table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set follow_version = follow_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('delete OK')
    }
