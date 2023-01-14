import json
import boto3
import urllib.parse
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
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_resource = boto3.resource("dynamodb")
    user_table = dynamodb_resource.Table(user_tb)
    
    try:
        user_id = event["user_id"]
        title = event["title"]
        score = event["score"]
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents) 
    
    #送信されたデータ加工
    decode_movie = urllib.parse.unquote(title)
    decode2_movie = urllib.parse.unquote(decode_movie)
    decode_movie_remove_null = decode2_movie.replace('+', ' ')
    
    try:
        dynamodb_client.update_item(
            TableName = movie_tb,
            Key={
                'user_id': {"S": user_id},
                'title': {"S": decode_movie_remove_null}
            },
            AttributeUpdates = {
                'score': {
                    "Action": "PUT",
                    "Value": {"N": score}
                }
            }
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    # revision更新
    user_table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set movie_version = movie_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )
