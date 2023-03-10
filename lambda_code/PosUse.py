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
    #リソース取得
    dynamodb_client = boto3.client('dynamodb')
    try:
        user_id = event["userName"]
        birthdate = event["request"]["userAttributes"]["birthdate"]
        preferred_username = event["request"]["userAttributes"]["preferred_username"]
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)
    
    replace_birthdate = birthdate.replace("-","")
    
    try:
        #user情報をdynamodbに登録
        response = dynamodb_client.put_item(
            TableName = user_tb,
            Item={
                'user_id': {"S": user_id},
                'birthdate': {"N": replace_birthdate},
                'preferred_username': {"S": preferred_username},
                'movie_version': {"N": "0"},
                'follow_version': {"N": "0"}
            }
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    return event