import json
import pdb
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
    dynamodb_resource = boto3.resource("dynamodb")
    movie_table = dynamodb_resource.Table(movie_tb)
    user_table = dynamodb_resource.Table(user_tb)
    cognito  =  boto3.client("cognito-idp")
    
    try:
        user = event['user']
        list = event['list']
    except:
        #正しい値が取得できなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)  

    #指定されたmovie表示順を選択
    if list == "score":
      index = "score-index"
    elif list == "register":
      index = "date-index"
    else:
      index = "releace-index"

    try:
        # movie一覧を表示するuserを取得
        queryData = []
        user_queryData = user_table.query(
          KeyConditionExpression = Key("user_id").eq(user)
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    try:
        #userのmovie一覧を取得
        movie_queryData = movie_table.query(
          IndexName=index,
          KeyConditionExpression = Key("user_id").eq(user), # 取得するKey情報
          ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    #各値を返す
    queryData.append(user_queryData)
    queryData.append(movie_queryData)
    return queryData
