import json
import boto3
from boto3.dynamodb.conditions import Key
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
    #各リソース取得
    dynamoDB = boto3.resource("dynamodb")
    follow_table = dynamoDB.Table(follow_tb)
    user_table = dynamoDB.Table(user_tb)
    
    try:
        user_id = event['user_id']
        follow = event['follow']
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの削除に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)  
    
    try:
        #  フォロー削除
        follow_table.delete_item(
            Key = {
                'user_id': user_id,
                'follow': follow
            }
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの削除に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    # revision更新
    user_table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set follow_version = follow_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )
