import json
import boto3
import urllib.parse
import re
import os

def lambda_handler(event, context):
    movie = os.environ['MovieTable']
    user = os.environ['UserTable']
    follow = os.environ['FollowTable']

    dynamodb = boto3.client('dynamodb')
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(user)
    
    user_id = event["user_id"]
    title = event["title"]
    date = event["date"]
    score = event["score"]
    username = event["username"]
    birthday = event["birthday"]
    
    decode_username = urllib.parse.unquote(username)
    decode_movie = urllib.parse.unquote(title)
    decode_movie_remove_null = decode_movie.replace('+', ' ')
    title_date = decode_movie_remove_null.split('--')
    title = title_date[0]
    replace_date = title_date[1].replace('/', '')
    image_path = title_date[2]
    
    title = title.replace('&', '')
    
    dynamodb.put_item(
     TableName = movie,
     Item={
         'user_id': {"S": user_id},
         'title': {"S": title},
         'date': {"N": date},
         'score': {"N": score},
         'username': {"S": decode_username},
         'birthday': {"N": birthday},
         'releace' : {"N": replace_date},
         'image_path': {"S": image_path}
     }
    )
    
    table.update_item(
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