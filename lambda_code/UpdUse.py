import json
import boto3
import os
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
    movie_tb = os.environ['MovieTable']
    user_tb = os.environ['UserTable']
    follow_tb = os.environ['FollowTable']
    userpool_id = os.environ['UserPoolID']

    #各リソース取得
    cognito_client = boto3.client('cognito-idp')
    dynamodb_client = boto3.client('dynamodb')
     
    try:
        user = event["user"]
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの更新に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)
    
    try:
        #congnito登録のユーザ取得
        responce = cognito_client.admin_get_user(
                        UserPoolId = userpool_id,
                        Username = user
                    )
    except:
        #cognito側でエラーが返された時の処理
        error_message = "データの更新に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    for i in responce["UserAttributes"]:
        if i["Name"] == "preferred_username":
            preferred_username = i["Value"]
        if i["Name"] == "website":
            sns = i["Value"]
            
    try:
        #dynamodbのユーザテーブル更新
        dynamodb_client.update_item(
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
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの更新に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
