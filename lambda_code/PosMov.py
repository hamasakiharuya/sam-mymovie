import json
import boto3
import urllib.parse
import re
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
    table = dynamodb_resource.Table(user_tb)
    
    try:
        user_id = event["user_id"]
        title = event["title"]
        date = event["date"]
        score = event["score"]
        username = event["username"]
        birthday = event["birthday"]
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの送信に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents) 
    
    #送信されたデータ加工
    decode_username = urllib.parse.unquote(username)
    decode_movie = urllib.parse.unquote(title)
    decode_movie_remove_null = decode_movie.replace('+', ' ')
    title_date = decode_movie_remove_null.split('--')
    title = title_date[0]
    replace_date = title_date[1].replace('/', '')
    image_path = title_date[2]
    title = title.replace('&', '')
    
    try:
        dynamodb_client.put_item(
            TableName = movie_tb,
            Item={
                'user_id': {"S": user_id},
                'title': {"S": title},
                'date': {"N": date},
                'score': {"N": score},
                'username': {"S": decode_username},
                'birthday': {"N": birthday},
                'releace' : {"N": replace_date},
                'image_path': {"S": image_path}
            }
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの登録に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    # revision更新
    table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression='set movie_version = movie_version + :add',
        ExpressionAttributeValues={
          ':add': 1,
        }
    )