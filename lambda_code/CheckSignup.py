import json
import boto3
import os
import hashlib
import traceback

#エラーを返す
class ExtendException(Exception):
    def __init__(self, statusCode, description, traceback_contents):
        self.statusCode = statusCode
        self.description = description
        self.traceback_contents = traceback_contents

    def __str__(self):
        obj = {
            "statusCode": self.statusCode,
            "description": self.description,
            "traceback": self.traceback_contents
        }
        return json.dumps(obj)

def lambda_handler(event, context):
    #環境変数取得
    userpool_id = os.environ['UserPoolID']
    #リソース取得
    cognito_client  =  boto3.client("cognito-idp")
    
    try:
        new_username = event['username']
        lower_new_username = new_username.lower()
        new_email = event['email']
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの送信に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)  

    try:
        response = cognito_client.list_users(
            UserPoolId = 'userpool_id,
            AttributesToGet = ["email"]
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの送信に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)

    usernames = []
    emails = []
    
    for user in response['Users']:
        Registered_username = user['Username']
        Registered_email = user['Attributes'][0]['Value']
        md5_Registered_email = hashlib.md5(Registered_email.encode("utf-8")).hexdigest()
        usernames.append(Registered_username)
        emails.append(md5_Registered_email)
        
    usernames.append(lower_new_username)
    emails.append(new_email)
    
    #重複確認 それぞれなにをJSに返すか
    response_clear = {"statusCode": 200}
    response_mail = {"statusCode": 401, "body": "Email already exists"}
    response_username = {"statusCode": 401, "body": "usernmae already exists"}
    
    if len(emails) != len(set(emails)):
        return json.dumps(response_mail)
    elif len(usernames) != len(set(usernames)):
        return json.dumps(response_username)
    else:
        return json.dumps(response_clear)

