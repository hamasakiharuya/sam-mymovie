import json
import pdb
import boto3
from boto3.dynamodb.conditions import Key
import os

movie = os.environ['MovieTable']
user = os.environ['UserTable']
follow = os.environ['FollowTable']


def lambda_handler(event, context):
    dynamoDB = boto3.resource("dynamodb")
    movie_table = dynamoDB.Table(movie)
    user_table = dynamoDB.Table(user)
    cognito  =  boto3.client("cognito-idp")
    
    user = event['user']
    list = event['list']

    if list == "score":
      index = "score-index"
    elif list == "register":
      index = "date-index"
    else:
      index = "releace-index"

    # DynamoDBへのqueåry処理実行
    queryData = []
    user_queryData = user_table.query(
      KeyConditionExpression = Key("user_id").eq(user)
    )
      
    movie_queryData = movie_table.query(
      IndexName=index,
      KeyConditionExpression = Key("user_id").eq(user), # 取得するKey情報
      ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
    )
    
    queryData.append(user_queryData)
    queryData.append(movie_queryData)
    print(queryData)
    return queryData
