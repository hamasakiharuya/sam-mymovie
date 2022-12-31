import json
import boto3
import urllib.parse
import os

def lambda_handler(event, context):
    movie = os.environ['MovieTable']
    user = os.environ['UserTable']
    follow = os.environ['FollowTable']

    dynamodb = boto3.client('dynamodb')
    dynamoDB = boto3.resource("dynamodb")
    user_table = dynamoDB.Table(user)
    
    user_id = event["user_id"]
    title = event["title"]
    score = event["score"]
    
    decode_movie = urllib.parse.unquote(title)
    decode2_movie = urllib.parse.unquote(decode_movie)
    
    print(decode2_movie)
    
    dynamodb.update_item(
     TableName = movie,
     Key={
         'user_id': {"S": user_id},
         'title': {"S": decode2_movie}
     },
     AttributeUpdates = {
         'score': {
             "Action": "PUT",
             "Value": {"N": score}
         }
     }
    )
    
    # version更新
    user_table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set movie_version = movie_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )
         
    return {
        'statusCode': 200
    }
