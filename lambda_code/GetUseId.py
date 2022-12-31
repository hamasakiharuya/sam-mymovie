import json
import random
import pdb
import boto3
from boto3.dynamodb.conditions import Key
import os

def lambda_handler(event, context):
    movie = os.environ['MovieTable']
    user = os.environ['UserTable']
    follow = os.environ['FollowTable']
    dynamodb = boto3.client('dynamodb')
    dynamoDB = boto3.resource("dynamodb")
    movie_table = dynamoDB.Table(movie)
    user_table = dynamoDB.Table(user)


    # DynamoDBへのquery処理実行
    queryData = dynamodb.scan(
      TableName = user, 
      AttributesToGet = ["user_id"]
    )
    print(queryData)
    
    user_id_array = queryData["Items"]
    user_ids = []
    
    for user in user_id_array:
      user_id = user["user_id"]["S"]
      user_ids.append(user_id)
    
    #ランダムに取得したuser
    user_id = random.choice(user_ids)
    
    # DynamoDBへのquery処理実行
    queryData = []
    user_queryData = user_table.query(
      KeyConditionExpression = Key("user_id").eq(user_id)
    )
      
    movie_queryData = movie_table.query(
      IndexName="score-index",
      KeyConditionExpression = Key("user_id").eq(user_id), # 取得するKey情報
      ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
    )
    
    queryData.append(user_queryData)
    queryData.append(movie_queryData)

    return queryData
