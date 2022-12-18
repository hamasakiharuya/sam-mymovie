import json
import boto3

def lambda_handler(event, context):
    cognito  =  boto3.client("cognito-idp")
    
    new_username = event['username']
    new_email = event['email']

    response = cognito.list_users(
      UserPoolId = 'ap-northeast-1_R7kJOutuY',
      AttributesToGet = ["email"],
     )

    usernames = []
    emails = []
    
    for user in response['Users']:
        Registered_username = user['Username']
        Registered_email = user['Attributes'][0]['Value']
        usernames.append(Registered_username)
        emails.append(Registered_email)
        
    usernames.append(new_username)
    emails.append(new_email)
    
    #重複確認 それぞれなにをJSに返すか
    response_clear = {"statusCode": 200}
    response_mail = {"statusCode": 400, "body": "Email already exists"}
    response_username = {"statusCode": 400, "body": "usernmae already exists"}
    
    if len(emails) != len(set(emails)):
        return json.dumps(response_mail)
    elif len(usernames) != len(set(usernames)):
        return json.dumps(response_username)
    else:
        return json.dumps(response_clear)

