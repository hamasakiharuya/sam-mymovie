import json
import boto3
import urllib.parse
import re
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
    contact_tb = os.environ['ContactTable']
    #リソース取得
    dynamodb_client = boto3.client('dynamodb')
    
    try:
        category = event["category"]
        email = event["email"]
        contents = event["contents"]
    except:
        #正しい値が送られてこなかった場合の処理
        error_message = "The value you entered is incorrect"
        traceback_contents = traceback.format_exc()
        raise ExtendException(400, error_message, traceback_contents)
        
    decode_category = urllib.parse.unquote(category)
    decode_email = urllib.parse.unquote(email)
    decode_contents = urllib.parse.unquote(contents)
    
    try:
        dynamodb_client.put_item(
         TableName = contact_tb,
             Item={
                 'category': {"S": decode_category},
                 'email': {"S": decode_email},
                 'contents': {"S": decode_contents},
             }
        )
    except:
        #dynamodb側でエラーが返された時の処理
        error_message = "Failed to link with dynamodb"
        traceback_contents = traceback.format_exc()
        raise ExtendException(500, error_message, traceback_contents)
        
    return {
        'statusCode': 200,
        'body': json.dumps('completed send contents')
     }
         