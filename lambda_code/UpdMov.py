import json
import boto3
import urllib.parse
import os

def lambda_handler(event, context):
    movie_tb = os.environ['MovieTable']
    user_tb = os.environ['UserTable']
    follow_tb = os.environ['FollowTable']

    dynamodb = boto3.client('dynamodb')
    dynamoDB = boto3.resource("dynamodb")
    user_table = dynamoDB.Table(user_tb)
    
    user_id = event["user_id"]
    title = event["title"]
    score = event["score"]
    
    decode_movie = urllib.parse.unquote(title)
    decode2_movie = urllib.parse.unquote(decode_movie)
    decode_movie_remove_null = decode2_movie.replace('+', ' ')
    
    dynamodb.update_item(
     TableName = movie_tb,
     Key={
         'user_id': {"S": user_id},
         'title': {"S": decode_movie_remove_null}
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
