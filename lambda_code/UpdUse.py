import json
import boto3
import os

def lambda_handler(event, context):
    movie_tb = os.environ['MovieTable']
    user_tb = os.environ['UserTable']
    follow_tb = os.environ['FollowTable']

    client = boto3.client('cognito-idp')
    dynamodb = boto3.client('dynamodb')

    user = event["user"]
    
    responce = client.admin_get_user(
        UserPoolId = 'ap-northeast-1_R7kJOutuY',
        Username = user
        )
    
    for i in responce["UserAttributes"]:
        if i["Name"] == "preferred_username":
            preferred_username = i["Value"]
        if i["Name"] == "website":
            sns = i["Value"]
            
    dynamodb.update_item(
     TableName = user_tb,
     Key={
         'user_id': {"S": user},
     },
     AttributeUpdates = {
         'preferred_username': {
             "Action": "PUT",
             "Value": {"S": preferred_username}
         },
         'sns': {
             "Action": "PUT",
             "Value": {"S": sns}
         }
     }
    )

    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
