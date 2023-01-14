import json
import random
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
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_resource = boto3.resource("dynamodb")
    movie_table = dynamodb_resource.Table(movie_tb)
    user_table = dynamodb_resource.Table(user_tb)

    try:
        # すべてのuser_idを取得
        queryData = dynamodb_client.scan(
            TableName = user_tb, 
            AttributesToGet = ["user_id"]
        )
    except:
        #正しい値が送られてこなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)

    #すべてのuser_idからランダムにひとつのuser_idを取得
    user_id_array = queryData["Items"]
    user_ids = []
    
    for user in user_id_array:
      user_id = user["user_id"]["S"]
      user_ids.append(user_id)
    
    user_id = random.choice(user_ids)
    
    try:
        # ランダムに抽出したuser_idのuser情報を取得
        queryData = []
        user_queryData = user_table.query(
            KeyConditionExpression = Key("user_id").eq(user_id)
        )
    except:
        #正しい値が送られてこなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
    
    try:
        # ランダムに抽出したuser_idのmovie情報を取得
        movie_queryData = movie_table.query(
          IndexName="score-index",
          KeyConditionExpression = Key("user_id").eq(user_id), # 取得するKey情報
          ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
        )
    except:
        #正しい値が送られてこなかった場合の処理
        error_message = "データの取得に失敗しました"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)

    # 各情報を返す
    queryData.append(user_queryData)
    queryData.append(movie_queryData)
    return queryData
