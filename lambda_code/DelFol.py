import json
import boto3
from boto3.dynamodb.conditions import Key
import os

def lambda_handler(event, context):
    movie_tb = os.environ['MovieTable']
    user_tb = os.environ['UserTable']
    follow_tb = os.environ['FollowTable']

    dynamoDB = boto3.resource("dynamodb")
    follow_table = dynamoDB.Table(follow_tb)
    user_table = dynamoDB.Table(user_tb)
    
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
