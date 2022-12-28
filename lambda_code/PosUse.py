import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    user_id = event["userName"]
    birthdate = event["request"]["userAttributes"]["birthdate"]
    preferred_username = event["request"]["userAttributes"]["preferred_username"]
    
    replace_birthdate = birthdate.replace("-","")
    
    response = dynamodb.put_item(
     TableName = 'user',
     Item={
         'user_id': {"S": user_id},
         'birthdate': {"N": replace_birthdate},
         'preferred_username': {"S": preferred_username},
         'movie_version': {"N": "0"},
         'follow_version': {"N": "0"}
     }
    )
    
    return event