import json
import boto3
import os

movie = os.environ['MovieTable']
user = os.environ['UserTable']
follow = os.environ['FollowTable']

client = boto3.client('cognito-idp')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)
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
     TableName = user,
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
