import json
import boto3
import os

def lambda_handler(event, context):
    movie_tb = os.environ['MovieTable']
    user_tb = os.environ['UserTable']
    follow_tb = os.environ['FollowTable']

    dynamodb = boto3.client('dynamodb')
    
    user_id = event["userName"]
    birthdate = event["request"]["userAttributes"]["birthdate"]
    preferred_username = event["request"]["userAttributes"]["preferred_username"]
    
    replace_birthdate = birthdate.replace("-","")
    
    response = dynamodb.put_item(
     TableName = user_tb,
     Item={
         'user_id': {"S": user_id},
         'birthdate': {"N": replace_birthdate},
         'preferred_username': {"S": preferred_username},
         'movie_version': {"N": "0"},
         'follow_version': {"N": "0"}
     }
    )
    
    return event